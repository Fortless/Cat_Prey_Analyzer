import cv2
import numpy as np
from collections import deque
import pytz
from datetime import datetime
from threading import Thread
import time
import gc


class Camera:
    def __init__(self):
        # Initialize HTTP stream URL
        self.stream_url = "http://stream:somepass@localhost:9081/"

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
