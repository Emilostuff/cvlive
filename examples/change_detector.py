from cvlive import LiveImageProcessor, annotate
import cv2
import numpy as np


class ChangeDetector(LiveImageProcessor):
    def __init__(self, T, alpha, A):
        """Change detector constructor

        Args:
            T: Activation threshold (in range 0..255)
            alpha: Exponential filter strength (in range 0..1)
            A: Change detection threshold (in range 0..1)
        """
        self.T = T
        self.alpha = alpha
        self.A = A
        super().__init__()

    def convert(self):
        # convert input to grayscale signed 16-bit (to enable subtraction)
        return cv2.cvtColor(self.raw_input, cv2.COLOR_BGR2GRAY).astype(np.int16)

    def process(self):
        # compute difference from previous image
        difference = np.abs(self.input - self.prev_input).astype(np.uint8)
        # compute activation
        thresh = difference > self.T
        self.activated = np.count_nonzero(thresh) / difference.size
        # store threshold image as result
        self.result = thresh.astype(np.uint8) * 255

    def display(self):
        messages = [f"FPS: {self.fps}", f"ACTIVATION: {self.activated * 100:.1f} %"]
        if self.activated > self.A:
            messages.append("CHANGE DETECTED!")

        # show both input and difference image
        cv2.imshow("Input", self.raw_input)
        cv2.imshow("Result", annotate(self.result_buf, messages))

    def update(self):
        # exponential filter on reference image and current image
        self.prev_input = self.alpha * self.prev_input + (1 - self.alpha) * self.input


if __name__ == "__main__":
    ChangeDetector(T=15, alpha=0.90, A=0.05).run()
