import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
import easyocr
import os
from datetime import datetime
import xlwings as xw

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

def perform_ocr(image_array):
    if image_array is None or image_array.size == 0:
        return "ERROR"
    
    # Convert image to grayscale for better OCR accuracy
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray)
    
    detected_text = "".join([res[1] for res in results])
    return detected_text.strip()

# Load YOLOv8 model
model = YOLO("best.pt")
names = model.names

# Define full-screen polygon area
area = np.array([(0, 0), (1920, 0), (1920, 1080), (0, 1080)], np.int32)

# Create directory for current date
current_date = datetime.now().strftime('%Y-%m-%d')
os.makedirs(current_date, exist_ok=True)

# Initialize Excel file
excel_file_path = os.path.join(current_date, f"{current_date}.xlsx")
if os.path.exists(excel_file_path):
    wb = xw.Book(excel_file_path)
else:
    wb = xw.Book()
    ws = wb.sheets[0]
    ws.range("A1").value = ["Number Plate", "Date", "Time"]

ws = wb.sheets[0]
processed_track_ids = set()

cap = cv2.VideoCapture("final.mp4")  # Read from video file

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model.track(frame, persist=True)

    no_helmet_detected = False
    numberplate_box = None
    numberplate_track_id = None

    if results and results[0].boxes:
        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        
        for box, class_id, track_id in zip(boxes, class_ids, track_ids):
            c = names[class_id]
            x1, y1, x2, y2 = box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if cv2.pointPolygonTest(area, (cx, cy), False) >= 0:
                if c == 'no-helmet':
                    no_helmet_detected = True
                elif c == 'numberplate':
                    numberplate_box = box
                    numberplate_track_id = track_id

        if no_helmet_detected and numberplate_box and numberplate_track_id not in processed_track_ids:
            x1, y1, x2, y2 = numberplate_box
            crop = frame[y1:y2, x1:x2] if y2 > y1 and x2 > x1 else None
            if crop is not None and crop.size > 0:
                crop = cv2.resize(crop, (120, 85))
                text = perform_ocr(crop)
                
                print(f"Detected Number Plate: {text}")
                
                current_time = datetime.now().strftime('%H-%M-%S-%f')[:12]
                crop_image_path = os.path.join(current_date, f"{text}_{current_time}.jpg")
                cv2.imwrite(crop_image_path, crop)
                
                last_row = ws.range("A" + str(ws.cells.last_cell.row)).end('up').row
                ws.range(f"A{last_row+1}").value = [text, current_date, current_time]
                
                processed_track_ids.add(numberplate_track_id)

    # Draw polygon area
    cv2.polylines(frame, [area], True, (255, 0, 255), 2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
wb.save(excel_file_path)
wb.close()
