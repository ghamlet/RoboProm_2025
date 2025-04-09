import cv2
from track_bars import ColorTracker

image = cv2.imread("Screenshot from 2025-04-09 16-16-28.png")[300:800, 600:1100,:]

tracker = ColorTracker()


while True:
    tracker.process_frame(image)