import cv2
from ultralytics import YOLO

# Load the pretrained YOLOv8 model
model = YOLO("yolov8n.pt")  # You can also try yolov8s.pt, yolov8m.pt, etc.

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = model(frame)

    # Visualize results on frame
    annotated_frame = results[0].plot()

    # Display the output
    cv2.imshow("Elephant Live View 🐘📷", annotated_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
