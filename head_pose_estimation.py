'''
This is the class for the Head Pose Estimation Model.
'''
import cv2
import numpy as np
from openvino.inference_engine.ie_api import IENetwork, IECore
import pprint

class Head_Pose_Estimation:
    '''
    Class for the Head Pose Estimation Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None, perf_counts="False"):
        self.model_weights = model_name + '.bin'
        self.model_structure = model_name + '.xml'
        self.device = device
        self.extensions = extensions
        try:
            self.model = IENetwork(self.model_structure, self.model_weights)
        except Exception as e:
            raise ValueError("Could not Initialise the network. Have you enterred the correct model path?")
        self.input_name = next(iter(self.model.inputs))
        self.input_shape = self.model.inputs[self.input_name].shape
        self.output_name = next(iter(self.model.outputs))
        self.output_shape = self.model.outputs[self.output_name].shape
        self.net = None
        self.pp = None
        if perf_counts == "True":
            self.pp = pprint.PrettyPrinter(indent=4)

    def load_model(self):
        '''
        This method loads the model
        '''
        core = IECore()
        if self.extensions != None:
            core.add_extension(self.extensions, self.device)
        self.net = core.load_network(network=self.model, device_name=self.device, num_requests=1)

    def predict(self, image):
        '''
        This method is meant for running predictions on the input image of a face.
        Return a numpy array of the detected three head pose angles (yaw, pitch, and roll)
        '''
        preprocessed_image = self.preprocess_input(image)
        outputs = self.net.infer({self.input_name: preprocessed_image})
        if self.pp is not None:
            self.pp.pprint(self.net.requests[0].get_perf_counts())
        return self.preprocess_output(outputs)

    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):
        '''
        Before feeding the data into the model for inference, given an input image:
        - Resize to width and height required for the model
        - Transpose the final "channel" dimension to be first
        - Reshape the image to add a "batch" of 1 at the start
        '''
        image = cv2.resize(image, (self.input_shape[3], self.input_shape[2]))
        image = image.transpose((2, 0, 1))
        image = image.reshape(1, *image.shape)
        return image

    def preprocess_output(self, outputs):
        '''
        Return a numpy array of the detected three head pose angles (yaw, pitch, and roll)

        Outputs contains :
        # name: "angle_y_fc", shape: [1, 1] - Estimated yaw (in degrees).
        # name: "angle_p_fc", shape: [1, 1] - Estimated pitch (in degrees).
        # name: "angle_r_fc", shape: [1, 1] - Estimated roll (in degrees).

        More information at https://docs.openvinotoolkit.org/latest/_models_intel_head_pose_estimation_adas_0001_description_head_pose_estimation_adas_0001.html
        '''
        return np.array([[outputs["angle_y_fc"][0][0],  outputs["angle_p_fc"][0][0], outputs["angle_r_fc"][0][0]]])
