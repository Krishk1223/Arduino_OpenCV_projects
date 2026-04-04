import cv2
import numpy as np
import mediapipe as mp
import pathlib
import math
import serial
from serial.tools import list_ports
import sys

RIGHT_LIP_INDEX = 306
LEFT_LIP_INDEX = 61
BAUD_RATE = 9600

def port_checker():
    ports = list_ports.comports()
    for port in ports:
        print(f"Port: {port.device}, Description: {port.description}")
        if "IOUSBHostDevice" in port.description:
            print(f"Arduino found on port: {port.device}")
            return port.device

    print("Arduino not found. Please check your connections.")
    return None


def main():
    arduino_port = port_checker()
    if arduino_port is None:
        print("Exiting program due to missing Arduino connection.")
        sys.exit(1)
    arduino = serial.Serial(arduino_port, BAUD_RATE)
    root_dir = pathlib.Path(__file__).parent.parent
    model_path = str(root_dir / "models" / "face_landmarker.task")
    print("Press ESC to quit webcam feed.")
    webcam = cv2.VideoCapture(0)
    baseOptions = mp.tasks.BaseOptions
    faceLandMarker = mp.tasks.vision.FaceLandmarker
    faceLandMarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    visionRunningMode = mp.tasks.vision.RunningMode

    options = faceLandMarkerOptions(
        base_options=baseOptions(model_asset_path=model_path),
        running_mode=visionRunningMode.IMAGE,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )

    with faceLandMarker.create_from_options(options) as face_landmarker:
        while True:
            control, frame = webcam.read()
            if not control:
                print("ERROR: UNABLE TO READ FROM WEBCAM FEED")
                break
            frame = cv2.flip(frame, 1) # flips for mirror like orientation
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(frame))
            face_landmarker_result = face_landmarker.detect(mp_image)
            height, width, channel = frame.shape #important for landmark coords
            if face_landmarker_result.face_landmarks:
                for landmarks in face_landmarker_result.face_landmarks:
                    point1 = landmarks[RIGHT_LIP_INDEX] # right lip
                    x1, y1 = int(point1.x * width), int(point1.y * height) #point of right lip
                    cv2.circle(frame, center=(x1, y1), radius=2, color=(255,0,0), thickness=2)
                    point2 = landmarks[LEFT_LIP_INDEX] # left lip
                    x2, y2 = int(point2.x * width), int(point2.y * height) #point of left lip
                    cv2.circle(frame, center=(x2, y2), radius=2, color=(255,0,0), thickness=2)
                    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    print("Distance between lips: ", distance) # you can use this distance value to determine if the person is smiling or not, you would need to experiment with different threshold values to find what works best for your use case
                    # 140-153 sadness
                    # 160-179 neutral
                     # 190+ happy
                    if distance < 155:
                        arduino.write(b's') # send 's' for sad
                    elif distance > 155 and distance < 180:
                        arduino.write(b'n') # send 'n' for neutral
                    elif distance > 180 and distance < 300:
                        arduino.write(b'h') # send 'h' for happy
                    else:
                        arduino.write(b'e') # cannot tell expression (adjust webcam?)
                

            cv2.imshow("Face Detector", frame)

            if cv2.waitKey(10) & 0xFF == 27: # press 'esc' to quit the webcam feed
                break


if __name__ == "__main__":
    main()