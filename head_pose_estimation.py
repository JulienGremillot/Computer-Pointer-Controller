'''
This is the class for the Head Pose Estimation Model.
'''
import cv2
import numpy as np
from openvino.inference_engine.ie_api import IENetwork, IECore


class Head_Pose_Estimation:
    '''
    Class for the Head Pose Estimation Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None):
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
        This method is meant for running predictions on the input image.
        '''
        preprocessed_image = self.preprocess_input(image)
        output = self.net.infer({self.input_name: preprocessed_image})
        # Output contains :
        # name: "angle_y_fc", shape: [1, 1] - Estimated yaw (in degrees).
        # name: "angle_p_fc", shape: [1, 1] - Estimated pitch (in degrees).
        # name: "angle_r_fc", shape: [1, 1] - Estimated roll (in degrees).
        return np.array([[output["angle_y_fc"][0][0],  output["angle_p_fc"][0][0], output["angle_r_fc"][0][0]]])

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
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        raise NotImplementedError
