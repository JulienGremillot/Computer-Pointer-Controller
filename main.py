'''
This is the main class for the Computer Pointer Controller.
'''
import argparse

import cv2
import time

from face_detection import Face_Detection
from facial_landmarks_detection import Facial_Landmarks_Detection
from gaze_estimation import Gaze_Estimation
from head_pose_estimation import Head_Pose_Estimation
from input_feeder import InputFeeder

# To avoid a very long list of models paths on the command line, here is a list of default models paths.
from mouse_controller import MouseController

FACE_DETECTION_MODEL = "models/intel/face-detection-adas-binary-0001/FP32-INT1/face-detection-adas-binary-0001"
GAZE_ESTIMATION_MODEL = "models/intel/gaze-estimation-adas-0002/FP32/gaze-estimation-adas-0002"
HEAD_POSE_ESTIMATION_MODEL = "models/intel/head-pose-estimation-adas-0001/FP32/head-pose-estimation-adas-0001"
FACIAL_LANDMARKS_DETECTION_MODEL = "models/intel/landmarks-regression-retail-0009/FP32/landmarks-regression-retail-0009"

class Computer_Pointer_Controller:

    def __init__(self, args):

        # load the objects corresponding to the models
        self.face_detection = Face_Detection(args.face_detection_model, args.device, args.extensions, args.perf_counts)
        self.gaze_estimation = Gaze_Estimation(args.gaze_estimation_model, args.device, args.extensions, args.perf_counts)
        self.head_pose_estimation = Head_Pose_Estimation(args.head_pose_estimation_model, args.device, args.extensions, args.perf_counts)
        self.facial_landmarks_detection = Facial_Landmarks_Detection(args.facial_landmarks_detection_model, args.device, args.extensions, args.perf_counts)

        start_models_load_time = time.time()
        self.face_detection.load_model()
        self.gaze_estimation.load_model()
        self.head_pose_estimation.load_model()
        self.facial_landmarks_detection.load_model()
        print("Models total loading time :", time.time() - start_models_load_time)

        # open the video feed
        self.feed = InputFeeder(args.input_type, args.input_file)
        self.feed.load_data()

        # init mouse controller
        self.mouse_controller = MouseController('low', 'fast')

    def run(self):
        '''
        This method process each frame.
        '''
        inferences_times = []
        face_detections_times = []
        for batch in self.feed.next_batch():
            if batch is None:
                break

            # as we want the webcam to act as a mirror, flip the frame
            batch = cv2.flip(batch, 1)

            inference_time = time.time()
            face = self.face_detection.predict(batch)
            if face is None:
                continue
            else:
                face_detections_times.append(time.time() - inference_time)

                left_eye_image, right_eye_image = self.facial_landmarks_detection.predict(face)
                if left_eye_image is None or right_eye_image is None:
                    continue
                head_pose_angles = self.head_pose_estimation.predict(face)
                if head_pose_angles is None:
                    continue
                vector = self.gaze_estimation.predict(left_eye_image, right_eye_image, head_pose_angles)
                inferences_times.append(time.time() - inference_time)
                if args.show_face == "True":
                    cv2.imshow("Detected face", face)
                    cv2.waitKey(1)
                self.mouse_controller.move(vector[0], vector[1])

        self.feed.close()
        cv2.destroyAllWindows()
        print("Average face detection inference time:", sum(face_detections_times) / len(face_detections_times))
        print("Average total inferences time:", sum(inferences_times) / len(inferences_times))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--face_detection_model', default=FACE_DETECTION_MODEL)
    parser.add_argument('--gaze_estimation_model', default=GAZE_ESTIMATION_MODEL)
    parser.add_argument('--head_pose_estimation_model', default=HEAD_POSE_ESTIMATION_MODEL)
    parser.add_argument('--facial_landmarks_detection_model', default=FACIAL_LANDMARKS_DETECTION_MODEL)
    parser.add_argument('--device', default='CPU')
    parser.add_argument('--extensions', default=None)
    parser.add_argument('--input_type', default='cam')
    parser.add_argument('--input_file', default=None)
    parser.add_argument('--show_face', default='True')
    parser.add_argument('--perf_counts', default='False')

    args = parser.parse_args()

    computer_pointer_controller = Computer_Pointer_Controller(args)
    computer_pointer_controller.run()
