from cvlive import LiveImageProcessor


if __name__ == "__main__":
    # Example using the app 'DroidCam' to get video feed from a phone

    # these parameters may vary
    wifi = '192.168.0.116'
    port = '4747'

    # construct url and run
    cam_url = f'http://{wifi}:{port}/video'
    LiveImageProcessor(url=cam_url).run()
