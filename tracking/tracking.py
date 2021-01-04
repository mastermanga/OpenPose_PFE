from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import matplotlib.pyplot as plt
import os.path as op
import os

directory = op.expanduser('video')
video_folder = op.join(directory, 'hockey')
track_folder = op.join(directory, 'track')

video_name = [op.join(video_folder, fn) for fn in os.listdir(video_folder) if fn.endswith('.mp4')]

def track(track_folder, video, colorLower,colorUpper, pts):
    
    vs = cv2.VideoCapture(video)
    time.sleep(2.0)
    
    while True:
        frame = vs.read()
        frame = frame [1]
        
        if frame is None:
            break
        
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center 
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # update the points queue
        pts.appendleft(center)
        
        # white image
        img = np.zeros(frame.shape,dtype=np.uint8)
        img.fill(255)

        # loop over the set of tracked points
        for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
            if pts[i - 1] is None or pts[i] is None:
                continue
            cv2.line(frame, pts[i - 1], pts[i], (0,0,255),2)
            cv2.line(img, pts[i - 1], pts[i], (0,0,255),2)

    # show the frame to our screen
        name = video.split('/',2)[-1]
        name = name.split('.',1)[0]
        cv2.imwrite(os.path.join(track_folder , str(name) + 'video.jpg'), frame)
        cv2.imwrite(os.path.join(track_folder , str(name) + '.jpg'), img)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            break
    
    vs.release()
    cv2.destroyAllWindows()


colorLower = np.array([115, 100, 86], np.uint8) 
colorUpper = np.array([135, 220, 166], np.uint8) 
pts = deque(maxlen=64)

for vs in video_name:
    print(vs)
    track(track_folder, vs, colorLower, colorUpper, pts)