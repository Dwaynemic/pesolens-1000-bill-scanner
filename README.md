# Philippine ₱1000 Bill Detection and Classification System

A Streamlit + YOLOv8 web application for detecting, classifying, counting, and computing the total amount of Philippine ₱1000 bills.

## Features

- Detects Philippine ₱1000 bills
- Classifies detected bills as old ₱1000 bill or new ₱1000 bill
- Counts old bills and new bills
- Computes total bill count
- Computes total monetary amount
- Shows a clear message if no ₱1000 bill is detected
- Supports image upload detection
- Supports camera/webcam snapshot detection
- Includes scan history, model info, help guide, and advanced settings

## Required Model File

Put your trained YOLOv8 model here:

```text
models/best.pt
```

This is usually copied from your Colab training output:

```text
/content/runs/detect/philippine_1000/weights/best.pt
```

## Local Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Streamlit Community Cloud Deployment

1. Create a GitHub repository.
2. Upload these files and folders:
   - `streamlit_app.py`
   - `src/`
   - `models/best.pt`
   - `requirements.txt`
   - `.streamlit/config.toml`
3. In Streamlit Community Cloud, connect your GitHub account.
4. Choose your repository and set the main file path to:

```text
streamlit_app.py
```

5. Deploy and open the generated Streamlit link.

## Notes

- The confidence threshold is hidden from the main dashboard and placed under Advanced Settings.
- Camera support uses Streamlit's `st.camera_input`, which captures a camera snapshot for detection.
- For best results, use clear images with good lighting.
