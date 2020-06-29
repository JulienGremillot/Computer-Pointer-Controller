'''
This is the class for the Facial Landmarks Detection Model.
'''
import cv2
from openvino.inference_engine.ie_api import IENetwork, IECore

# To crop the eyes from the face, we use a square sized with 1/5 the width of the face.
EYE_FACE_COEF = 0.2

class Facial_Landmarks_Detection:
    '''
    Class for the Facial Landmarks Detection Model.
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
        # Here we return a row-vector of 10 floating point values for five landmarks coordinates in the form (x0, y0, x1, y1, ..., x5, y5).
        # All the coordinates are normalized to be in range [0,1].
        landmarks = next(iter(output.values()))[0]
        width = int(image.shape[1])
        height = int(image.shape[0])
        eye_square_size = int(width * EYE_FACE_COEF)
        left_eye = cv2.getRectSubPix(image, (eye_square_size, eye_square_size), (landmarks[0] * width + eye_square_size / 2, landmarks[1] * height + eye_square_size / 2))
        right_eye = cv2.getRectSubPix(image, (eye_square_size, eye_square_size), (landmarks[2] * width + eye_square_size / 2, landmarks[3] * height + eye_square_size / 2))
        # cv2.circle(image, (landmarks[0] * width, landmarks[1] * height), 5, (0, 0, 255), 1)
        # cv2.circle(image, (landmarks[2] * width, landmarks[3] * height), 5, (0, 0, 255), 1)
        return left_eye, right_eye

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
