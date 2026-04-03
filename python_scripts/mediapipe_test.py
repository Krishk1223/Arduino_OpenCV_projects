import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
import pathlib

def draw_landmarks_on_image(rgb_image, detection_result):
    # credit to mediapipe docs for the code used in this function.
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.


    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks,
        connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style())
    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks,
        connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style())
    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks,
        connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_LEFT_IRIS,
          landmark_drawing_spec=None,
          connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style())
    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks,
        connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_RIGHT_IRIS,
          landmark_drawing_spec=None,
          connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style())

  return annotated_image

def main():
    root_dir = pathlib.Path(__file__).parent.parent
    model_path = str(root_dir / "models" / "face_landmarker.task")
    print(model_path)
    webcam = cv2.VideoCapture(0)
    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.IMAGE,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5)

    with FaceLandmarker.create_from_options(options) as face_landmarker:
        while True:
            control, frame = webcam.read()
            frame = cv2.flip(frame, 1) # Flip the frame horizontally for a mirror effect
            if not control:
                print("Unable to read from webcam feed")
                break

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(frame))
            face_landmarker_result = face_landmarker.detect(mp_image)

            frame = draw_landmarks_on_image(frame, face_landmarker_result)

            # if you want to draw landmarks manually without using the drawing_utils, you can use the code below (this just draws the landmarks as green circles on the frame, you can customize it as needed):
            # if face_landmarker_result.face_landmarks:
            #     for landmarks in face_landmarker_result.face_landmarks:
            #         for landmark in landmarks:
            #             x = int(landmark.x * frame.shape[1])
            #             y = int(landmark.y * frame.shape[0])
            #             cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            cv2.imshow("Test", frame)
            if cv2.waitKey(10) & 0xFF == 27:
                break


if __name__ == "__main__":
    main()

# to draw proper landmarks use code below accordingly
#@markdown We implemented some functions to visualize the face landmark detection results. <br/> Run the following cell to activate the functions.
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from mediapipe.tasks.python.vision import drawing_utils
# from mediapipe.tasks.python.vision import drawing_styles
# import numpy as np
# import matplotlib.pyplot as plt