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

    def __init__(self, model_name, device='CPU', extensions=None):

        # load the objects corresponding to the models
        self.face_detection = Face_Detection(args.face_detection_model, args.device, args.extensions)
        self.gaze_estimation = Gaze_Estimation(args.gaze_estimation_model, args.device, args.extensions)
        self.head_pose_estimation = Head_Pose_Estimation(args.head_pose_estimation_model, args.device, args.extensions)
        self.facial_landmarks_detection = Facial_Landmarks_Detection(args.facial_landmarks_detection_model, args.device, args.extensions)

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
        self.mouse_controller = MouseController('high', 'fast')

        self.out_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'avc1'), 29.97, (1920, 1080), True)

    def run(self):
        '''
        This method process each frame.
        '''
        i = 0
        for batch in self.feed.next_batch():
            if batch is None:
                break

            face = self.face_detection.predict(batch)
            i = i + 1
            if face is None:
                continue
            else:
                left_eye_image, right_eye_image = self.facial_landmarks_detection.predict(face)
                head_pose_angles = self.head_pose_estimation.predict(face)
                vector = self.gaze_estimation.predict(left_eye_image, right_eye_image, head_pose_angles)
                cv2.imshow("Detected face", face)
                cv2.waitKey(1)
                self.mouse_controller.move(vector[0], vector[1])

        self.feed.close()
        cv2.destroyAllWindows()

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

    args = parser.parse_args()

    computer_pointer_controller = Computer_Pointer_Controller(args)
    computer_pointer_controller.run()
