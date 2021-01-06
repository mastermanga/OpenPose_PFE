import argparse
import logging
import time
import numpy as np
import os
import random
import cv2
from datetime import date

def read_vid():
    
    name = random.choice(os.listdir("attack_seq/"))
    path = "attack_seq/"+name
    cap = cv2.VideoCapture(path)
    rate = cap.get(cv2.CAP_PROP_FPS)
    if (cap.isOpened()== False): 
          print("Error opening video stream or file")
    while(cap.isOpened()):
        ret, frame = cap.read(rate)
        if ret == True:
            time.sleep(1/rate)

            cv2.imshow(name,frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    return name


def record_vid(name):
    print("record_vid load")
    # name = vid = goal/test/test_1
    file = name +'.avi'
    cap = cv2.VideoCapture(0)
    t0 = time.time()
    if (cap.isOpened() == False): 
          print("Unable to read camera feed")
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    rate = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(file,cv2.VideoWriter_fourcc('M','J','P','G'), rate, (frame_width,frame_height))
    while(True):
        
        ret, frame = cap.read()
        if ret == True: 
                out.write(frame)

                # Display the resulting frame    
                cv2.imshow('frame',frame)

                # Press Q on keyboard to stop recording
                if cv2.waitKey(1) & 0xFF == ord('q'):
                      break

                t1 = time.time() # current time
                num_seconds = t1 - t0 # diff
                if num_seconds > 5:
                    break
        else:
            break  
    cap.release()
    out.release()
    cv2.destroyAllWindows() 

def script(iterations, name):
    path = "goal/" + name
    path = path + "/"
    print(path)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
        
    for n in range(1, iterations+1):
        print("Read video :" + str(n))
        attack_name = read_vid()
        print("Record video :" + str(n))
        vid = path + name + '_' + attack_name + '_' + str(n)
        print(vid)
        # vid = 'goal/test/test_1'
        record_vid(vid)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='recording simulation run')
    parser.add_argument('--runs', type=int, default=1)

    args = parser.parse_args()

    today = date.today()
    curr_date = today.strftime("%b-%d-%Y")
    print("Current date =", curr_date)
    script(args.runs,'Training '+ curr_date)
