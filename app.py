"""
PesoLens ₱1000 Bill Scanner
Streamlit + YOLOv8 deployment app.

Before running:
1. Put your trained YOLOv8 model at: models/trained_model_100_epoch.pt
2. Install dependencies: pip install -r requirements.txt
3. Run: streamlit run app.py
"""

from __future__ import annotations

import io

import pandas as pd
import streamlit as st
from PIL import Image

from src.detector import DEFAULT_CONFIDENCE, get_model_class_names, load_yolo_model, run_detection
from src.ui import (
    apply_css,
    render_brand,
    render_breakdown,
    render_empty_state,
    render_floating_model_notification,
    render_scan_tip,
    render_summary,
    render_topbar,
)

# Configure the Streamlit page title, icon, layout, and sidebar behavior.
st.set_page_config(
    page_title="PesoLens ₱1000 Scanner",
    page_icon="₱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
# These helper functions initialize and control state variables used across Streamlit reruns.

def init_state() -> None:
    """Initialize session state defaults when the app first loads."""
    defaults = {
        "confidence": DEFAULT_CONFIDENCE,
        "last_summary": None,
        "last_image": None,
        "last_annotated": None,
        "history": [],
        "model_status_toast": None,
        "active_upload_id": None,
        "force_scan_page": False,
        "upload_widget_key": 0,
        "camera_widget_key": 0,
        "detection_mode": "Image Upload Detection",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_scan(
    clear_upload: bool = False,
    clear_camera: bool = False,
    clear_upload_marker: bool = False,
) -> None:
    """Clear scan results and optionally reset upload/camera widgets."""
    st.session_state.last_summary = None
    st.session_state.last_image = None
    st.session_state.last_annotated = None
    st.session_state.active_upload_id = None

    if clear_upload_marker:
        clear_upload = True

    if clear_upload:
        st.session_state.upload_widget_key = st.session_state.get("upload_widget_key", 0) + 1

    if clear_camera:
        st.session_state.camera_widget_key = st.session_state.get("camera_widget_key", 0) + 1


def handle_detection_mode_change() -> None:
    """Reset scan state whenever the user switches between upload and camera detection."""
    reset_scan(clear_upload=True, clear_camera=True)


def get_query_value(key: str) -> str | None:
    """Return the first value for a query parameter key."""
    value = st.query_params.get(key)

    if isinstance(value, list):
        return value[0] if value else None

    return value


def handle_url_actions() -> None:
    """Handle special URL actions such as forcing a new scan page."""
    if get_query_value("new_scan") == "1":
        reset_scan(clear_upload=True, clear_camera=True)
        st.session_state.detection_mode = "Image Upload Detection"
        st.session_state["nav_radio"] = "Scan"
        st.session_state.force_scan_page = True
        st.query_params.clear()
        st.rerun()


def image_to_bytes(image: Image.Image) -> bytes:
    """Convert a PIL image to PNG bytes for download buttons."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def resize_image_for_display(
    image: Image.Image,
    max_width: int = 900,
    max_height: int = 650,
) -> Image.Image:
    """Resize an image for display, preserving aspect ratio and fitting the preview size."""
    display_image = image.copy()
    display_image.thumbnail((max_width, max_height))
    return display_image


def process_image(image: Image.Image, mode: str) -> None:
    """Run detection on the image, then save summary, annotated output, and history."""
    summary, annotated = run_detection(image, confidence=float(st.session_state.confidence))

    st.session_state.last_summary = summary
    st.session_state.last_image = image
    st.session_state.last_annotated = annotated
    st.session_state.history.insert(0, summary.to_history_row(mode))


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
# The app sidebar contains page navigation and scan tips.
def sidebar() -> str:
    with st.sidebar:
        render_brand()

        st.markdown("<div class='sidebar-menu-label'>Menu</div>", unsafe_allow_html=True)

        pages = ["Scan", "History", "How It Works", "About System", "User Guide", "Settings"]

        if st.session_state.get("force_scan_page", False):
            st.session_state["nav_radio"] = "Scan"
            st.session_state["force_scan_page"] = False

        page = st.radio(
            "Navigation",
            pages,
            format_func=lambda item: item,
            key="nav_radio",
            label_visibility="collapsed",
        )

        render_scan_tip()

        return page


# -----------------------------------------------------------------------------
# Scan page
# -----------------------------------------------------------------------------
# Primary scan page functions for choosing mode and performing detection.
def render_detection_mode_selector() -> str:
    """Render the detection mode radio selector for upload or camera scanning."""
    options = ["Image Upload Detection", "Camera/Webcam Detection"]

    if st.session_state.get("detection_mode") not in options:
        st.session_state.detection_mode = "Image Upload Detection"

    st.markdown("<div class='section-title compact-title'>Detection Mode</div>", unsafe_allow_html=True)

    mode = st.radio(
        "Detection mode selector",
        options,
        horizontal=True,
        key="detection_mode",
        label_visibility="collapsed",
        help="Choose whether to upload an image or capture a webcam snapshot.",
        on_change=handle_detection_mode_change,
        format_func=lambda item: {
            "Image Upload Detection": "Image Upload Detection\nUpload an image of the bill(s)",
            "Camera/Webcam Detection": "Camera/Webcam Detection\nTake a picture using your camera",
        }[item],
    )

    return mode or "Image Upload Detection"


def scan_page() -> None:
    """Render the main Scan page including model status and mode selection."""
    render_topbar()

    model = load_yolo_model()
    model_status = "ready" if model is not None else "missing"

    if st.session_state.model_status_toast != model_status:
        render_floating_model_notification(model is not None)
        st.session_state.model_status_toast = model_status

    mode = render_detection_mode_selector()

    if mode == "Image Upload Detection":
        upload_detection()
    else:
        camera_detection()

    render_breakdown(st.session_state.last_summary)


def upload_detection() -> None:
    """Render the image upload scan flow and handle image analysis."""
    st.markdown("<div class='mini-label'>Image Upload Detection</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of old or new Philippine ₱1000 bill/s.",
        key=f"upload_file_{st.session_state.upload_widget_key}",
    )

    if uploaded_file is None and st.session_state.last_summary is None:
        render_empty_state()
        return

    if uploaded_file is not None:
        upload_id = f"{uploaded_file.name}-{uploaded_file.size}-{uploaded_file.type}"

        if st.session_state.active_upload_id != upload_id:
            reset_scan()
            st.session_state.active_upload_id = upload_id

        image = Image.open(uploaded_file).convert("RGB")

        left, right = st.columns([0.58, 0.42], gap="large")

        with left:
            st.markdown("<div class='section-title'>Uploaded Image Preview</div>", unsafe_allow_html=True)

            preview_image = resize_image_for_display(image, max_width=760, max_height=480)
            st.image(preview_image, width=preview_image.width)

            c1, c2 = st.columns(2)

            with c1:
                analyze = st.button("Analyze Image", use_container_width=True)

            with c2:
                clear = st.button("Reset", use_container_width=True)

            if clear:
                reset_scan(clear_upload=True)
                st.rerun()

            if analyze:
                with st.spinner("Analyzing ₱1000 bill image…"):
                    try:
                        process_image(image, "Image Upload Detection")
                    except FileNotFoundError:
                        st.error("Model file is missing. Please add your trained model inside the models folder.")
                        return

                st.rerun()

        with right:
            st.markdown("<div class='section-title'>Detection Result Summary</div>", unsafe_allow_html=True)

            if st.session_state.last_summary is None:
                st.info("Uploaded image is ready. Click Analyze Image to scan.")
            else:
                summary = st.session_state.last_summary

                if summary.total_bills == 0:
                    st.warning(summary.message)
                else:
                    st.success(summary.message)

                render_summary(summary)

                if st.session_state.last_annotated is not None:
                    st.download_button(
                        "Download Output Image",
                        data=image_to_bytes(st.session_state.last_annotated),
                        file_name="pesolens_detection_result.png",
                        mime="image/png",
                        use_container_width=True,
                    )

    if st.session_state.last_annotated is not None:
        st.markdown("<div class='section-title'>Result Preview Area</div>", unsafe_allow_html=True)

        result_image = resize_image_for_display(
            st.session_state.last_annotated,
            max_width=900,
            max_height=650,
        )
        st.image(
            result_image,
            caption="Output image with bounding boxes",
            width=result_image.width,
        )


def camera_detection() -> None:
    """Render the camera capture scan flow and handle image analysis."""
    st.markdown("<div class='mini-label'>Camera/Webcam Detection</div>", unsafe_allow_html=True)
    st.info("Allow camera permission, take a snapshot, then click Analyze Captured Image.")

    camera_file = st.camera_input(
        "Take a picture",
        key=f"camera_input_{st.session_state.camera_widget_key}",
    )

    if camera_file is None and st.session_state.last_summary is None:
        render_empty_state()
        return

    if camera_file is not None:
        image = Image.open(camera_file).convert("RGB")

        left, right = st.columns([0.58, 0.42], gap="large")

        with left:
            st.markdown("<div class='section-title'>Camera Snapshot Preview</div>", unsafe_allow_html=True)

            preview_image = resize_image_for_display(image, max_width=760, max_height=480)
            st.image(preview_image, width=preview_image.width)

            c1, c2 = st.columns(2)

            with c1:
                analyze = st.button("Analyze Captured Image", use_container_width=True)

            with c2:
                clear = st.button("Reset", use_container_width=True)

            if clear:
                reset_scan(clear_camera=True)
                st.rerun()

            if analyze:
                with st.spinner("Analyzing camera image…"):
                    try:
                        process_image(image, "Camera/Webcam Detection")
                    except FileNotFoundError:
                        st.error("Model file is missing. Please add your trained model inside the models folder.")
                        return

                st.rerun()

        with right:
            st.markdown("<div class='section-title'>Detection Result Summary</div>", unsafe_allow_html=True)

            if st.session_state.last_summary is None:
                st.info("Captured image is ready. Click Analyze Captured Image to scan.")
            else:
                summary = st.session_state.last_summary

                if summary.total_bills == 0:
                    st.warning(summary.message)
                else:
                    st.success(summary.message)

                render_summary(summary)

                if st.session_state.last_annotated is not None:
                    st.download_button(
                        "Download Output Image",
                        data=image_to_bytes(st.session_state.last_annotated),
                        file_name="pesolens_camera_detection_result.png",
                        mime="image/png",
                        use_container_width=True,
                    )

    if st.session_state.last_annotated is not None:
        st.markdown("<div class='section-title'>Result Preview Area</div>", unsafe_allow_html=True)

        result_image = resize_image_for_display(
            st.session_state.last_annotated,
            max_width=900,
            max_height=650,
        )
        st.image(
            result_image,
            caption="Camera output image with bounding boxes",
            width=result_image.width,
        )


# -----------------------------------------------------------------------------
# Other pages
# -----------------------------------------------------------------------------
# Secondary app pages for history, help, system info, user guidance, and settings.
def history_page() -> None:
    """Render the scan history page to review past detections."""
    render_topbar()
    st.markdown("<div class='section-title'>Scan History</div>", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            """
            <div class="soft-panel">
                <h3>No scan history yet.</h3>
                <p>Analyze an uploaded image or camera snapshot to see history here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()


def how_it_works_page() -> None:
    """Render the How It Works page to explain the scanning workflow."""
    render_topbar()
    st.markdown("<div class='section-title'>How It Works</div>", unsafe_allow_html=True)

    steps = [
        ("1", "Upload or Capture", "Upload an image or take a webcam snapshot of the bill."),
        ("2", "AI Scanning", "PesoLens scans the image using a trained YOLOv8 detection model."),
        ("3", "Bill Detection", "The system looks for visible Philippine ₱1000 bills in the image."),
        ("4", "Bill Classification", "Each detected bill is classified as an old or new ₱1000 bill."),
        ("5", "Counting", "The system counts old bills, new bills, and total detected bills."),
        ("6", "Amount Computation", "The total count is multiplied by ₱1,000 to compute the total amount."),
    ]

    for start in range(0, len(steps), 3):
        cols = st.columns(3)

        for col, (num, title, desc) in zip(cols, steps[start : start + 3]):
            with col:
                st.markdown(
                    f"""
                    <div class="guide-card">
                        <div class="status-pill">Step {num}</div>
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def about_system_page() -> None:
    """Render the About System page that describes the app and model status."""
    render_topbar()
    st.markdown("<div class='section-title'>About System</div>", unsafe_allow_html=True)

    model = load_yolo_model()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="soft-panel">
                <h3>System Purpose</h3>
                <p>PesoLens is an AI-powered scanner designed to detect and classify Philippine ₱1000 bills.</p>
                <p>It identifies whether detected bills are old or new ₱1000 banknotes.</p>
                <p>It can also count multiple detected bills and compute the total monetary amount.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="soft-panel">
                <h3>System Outputs</h3>
                <p><strong>Detection:</strong> Bounding boxes around detected bills</p>
                <p><strong>Classification:</strong> Old bill or new bill</p>
                <p><strong>Counting:</strong> Old, new, and total ₱1000 bills</p>
                <p><strong>Computation:</strong> Total monetary amount</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-title'>Model Status</div>", unsafe_allow_html=True)

    if model is None:
        st.error("Model status: Not loaded.")
    else:
        st.success("Model status: Ready.")

        with st.expander("View model class names"):
            st.json(get_model_class_names(model))


def user_guide_page() -> None:
    """Render the user guide with tips and troubleshooting advice."""
    render_topbar()
    st.markdown("<div class='section-title'>User Guide</div>", unsafe_allow_html=True)

    tips = [
        ("Use clear images", "Make sure the bill is visible and not too blurry."),
        ("Use good lighting", "Bright and even lighting improves detection."),
        ("Avoid covered bills", "Folded or hidden bills may be harder to detect."),
        ("Capture the full bill", "Keep the bill inside the frame as much as possible."),
        ("Check the result", "Review the result preview and detection summary after scanning."),
        ("Adjust only when needed", "Use Settings only if the scanner misses bills or detects incorrectly."),
    ]

    for start in range(0, len(tips), 3):
        cols = st.columns(3)

        for col, (title, desc) in zip(cols, tips[start : start + 3]):
            with col:
                st.markdown(
                    f"""
                    <div class="guide-card">
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div class='section-title'>Troubleshooting</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="soft-panel">
            <p><strong>No bill detected:</strong> Try using a clearer image, better lighting, or a closer view of the bill.</p>
            <p><strong>Wrong count:</strong> Make sure all bills are visible and not heavily covered or overlapping.</p>
            <p><strong>Camera not opening:</strong> Allow browser camera permission and refresh the page.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def settings_page() -> None:
    """Render app settings so the user can adjust detection confidence."""
    render_topbar()
    st.markdown("<div class='section-title'>Settings</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="soft-panel">
            <h3>Confidence Threshold</h3>
            <p>This controls how strict the scanner is when accepting detections.</p>
            <p>Lower values may detect more bills but can increase false detections. Higher values are stricter but may miss unclear bills.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state.confidence = st.slider(
        "Confidence threshold",
        min_value=0.10,
        max_value=0.95,
        value=float(st.session_state.confidence),
        step=0.05,
        help="Lower = more detections but more false positives. Higher = stricter detections.",
    )

    st.info(f"Current confidence threshold: {st.session_state.confidence:.2f}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
# Entry point for the app. Initializes styles, state, URL actions, and page rendering.
def main() -> None:
    apply_css()
    init_state()
    handle_url_actions()

    selected_page = sidebar()

    if selected_page == "Scan":
        scan_page()
    elif selected_page == "History":
        history_page()
    elif selected_page == "How It Works":
        how_it_works_page()
    elif selected_page == "About System":
        about_system_page()
    elif selected_page == "User Guide":
        user_guide_page()
    elif selected_page == "Settings":
        settings_page()


if __name__ == "__main__":
    main()