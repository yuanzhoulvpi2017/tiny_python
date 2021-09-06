import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


# for webcam input:

def main():
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    cap = cv2.VideoCapture(0)

    with mp_face_mesh.FaceMesh(min_tracking_confidence=0.5, min_detection_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty frames.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = face_mesh.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    if face_landmarks is not None:
                        # print(face_landmarks.landmark)
                        mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            # landmark_drawing_spec=None,
                            # connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                        )

            cv2.imshow(winname="face Mesh", mat=image)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


if __name__ == '__main__':
    main()
