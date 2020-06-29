'''
This is the class for the Gaze Estimation Model.
'''
import cv2
from openvino.inference_engine.ie_api import IENetwork, IECore


class Gaze_Estimation:
    '''
    Class for the Gaze Estimation Model.
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
        self.input_shape = self.model.inputs['left_eye_image'].shape # same shape for both eyes
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

    def predict(self, left_eye_image, right_eye_image, head_pose_angles):
        '''
        This method is meant for running predictions with the provided inputs :
        square crop of left eye image, square crop of right eye image, and three head pose angles – (yaw, pitch, and roll)

        Names of the inputs & output are those provided in the model's documentation :
        https://docs.openvinotoolkit.org/latest/_models_intel_gaze_estimation_adas_0002_description_gaze_estimation_adas_0002.html
        '''
        output = self.net.infer({
                        'left_eye_image': self.preprocess_input(left_eye_image),
                        'right_eye_image': self.preprocess_input(right_eye_image),
                        'head_pose_angles': head_pose_angles
                      })
        return output['gaze_vector'][0]

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
