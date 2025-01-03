import cv2

def preprocess_for_ocr(plate_img):
    """
    Preprocess the license plate image for better OCR accuracy.
    """
    # Resize if too small
    min_height = 100
    height, width = plate_img.shape[:2]
    if height < min_height:
        scale = min_height / height
        plate_img = cv2.resize(plate_img, (int(width * scale), min_height))

    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    # Thresholding (using adaptive threshold instead of simple binary)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    
    return gray, thresh 