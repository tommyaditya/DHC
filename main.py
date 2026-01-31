import cv2
import mediapipe as mp
import pyautogui
import math
import time
import os

# TASKS API imports
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Configuration
MODEL_PATH = 'hand_landmarker.task'
PINCH_THRESHOLD = 0.05  # Normalized distance threshold (0.05 is roughly 5% of screen width)

# Check if model exists
if not os.path.exists(MODEL_PATH):
    print(f"Error: Model file {MODEL_PATH} not found. Please run download_model.py")
    exit(1)

# Initialize Hand Landmarker
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    running_mode=vision.RunningMode.IMAGE) # Using IMAGE mode for synchronous simple usage

landmarker = vision.HandLandmarker.create_from_options(options)

# Open webcam
cap = cv2.VideoCapture(0)
# Set reliable resolution for performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# OPTIMIZATION: Remove PyAutoGUI default delay (0.1s) which causes lag
pyautogui.PAUSE = 0

is_pinched = False
previous_time = 0

print("Chrome Dino Hand Controller Started (Tasks API).")
print("Pinch your thumb and index finger to Jump (Space).")
print("Press 'q' to exit.")

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time) if previous_time > 0 else 0
        previous_time = current_time

        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)
        
        # Convert the BGR image to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        
        # Detect hands
        detection_result = landmarker.detect(mp_image)
        
        # Get hand landmarks
        hand_landmarks_list = detection_result.hand_landmarks
        
        if hand_landmarks_list:
            for hand_landmarks in hand_landmarks_list:
                # hand_landmarks is a list of NormalizedLandmark objects
                
                # Get coordinates of Thumb Tip (4) and Index Finger Tip (8)
                h, w, c = image.shape
                
                thumb_tip = hand_landmarks[4]
                index_tip = hand_landmarks[8]
                
                cx4, cy4 = int(thumb_tip.x * w), int(thumb_tip.y * h)
                cx8, cy8 = int(index_tip.x * w), int(index_tip.y * h)
                
                # Draw landmarks and skeleton (simple version)
                # Draw all 21 points
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (cx, cy), 3, (255, 0, 0), cv2.FILLED)
                
                # Draw pinch points larger
                cv2.circle(image, (cx4, cy4), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (cx8, cy8), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (cx4, cy4), (cx8, cy8), (255, 0, 255), 3)
                
                # Calculate center point
                cx_mid, cy_mid = (cx4 + cx8) // 2, (cy4 + cy8) // 2
                
                # Calculate distance (Euclidean distance on normalized coordinates can be more robust for scaling, 
                # but pixel distance is easier to visualize. Using Normalized here for thresholding logic)
                # Note: Normalized distance avoids issues with camera resolution changes, but aspect ratio matters.
                # Let's use simple euclidean on landmarks
                dist_normalized = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
                
                # Check for pinch
                if dist_normalized < PINCH_THRESHOLD:
                    cv2.circle(image, (cx_mid, cy_mid), 10, (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "JUMP!", (cx_mid - 20, cy_mid - 20), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    
                    if not is_pinched:
                        pyautogui.keyDown('space')
                        print("Jump!")
                        is_pinched = True
                else:
                    if is_pinched:
                        pyautogui.keyUp('space')
                        is_pinched = False
        
        # Display FPS
        cv2.putText(image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Dino Hand Controller', image)
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Cleanup
    if is_pinched:
        pyautogui.keyUp('space')
    cap.release()
    cv2.destroyAllWindows()
