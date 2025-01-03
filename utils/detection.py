import cv2
from pathlib import Path
import pytesseract
import easyocr
from ultralytics import YOLO
from utils.file_utils import save_detected_plates, write_results
from utils.validation import valid_license_plate_format
from utils.preprocessing import preprocess_for_ocr

# Initialize models
YOLO_MODEL_PATH = 'yolov8s.pt'
LICENSE_PLATE_MODEL_PATH = 'license_plate_detector.pt'
yolo_model = YOLO(YOLO_MODEL_PATH)
license_plate_detector = YOLO(LICENSE_PLATE_MODEL_PATH)

# Initialize OCR readers
reader = easyocr.Reader(['en'])

RESULTS_DIR = 'results/'

def process_video(video_path, method='easyocr'):
    """
    Process a video, detect license plates, and save results to a file.
    Output file will be named {video_name}_output.txt in the same directory as the video.
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    # Create output file path using video name
    output_file = RESULTS_DIR + Path(video_path).stem + "_result.txt"
    
    # Open file in write mode
    with open(output_file, 'w') as file:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            base_filename = f"{Path(video_path).stem}_frame_{frame_count}"
            plates = detect_license_plates(frame, method=method, base_filename=base_filename)

            write_results(file, frame_count, plates, method)

    cap.release()
    completion_msg = "Processing completed. Results saved to " + output_file
    print(completion_msg)
    with open(output_file, 'a') as f:
        f.write("\n" + completion_msg)

def process_image(image_path, method='easyocr'):
    """Process a single image and print detected license plates."""
    frame = cv2.imread(image_path)
    if frame is None:
        print("Invalid image path.")
        return

    plates = detect_license_plates(frame, method=method, base_filename=image_path)

    # Create output file path using video name
    output_file = RESULTS_DIR + Path(image_path).stem + "_result.txt"
    
    # Open file in write mode
    with open(output_file, 'w') as file:
        write_results(file, "1", plates, method)

def detect_license_plates(frame, method='easyocr', base_filename="unknown"):
    """Detect license plates in a frame and extract text.
    
    Args:
        frame: The input image frame
        method: OCR method to use ('tesseract' or 'easyocr')
        base_filename: Base name to use for saving detected regions
    
    Returns:
        List of detected license plate texts
    """
    # Detect license plates using the specialized model
    results = license_plate_detector(frame)[0]

    saved_files = save_detected_plates(frame, results, method=method, base_filename=base_filename)
    if saved_files:
        print(f"Saved {len(saved_files)} detected regions to ./detected_plates/")
        for file in saved_files:
            print(f"  - {file}")
    
    plates = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cropped = frame[y1:y2, x1:x2]
        
        gray, thresh = preprocess_for_ocr(cropped)

        plate_text = ''
        if method.lower() == 'tesseract':
            plate_text = pytesseract.image_to_string(thresh, config='--psm 8').strip()
        elif method.lower() == 'easyocr':
            results = reader.readtext(thresh)
            for _, text, conf in results:
                plate_text = text.upper().replace(' ', '')
                if valid_license_plate_format(plate_text):
                    break
        else:
            raise ValueError(f"Unsupported OCR method: {method}")

        if plate_text != '':
            plates.append(plate_text)

    return plates