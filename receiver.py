from vidgear.gears import NetGear
import cv2
import pyvirtualcam
import numpy as np

# Configure NetGear client with receive_mode enabled
client = NetGear(address="0.0.0.0", port="5556", protocol="tcp", logging=True, receive_mode=True)

with pyvirtualcam.Camera(width=1920, height=1080, fps=30) as cam:
    while True:
        # Receive the frame from the server
        frame = client.recv()
        if frame is None:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cam.send(frame_rgb)

        cv2.imshow("Received Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Release resources
client.close()
cv2.destroyAllWindows()
