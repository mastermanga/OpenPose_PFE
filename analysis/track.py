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
from datetime import datetime

def frame_detect(track_folder, video, name, i):
    while (vs.isOpened()):
        frames = vs.read()
        frame = frames [1]
        
        if frame is None:
            break

        frame = imutils.resize(frame, width=600)
    
        if i == 0:
            cv2.imwrite(os.path.join(track_folder , str(name) + '_first.png'), frame)
        cv2.imwrite(os.path.join(track_folder , str(name) + '_last.png'), frame)
    
        key = cv2.waitKey(1)
    
        if key == ord("q"):
            break


        i += 1
    
    vs.release()
    cv2.destroyAllWindows()



def track(track_folder, video, name, colorLower,colorUpper, pts, durationInSeconds, time_attack):
    i=0
    
    #[time_first, time_mvt, got_first] 
    ts = [0,0,False]
    found = []

    while (vs.isOpened()):
        frames = vs.read()
        frame = frames [1]
        
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
        pts.append(center)

        # white image
        img = np.zeros(frame.shape,dtype=np.uint8)
        img.fill(255)

        
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue

            if i > 1:
                if (pts[i-1][0]- pts[i][0] < -2) or (pts[i-1][0]- pts[i][0] > 2) or (pts[i-1][1]- pts[i][1] < -2) or (pts[i-1][1]- pts[i][1] > 2):
                    
                    cv2.line(frame, pts[i-1], pts[i], (0,0,255),2)
                    cv2.line(img, pts[i - 1], pts[i], (0,0,0),2)
                    
                    if ts[2] == False:
                        milliseconds = vs.get(cv2.CAP_PROP_POS_MSEC) 
                        seconds = milliseconds/1000
                        ts[0] = seconds - time_attack
                        ts[1] = durationInSeconds - seconds
                        ts[2] = True
                        found.append([ts[0], ts[1],ts[2]])


        # show the frame to our screen
        #cv2.imshow("Frame",frame)
        
        im = cv2.putText(img, 'temps reaction: %.2f s' % ts[0], (319,300), cv2.FONT_HERSHEY_SIMPLEX ,  
                   0.5, (255, 0, 0) , 1, cv2.LINE_AA) 
        mvt = cv2.putText(im, 'temps mouvement: %.2f s' % ts[1], (319,320), cv2.FONT_HERSHEY_SIMPLEX ,  
                   0.5, (255, 0, 0) , 1, cv2.LINE_AA) 
        cv2.imwrite(os.path.join(track_folder , str(name) + '_white.png'), mvt)


        key = cv2.waitKey(1)
        
        if key == ord("q"):
            break

        i += 1
    
    vs.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-o", "--output",
        help="path to the output directory")
    args = vars(ap.parse_args())

    if not args.get("video", False):
        vs = VideoStream(src=0).start()
    else:
        vs = cv2.VideoCapture(args["video"])
        vs2 = vs
    time.sleep(2.0)

    video_name = args["video"]
    track_folder = args["output"]

    # green color mask
    colorLower = np.array([30, 52, 72], np.uint8) 
    colorUpper = np.array([90, 255, 255], np.uint8) 
    
    # list of points
    pts = deque(maxlen=64)

    # name 
    print(video_name)
    name = video_name.split('/')[-1]
    # name = name.split('.',1)[0]

    name = name.split('.')[0] + '.' + name.split('.')[1]
    
    #attack
    attack = name.split('_',2)[-1]
    # attack_path = video_name.split('/')[0] + '/attack_seq/' + attack + '.mp4'
    attack_path = './record/attack_seq/' + attack 
    attack_vs = cv2.VideoCapture(attack_path)
    time_attack = float(attack_vs.get(cv2.CAP_PROP_FRAME_COUNT)) / float(attack_vs.get(cv2.CAP_PROP_FPS))
        
    # record
    durationInSeconds = float(vs.get(cv2.CAP_PROP_FRAME_COUNT)) / float(vs.get(cv2.CAP_PROP_FPS))  

    # tracking
    print(name)
    track(track_folder, vs, name, colorLower, colorUpper, pts, durationInSeconds, time_attack)
    
    #frame extraction
    vs = cv2.VideoCapture(args["video"])
    frame_detect(track_folder, vs, name, 0)
    
    #print("durationInSeconds: ",durationInSeconds,"s")
    
