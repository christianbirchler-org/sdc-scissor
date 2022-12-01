import cv2
import numpy as np
from tensorflow import keras


class Dave2Model:
    def __init__(self):
        path = "sdc_scissor/simulator_api/self_driving_models/dave2.h5"
        self.model = keras.models.load_model(path)

    def predict(self, img):
        """Return steering direction from -1.0 to 1.0"""

        preprocessed = self.img_preprocess(img)
        prediction = self.model.predict(np.array([preprocessed]))
        return float(prediction[0][0])

    def img_preprocess(self, img):
        """Prepare an image for inference"""

        img = np.asarray(img)

        ## Crop image to remove unnecessary features
        img = img[60:135, :, :]

        ## Change to YUV image
        img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)

        ## Gaussian blur
        img = cv2.GaussianBlur(img, (3, 3), 0)

        ## Decrease size for easier processing
        img = cv2.resize(img, (100, 100))

        ## Normalize values
        img = img / 255
        return img
