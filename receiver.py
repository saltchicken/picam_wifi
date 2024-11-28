from vidgear.gears import NetGear
import cv2

# Configure NetGear client with receive_mode enabled
client = NetGear(address="0.0.0.0", port="5556", protocol="tcp", logging=True, receive_mode=True)

while True:
    # Receive the frame from the server
    frame = client.recv()
    if frame is None:
        break
    print(frame)

    # processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the frame
    # print(processed_frame)
    cv2.imshow("Received Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
client.close()
cv2.destroyAllWindows()
