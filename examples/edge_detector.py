from cvlive import LiveImageProcessor
import cv2
import numpy as np


class EdgeDetector(LiveImageProcessor):
    def convert(self):
        # convert input to grayscale
        return cv2.cvtColor(self.raw_input, cv2.COLOR_BGR2GRAY)

    def process(self):
        # input filtering
        median = cv2.medianBlur(self.input, 11)
        gaussian = cv2.GaussianBlur(median, (3, 3), 0)

        # Edge detection using a Prewitt filter
        kernel_x = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernel_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        prewitt_x = cv2.filter2D(gaussian, -1, kernel_x)
        prewitt_y = cv2.filter2D(gaussian, -1, kernel_y)
        self.result = prewitt_x + prewitt_y


if __name__ == "__main__":
    EdgeDetector().run()
