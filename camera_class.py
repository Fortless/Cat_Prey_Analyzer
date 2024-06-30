import cv2
import pytz
from datetime import datetime
import yaml
import time
import gc


class Camera:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        # Initialize HTTP stream URL
        self.stream_url = config['camera']['stream_url']

    def fill_queue(self, deque):
        cap = cv2.VideoCapture(self.stream_url)
        if not cap.isOpened():
            print("Error: Couldn't open the stream.")
            return

        while True:
            gc.collect()
            ret, frame = cap.read()
            if not ret:
                print("Error: Couldn't read the frame.")
                break

            image = frame()

            deque.append(
                (datetime.now(pytz.timezone('Europe/Zurich')).strftime("%Y_%m_%d_%H-%M-%S.%f"), image)
            )
            # deque.pop()
            print("Quelength: " + str(len(deque)) + "\tFrame size: " + str(sys.getsizeof(frame)))

            # Wait to achieve approximately 5 frames per second
            time.sleep(0.2)  #

            # Simulate the loop break and restart after 60 frames
            if len(deque) >= 60:
                print("Loop ended, starting over.")
                break

        cap.release()
