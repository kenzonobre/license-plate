# License Plate Detection CLI Tool

## Overview
This project provides a Command-Line Interface (CLI) tool to detect license plates in videos and images. The detection pipeline leverages YOLO for license plate detection and OCR tools (EasyOCR or Tesseract) for character recognition. The tool is designed to identify license plates and output the results in a structured format.

---

## Features
- Detect license plates from images and videos.
- Support for OCR methods: **EasyOCR** (default) and **Tesseract**.
- Save detected license plate images and corresponding text outputs.
- Validate license plates against Brazilian formats.
- Generate detailed result files for easy review.

---

## Installation
### Prerequisites
Ensure you have the following installed:
1. **Python 3.8 or later**
2. **pip** (Python package manager)
3. **Tesseract-OCR** (if using Tesseract as the OCR method)

To install Tesseract:
- **Ubuntu**:
  ```bash
  sudo apt update && sudo apt install tesseract-ocr
  ```
- **MacOS** (using Homebrew):
  ```bash
  brew install tesseract
  ```
- **Windows**:
  Download and install Tesseract from the official website: https://github.com/tesseract-ocr/tesseract

### Project Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
### Running the CLI Tool
The CLI offers two commands: `video` for processing videos and `frame` for processing single images.

### Commands and Options
#### Process a Video
```bash
python main.py video <video_path> --method <method>
```
- **`video_path`**: Path to the video file.
- **`--method`** (optional): OCR method to use (`easyocr` or `tesseract`). Defaults to `easyocr`.

Example:
```bash
python main.py video videos/video1.mp4 --method easyocr
```

#### Process an Image
```bash
python main.py frame <image_path> --method <method>
```
- **`image_path`**: Path to the image file.
- **`--method`** (optional): OCR method to use (`easyocr` or `tesseract`). Defaults to `easyocr`.

Example:
```bash
python main.py frame images/image7.jpg --method easyocr
```

---

## Handling Issues on CPU-Only Systems
If you do not have a GPU, you may encounter errors related to CUDA libraries. To resolve these issues, ensure you install the CPU-only version of PyTorch.

### Steps for CPU-Only Setup:
1. Uninstall the existing PyTorch installation:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip cache purge
   ```
2. Install the CPU-only version of PyTorch:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```
3. Verify PyTorch installation:
   ```python
   import torch
   print(torch.__version__)
   print(torch.cuda.is_available())  # Should return False
   ```
4. Reinstall `easyocr` to ensure compatibility:
   ```bash
   pip install easyocr
   ```
5. Test your script again:
   ```bash
   python main.py frame images/7
   ```

---

## Results
- **License plate detections** are saved in the `results/` directory as text files named `<input_file_stem>_result.txt`.
- **Detected regions** of license plates are saved as individual images in the `detected_plates/` directory.

---

## Project Structure
```
.
├── main.py                # Entry point for the CLI tool
├── requirements.txt       # Project dependencies
├── utils
│   ├── detection.py       # Core detection logic
│   ├── file_utils.py      # Functions for file saving and result handling
│   ├── preprocessing.py   # Image preprocessing utilities
│   ├── validation.py      # License plate format validation
├── yolov8s.pt             # YOLO model weights (general detection)
├── license_plate_detector.pt # License plate-specific YOLO model weights
└── detected_plates/       # Directory for cropped plate images
└── results/               # Directory for output results
```

---

## Requirements
Here are the Python dependencies required for the project:

```txt
opencv-python
click
pytesseract
easyocr
ultralytics
```

Install them using:
```bash
pip install -r requirements.txt
```

---

## Notes
- **YOLO Model Weights**: Place `yolov8s.pt` and `license_plate_detector.pt` in the project root directory before running the tool.
- **Output Directories**: Ensure the directories `results/` and `detected_plates/` exist or are created automatically during runtime.

