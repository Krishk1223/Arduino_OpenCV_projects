import cv2

def main():
    webcam = cv2.VideoCapture(0)
    while True:
        control, frame = webcam.read()
        cv2.imshow("Webcam", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'): # Press 'q' to quit the webcam feed
            break 


if __name__ == "__main__":
    main()
