import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


def main():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = holistic.process(image)

            # Draw landmark annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if image is not None:
                mp_drawing.draw_landmarks(
                    image,
                    results.face_landmarks,
                    mp_holistic.FACE_CONNECTIONS,
                    landmark_drawing_spec=None,
                    # connection_drawing_spec=mp_drawing_styles
                    # .get_default_face_mesh_contours_style()
                )
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS,
                    # landmark_drawing_spec=mp_drawing_styles
                    # .get_default_pose_landmarks_style()
                )
            cv2.imshow('MediaPipe Holistic', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


if __name__ == '__main__':
    main()
