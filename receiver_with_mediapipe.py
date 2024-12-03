from vidgear.gears import NetGear
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure NetGear client with receive_mode enabled
client = NetGear(address="0.0.0.0", port="5556", protocol="tcp", logging=True, receive_mode=True)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while True:
        # Receive the frame from the server
        frame = client.recv()
        if frame is None:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # cv2.rectangle(frame, (300, 300), (100, 100), (0, 255, 0), 0)
        # processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Display the frame
        cv2.imshow("Received Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Release resources
client.close()
cv2.destroyAllWindows()
