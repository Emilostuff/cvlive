from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="cvlive",
    version="0.1.2",
    description="A multithreaded live image processor in Python running OpenCV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emilostuff/cvlive",
    author="Emil Skydsgaard",
    author_email="emilostuff@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Image Processing"
    ],
    keywords="OpenCV, image, processing, computer, vision, demo, multithreaded",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=["opencv-python"],
)
