import threading
import time
import cv2


def annotate(frame, messages):
    """Burn text into the provided frame."""
    for (i, msg) in enumerate(messages):
        cv2.putText(frame, msg, (25, (i + 1) * 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255, 1)
    return frame


class LiveImageProcessor:
    """A multithreaded image processing engine.

    Usage
    -----
    Make a subclass and override one or more of the following methods:
    - `convert()`
    - `process()`
    - `display()`
    - `update()`

    The constructor `__init__()` can also be overridden,
    but then remember to call `super().__init__()` in the new constructor.

    Overridden methods should not mutate any attributes
    which are not explicitly required to be updated,
    since this potentially can lead to race conditions.

    Introducing new attributes in the subclass is fine,
    but care must be taken if they are used by the `process() function.
    """

    def __init__(self, url=0, width=None, height=None):
        """Connects to the desired video source."""
        # connect to video source
        print("Video feed starting up ... ", end="")
        self.cap = cv2.VideoCapture(url)
        if not self.cap.isOpened():
            raise Exception(f"Failed to open video source at: {url}!")
        self.n_frames = 0
        print("Ready!")

        # set custom frame size
        if width and height:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    @property
    def fps(self):
        """Returns the average FPS of the image processor."""
        return int(self.n_frames / (time.time() - self.start_time))

    def capture(self):
        """
        Reads new frame from the video source and
        puts the converted frame into the input buffer.
        """
        ok, frame = self.cap.read()
        if not ok:
            raise Exception("Can't receive frame")
        self.raw_input = frame
        self.input_buf = self.convert()

    def convert(self):
        """converts the raw input frame to the desired format.

        How to Override
        -----
        The function must return an image.
        Use this function to discard unneeded information
        or to convert to a desired format.

        The returned value can be any function of `self.raw_input`
        """
        return self.raw_input

    def process(self):
        """Processes the input image and stores the result.

        How to Override
        -----
        The function must update `self.result`.

        The updated value can be any function of:
        - `self.input`
        - `self.prev_input`
        """
        time.sleep(0.025)
        self.result = self.input

    def display(self):
        """Generates and displays the desired output.

        How to Override
        -----
        The function should call `cv2.imshow(...)` at least once.

        The function is allowed to read from:
        - `self.result_buf`
        - `self.input`
        - `self.prev_input`
        - `self.raw_input`
        - `self.fps`
        """
        cv2.imshow("Output", annotate(self.result_buf, [f"FPS: {self.fps}"]))

    def update(self):
        """Updates the previous image (reference).

        How to Override
        -----
        The function must update `self.prev_input`.

        The updated value can be any function of:
        - `self.input`
        - `self.prev_input`
        """
        self.prev_input = self.input

    def run(self):
        """Runs an infinite processing loop until 'q' is pressed."""
        # setup
        self.capture()
        self.input = self.input_buf
        self.prev_input = self.input
        self.process()
        self.capture()
        # track fps
        self.start_time = time.time()
        # processing loop
        print("Processing loop started! Press 'q' to exit.")
        while True:
            # update frame count
            self.n_frames += 1
            # shift buffers
            self.update()
            self.input = self.input_buf
            self.result_buf = self.result
            # launch separate thread processing the frame
            t1 = threading.Thread(target=self.process, args=())
            t1.start()
            # meanwhile, display previous result and capture next frame
            self.display()
            self.capture()
            # check for exit command
            if cv2.waitKey(1) == ord("q"):
                break
            # wait for processing thread to finish
            t1.join()

        # shut down gracefully
        print("Exiting ... ", end="")
        self.cap.release()
        cv2.destroyAllWindows()
        t1.join()
        print("Done!")


if __name__ == "__main__":
    LiveImageProcessor().run()
