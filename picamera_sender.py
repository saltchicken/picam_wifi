import cv2
from picamera2 import Picamera2
from vidgear.gears import NetGear

picam2 = Picamera2()
# video_config = picam2.create_video_configuration(main={"size": (640, 480)})
# video_config = picam2.create_video_configuration(main={"size": (1280, 960)})
video_config = picam2.create_video_configuration(main={"size": (1920, 1080)})
# video_config = picam2.create_video_configuration(main={"size": (3840, 2160)})
# video_config = picam2.create_video_configuration(main={"format": "BGR888", "size": (640, 480)})

fps = 30
frame_duration = int(1e6 / fps)  # Convert FPS to microseconds (1 second = 1,000,000 microseconds)
video_config["controls"]["FrameDurationLimits"] = (frame_duration, frame_duration)


picam2.configure(video_config)
picam2.start()

# Configure NetGear server
server = NetGear(address="10.0.0.3", port="5556", protocol="tcp", logging=True)


try:
    print("Streaming video... Press Ctrl+C to stop.")
    while True:
        # Capture frame from Picamera2
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Stream the frame over the network
        server.send(frame_bgr)

except KeyboardInterrupt:
    print("\nServer stopped.")

finally:
    # Cleanup
    picam2.stop()
    server.close()
