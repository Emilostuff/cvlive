# CVLive
A multithreaded live image processor in Python running OpenCV that processes images from a webcam or another video source and shows the results in 'real time'. A separate thread handles the processing while the main thread displays the previous result and captures the next input, resulting in significant performance gains on a multi-core CPU. 

CVLive makes it possible to create live demos of a wide variety of image processing concepts *in only a few lines of code*. 

# How to Install
```bash
pip install cvlive
```

# How to Use
- Import `cvlive`
- Create a subclass of `LiveImageProcessor`
- Override one or more of the class methods: `convert()`, `process()`, `display()` and `update()` to obtain the desired functionality

Please take a look at the [examples](https://github.com/Emilostuff/cvlive/tree/main/examples) and consult the documentation found in the [`LiveImageProcessor`](https://github.com/Emilostuff/cvlive/blob/main/src/cvlive/processor.py) base class to see how this might be done.

# A Simple Example
```python
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

```



