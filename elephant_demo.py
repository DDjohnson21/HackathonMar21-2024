import streamlit as st
import cv2
from PIL import Image, ImageDraw
import numpy as np
from ultralytics import YOLO
import time

# Set page configuration
st.set_page_config(page_title="🐘 Elephant – Assistive AI for Independent Living", layout="wide")

# Initialize session state for storing items and privacy mode.
# Items can be either a location string (from "Teach Elephant") or a dict with training coordinates (from "Add New Item").
if "items" not in st.session_state:
    st.session_state.items = {"keys": "on the living room table", "remote": "on the couch"}
if "privacy_mode" not in st.session_state:
    st.session_state.privacy_mode = False

# Sidebar navigation for multiple modes
page = st.sidebar.radio("Navigate", ["Ask Elephant", "Live Detection", "Add New Item", "Emergency"])

# --------------------- Ask Elephant Page ---------------------
if page == "Ask Elephant":
    st.title("🐘 Elephant – Assistive AI for Independent Living")
    
    st.subheader("1. 🔍 Ask Elephant where something is")
    query = st.text_input("Ask: Where is my...", placeholder="e.g. keys, remote", key="query")
    if query:
        item = query.lower().strip()
        if item in st.session_state.items:
            # If stored value is a dict, show its bounding box info; otherwise, assume a location string.
            value = st.session_state.items[item]
            if isinstance(value, dict):
                st.success(f"Your {item} is trained with bounding box info: {value}.")
            else:
                st.success(f"Your {item} is {value}.")
        else:
            st.warning(f"Elephant doesn't know where your {item} is yet.")
    
    st.divider()
    
    st.subheader("2. 🧠 Teach Elephant a New Item (Simple)")
    uploaded = st.file_uploader("Upload a photo of the item (optional)", key="teach_uploader")
    new_item = st.text_input("Give it a name (e.g. glasses, book)", key="teach_name")
    location = st.text_input("Where is it right now? (e.g. on the shelf)", key="teach_location")
    if st.button("Add to Memory (Simple)"):
        if new_item and location:
            st.session_state.items[new_item.lower()] = location
            st.success(f"Saved: '{new_item}' is {location}.")
        else:
            st.error("Please enter both a name and a location.")
    
    st.divider()
    
    st.subheader("3. 🛡️ Privacy Mode")
    st.session_state.privacy_mode = st.checkbox("Enable privacy mode (unauthorized access)", value=st.session_state.privacy_mode)
    if st.session_state.privacy_mode:
        st.warning("Privacy mode is ON. Camera feed hidden.")
        st.image("https://via.placeholder.com/600x400/000000/FFFFFF?text=CAMERA+BLOCKED")
    else:
        try:
            base_img = Image.open("https://i.imgur.com/YZ6RvZC.jpg")
        except Exception as e:
            st.error("Failed to load demo image.")
            base_img = None
        if base_img:
            draw = ImageDraw.Draw(base_img)
            draw.rectangle([100, 200, 250, 300], outline="red", width=4)
            draw.text((100, 180), "keys", fill="red")
            draw.rectangle([300, 350, 420, 420], outline="blue", width=4)
            draw.text((300, 330), "remote", fill="blue")
            st.image(base_img, caption="Simulated object recognition with bounding boxes")
    
    st.divider()
    
    st.subheader("Stored Items")
    st.json(st.session_state.items)

# --------------------- Live Detection Page ---------------------
elif page == "Live Detection":
    st.title("🐘 Elephant – Live Camera Object Detection")
    st.subheader("Activate your webcam to detect objects in real time.")
    run = st.checkbox("Start Camera", key="live_run")
    FRAME_WINDOW = st.image([])
    
    # Load YOLO model (it loads once when this page is selected)
    model = YOLO('yolov8n.pt')
    
    cap = None
    if run:
        cap = cv2.VideoCapture(0)
    
    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame.")
            break
        results = model(frame, stream=True)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    if cap:
        cap.release()

# --------------------- Add New Item (Training) Page ---------------------
elif page == "Add New Item":
    st.title("🐘 Elephant – Train on a New Item")
    st.subheader("Upload an image and specify a bounding box to train Elephant on a new item.")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="train_uploader")
    if uploaded_file:
        img = Image.open(uploaded_file).convert('RGB')
        img_np = np.array(img)
        st.image(img_np, caption="Uploaded Image", use_column_width=True)
        
        name = st.text_input("Enter the name of the object", key="train_name")
        x = st.number_input("X (left)", min_value=0, max_value=img_np.shape[1]-1, value=50, key="train_x")
        y_val = st.number_input("Y (top)", min_value=0, max_value=img_np.shape[0]-1, value=50, key="train_y")
        w = st.number_input("Width", min_value=1, max_value=img_np.shape[1]-int(x), value=100, key="train_w")
        h = st.number_input("Height", min_value=1, max_value=img_np.shape[0]-int(y_val), value=100, key="train_h")
        
        if st.button("Save Item (Training)"):
            if name:
                # Save the training item as a dictionary of bounding box coordinates.
                st.session_state.items[name.lower()] = {'x': int(x), 'y': int(y_val), 'w': int(w), 'h': int(h)}
                st.success(f"Saved '{name}' at ({x}, {y_val}, {w}, {h})")
            else:
                st.error("Please enter a name for the item.")
        
        # Draw bounding box preview
        preview = img_np.copy()
        cv2.rectangle(preview, (int(x), int(y_val)), (int(x + w), int(y_val + h)), (255, 0, 0), 2)
        st.image(preview, caption=f"Preview with box for '{name}'", use_column_width=True)
    
    with st.expander("Stored Items"):
        st.json(st.session_state.items)

# --------------------- Emergency Page ---------------------
elif page == "Emergency":
    st.title("🐘 Elephant – Emergency Fall Detection (Simulated)")
    st.subheader("Simulate a fall to alert your caregiver.")
    if st.button("Simulate Fall"):
        st.error("⚠️ Fall detected! Notifying emergency contact...")
        time.sleep(2)
        st.success("✅ Alert sent to caregiver.")
