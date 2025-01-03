import cv2
from pathlib import Path
from utils.validation import valid_license_plate_format

def save_detected_plates(frame, results, output_dir='detected_plates', method='unknown', base_filename="unknown"):
    """Save detected license plate regions as individual image files."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for i, box in enumerate(results.boxes):
        # Get bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cropped = frame[y1:y2, x1:x2]

        # Generate unique filename using base_filename and method
        stem = Path(base_filename).stem
        filename = f"{stem}_{method}_plate_{i}.jpg"
        filepath = str(Path(output_dir) / filename)
        
        # Save the cropped image
        cv2.imwrite(filepath, cropped)
        saved_files.append(filepath)
    
    return saved_files

def write_results(file, frame_count, plates, method):
    if plates:
        output_line = f"Detected license plates ({method}) in frame {frame_count}:"
        print(output_line)
        file.write(output_line + '\n') 
        for plate in plates:
            output_line = plate + (" (valid plate)" if valid_license_plate_format(plate) else " (invalid plate)")
            print(output_line) 
            file.write(output_line + '\n')
    else:
        output_line = f"No license plates detected in frame {frame_count}."
        print(f"No license plates detected.")
        file.write(output_line + '\n')

    print()
    file.write('\n')