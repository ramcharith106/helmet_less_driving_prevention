Helmet Detection System 🚀
Overview
The Helmet Detection System is an AI-powered solution designed to detect helmet-less riders and capture their license plates for further action. Using YOLOv8 for object detection and EasyOCR for text recognition, the system ensures real-time monitoring and automatic number plate recognition (ANPR).

Features
✅ Real-time Helmet Detection (Detects riders without helmets)
✅ Automatic Number Plate Recognition (ANPR) using OCR
✅ Works with CCTV, webcams, or pre-recorded videos
✅ Lightweight & optimized for Raspberry Pi / Jetson Nano

How It Works
The system detects a person riding a motorcycle.
It checks if the rider is wearing a helmet.
If no helmet is detected, it captures the license plate.
The system logs the detected number plate for further processing.

1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/helmet_detection.git
cd helmet_detection
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Run the Detection System
bash
Copy
Edit
python main.py
Demo Video & Screenshots
(Add a GIF or Image of your system in action!)

Technologies Used
🖥️ YOLOv8 - Helmet Detection
🔤 EasyOCR - License Plate Recognition
📸 OpenCV - Image Processing
🐍 Python - Backend

Contributing
Want to improve this project? Fork, star ⭐, and contribute! Open an issue or submit a pull request.

License
🔓 This project is open-source under the MIT License.

