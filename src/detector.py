"""YOLOv8 detection logic for the PesoLens ₱1000 Bill Scanner."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

BILL_VALUE = 1000
DEFAULT_CONFIDENCE = 0.75
MODEL_PATH = Path("models/trained_model_100_epoch.pt")

# These names should match your Roboflow/YOLO data.yaml classes.
OLD_CLASS_KEYWORDS = ("1000_old", "1000_olds", "old_1000", "old")
NEW_CLASS_KEYWORDS = ("1000_new", "1000_news", "new_1000", "new")


@dataclass
class DetectionItem:
    bill_type: str
    class_name: str
    confidence: float
    box: Tuple[int, int, int, int]


@dataclass
class DetectionSummary:
    old_count: int
    new_count: int
    total_bills: int
    total_amount: int
    average_confidence: float
    status: str
    message: str
    scan_time: str
    detections: List[DetectionItem]

    def to_history_row(self, mode: str) -> Dict[str, str]:
        return {
            "Mode": mode,
            "Old Bills": str(self.old_count),
            "New Bills": str(self.new_count),
            "Total Bills": str(self.total_bills),
            "Total Amount": f"₱{self.total_amount:,}",
            "Confidence": f"{self.average_confidence * 100:.2f}%",
            "Status": self.status,
            "Date/Time": self.scan_time,
        }

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["detections"] = [asdict(item) for item in self.detections]
        return data


@st.cache_resource(show_spinner=False)
def load_yolo_model(model_path: str = str(MODEL_PATH)) -> Optional[YOLO]:
    """Load and cache the trained YOLOv8 model."""
    path = Path(model_path)

    if not path.exists():
        return None

    try:
        return YOLO(str(path))
    except Exception:
        return None


def get_model_class_names(model: Optional[YOLO]) -> Dict[int, str]:
    """Return model class names as a dictionary."""
    if model is None:
        return {}

    names = getattr(model, "names", {}) or {}

    if isinstance(names, dict):
        return {int(k): str(v) for k, v in names.items()}

    if isinstance(names, list):
        return {i: str(v) for i, v in enumerate(names)}

    return {}


def _normalize(text: str) -> str:
    return text.lower().strip().replace("-", "_").replace(" ", "_")


def classify_bill(class_id: int, class_name: str) -> str:
    """Classify a detected YOLO class as old, new, or unknown."""
    normalized = _normalize(class_name)

    if any(keyword in normalized for keyword in OLD_CLASS_KEYWORDS):
        return "old"

    if any(keyword in normalized for keyword in NEW_CLASS_KEYWORDS):
        return "new"

    # Fallback for the current dataset order: 0 = 1000_new, 1 = 1000_old.
    if class_id == 0:
        return "new"

    if class_id == 1:
        return "old"

    return "unknown"


def run_detection(image: Image.Image, confidence: float) -> Tuple[DetectionSummary, Image.Image]:
    """Run YOLOv8 detection and return the detection summary plus annotated image."""
    model = load_yolo_model()

    if model is None:
        raise FileNotFoundError("Model file not found.")

    image_rgb = image.convert("RGB")

    results = model.predict(
        source=image_rgb,
        conf=confidence,
        imgsz=640,
        verbose=False,
    )

    detections = _extract_detections(results)
    summary = _build_summary(detections)
    annotated_image = draw_detections(image_rgb, detections)

    return summary, annotated_image


def _extract_detections(results: List[Any]) -> List[DetectionItem]:
    detections: List[DetectionItem] = []

    for result in results:
        boxes = getattr(result, "boxes", None)

        if boxes is None or len(boxes) == 0:
            continue

        names = getattr(result, "names", {}) or {}

        if isinstance(names, list):
            names = {i: name for i, name in enumerate(names)}

        for box in boxes:
            class_id = int(box.cls[0].item())
            class_name = str(names.get(class_id, class_id))
            bill_type = classify_bill(class_id, class_name)
            detection_confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]

            if bill_type not in {"old", "new"}:
                continue

            detections.append(
                DetectionItem(
                    bill_type=bill_type,
                    class_name=class_name,
                    confidence=detection_confidence,
                    box=(x1, y1, x2, y2),
                )
            )

    return detections


def _build_summary(detections: List[DetectionItem]) -> DetectionSummary:
    old_count = sum(1 for item in detections if item.bill_type == "old")
    new_count = sum(1 for item in detections if item.bill_type == "new")
    total_bills = old_count + new_count
    total_amount = total_bills * BILL_VALUE

    average_confidence = float(np.mean([item.confidence for item in detections])) if detections else 0.0
    scan_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    if total_bills == 0:
        status = "No ₱1000 Bill Detected"
        message = "No Philippine ₱1000 bill detected. Please try a clearer image or another angle."
    elif total_bills == 1 and old_count == 1:
        status = "Old ₱1000 Bill Detected"
        message = "One old Philippine ₱1000 bill was detected."
    elif total_bills == 1 and new_count == 1:
        status = "New ₱1000 Bill Detected"
        message = "One new Philippine ₱1000 bill was detected."
    else:
        status = "Multiple ₱1000 Bills Detected"
        message = f"{total_bills} Philippine ₱1000 bills were detected and counted."

    return DetectionSummary(
        old_count=old_count,
        new_count=new_count,
        total_bills=total_bills,
        total_amount=total_amount,
        average_confidence=average_confidence,
        status=status,
        message=message,
        scan_time=scan_time,
        detections=detections,
    )


def _get_font(size: int = 18) -> ImageFont.ImageFont:
    for font_name in ("DejaVuSans-Bold.ttf", "Arial.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue

    return ImageFont.load_default()


def draw_detections(image: Image.Image, detections: List[DetectionItem]) -> Image.Image:
    """Draw custom bounding boxes and labels on a PIL image."""
    output = image.convert("RGB").copy()
    draw = ImageDraw.Draw(output)

    width, height = output.size
    box_width = max(3, int(min(width, height) / 180))
    label_font = _get_font(max(14, int(min(width, height) / 45)))

    for item in detections:
        x1, y1, x2, y2 = item.box

        if item.bill_type == "old":
            color = (220, 53, 69)
            bill_label = "Old ₱1000 Bill"
        else:
            color = (37, 111, 230)
            bill_label = "New ₱1000 Bill"

        label = f"{bill_label} {item.confidence * 100:.1f}%"

        draw.rectangle((x1, y1, x2, y2), outline=color, width=box_width)

        text_bbox = draw.textbbox((x1, y1), label, font=label_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        padding = 8
        label_y = max(0, y1 - text_height - (padding * 2))

        draw.rounded_rectangle(
            (x1, label_y, x1 + text_width + padding * 2, label_y + text_height + padding * 2),
            radius=6,
            fill=color,
        )

        draw.text(
            (x1 + padding, label_y + padding),
            label,
            fill=(255, 255, 255),
            font=label_font,
        )

    return output