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



def track(track_folder, video, name, colorLower,colorUpper, pts):
    
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
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
            c = max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        pts.appendleft(center)
        
        # white image
        img = np.zeros(frame.shape,dtype=np.uint8)
        img.fill(255)

        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            cv2.line(frame, pts[i-1], pts[i], (0,0,255),2)
            cv2.line(img, pts[i - 1], pts[i], (0,0,255),2)

        # show the frame to our screen
        #cv2.imshow("Frame",frame)
        name = name.split('/',2)[-1]
        name = name.split('.',1)[0]
        cv2.imwrite(os.path.join(track_folder , str(name) + 'video.png'), frame)
        cv2.imwrite(os.path.join(track_folder , str(name) + '.png'), img)
        key = cv2.waitKey(1)
        
        if key == ord("q"):
            break
    
    vs.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    args = vars(ap.parse_args())

    if not args.get("video", False):
        vs = VideoStream(src=0).start()
    else:
        vs = cv2.VideoCapture(args["video"])
    time.sleep(2.0)

    directory = op.expanduser('video')
    video_folder = op.join(directory, 'hockey')
    track_folder = op.join(directory, 'track')

    # video_name = op.join(video_folder, args["video"])

    video_name = args["video"]

    colorLower = np.array([30, 52, 72], np.uint8) 
    colorUpper = np.array([90, 255, 255], np.uint8) 
    pts = deque(maxlen=64)
    print(video_name)
    track(track_folder, vs, video_name, colorLower, colorUpper, pts)
