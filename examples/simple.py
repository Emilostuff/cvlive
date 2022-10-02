from cvlive import LiveImageProcessor
import cv2


class MySimpleProcessor(LiveImageProcessor):
    def convert(self):
        # convert input image to grayscale
        return cv2.cvtColor(self.raw_input, cv2.COLOR_BGR2GRAY)

    def process(self):
        # blur the input using a 51x51 Gaussian filter
        self.result = cv2.GaussianBlur(self.input, (51, 51), 0)


if __name__ == "__main__":
    MySimpleProcessor().run()
