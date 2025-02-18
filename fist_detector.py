import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial('COM4', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
last_command = '' 

def detect_finger_gesture(landmarks):
    """ Detects which fingers are raised (1 = raised, 0 = down) """
    fingers = [0, 0, 0, 0, 0] 
    
    if landmarks[4].x < landmarks[3].x: 
        fingers[0] = 1


    for i, tip, base in [(1, 8, 6), (2, 12, 10), (3, 16, 14), (4, 20, 18)]:
        if landmarks[tip].y < landmarks[base].y:  
            fingers[i] = 1

    return fingers

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            fingers = detect_finger_gesture(landmarks)

            raised_fingers = sum(fingers)

            if raised_fingers == 5:
                if last_command != 'H':
                    arduino.write(b'H')
                    last_command = 'H'
                    print("Sent: H (All LEDs & Buzzer ON)")

            elif raised_fingers == 1:
                led_index = fingers.index(1) + 1
                if last_command != str(led_index):
                    arduino.write(str(led_index).encode())
                    last_command = str(led_index)
                    print(f"Sent: {led_index} (LED {led_index} ON)")

            elif raised_fingers == 0:
                if last_command != '0':
                    arduino.write(b'0')
                    last_command = '0'
                    print("Sent: 0 (All LEDs & Buzzer OFF)")

    cv2.imshow("Gesture LED Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
