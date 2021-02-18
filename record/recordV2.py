import argparse
import logging
import time
import numpy as np
import os
import random
import cv2
from datetime import datetime

def read_and_record(output_path, n):
    # Attack sequence initialization 
    atk_name = random.choice(os.listdir("./record/attack_seq/"))
    atk_path = "./record/attack_seq/"+ atk_name
    atk_cap = cv2.VideoCapture(atk_path)

    atk_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    atk_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

    atk_rate = atk_cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(atk_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count/atk_rate)
    
    if (atk_cap.isOpened()== False): 
          print("Error opening video stream or file")

    # Defense sequence initialization
    goal_cap = cv2.VideoCapture(0)
    t0 = time.time()
    if (goal_cap.isOpened() == False): 
          print("Unable to read camera feed")
    frame_width = int(goal_cap.get(3))
    frame_height = int(goal_cap.get(4))
    goal_rate = goal_cap.get(cv2.CAP_PROP_FPS)


    # Write camera feed in directory
    now = now = datetime.now() # current time
    curr_time = now.strftime("%H:%M:%S")

    output_vid = output_path + '_' + curr_time + '_' + atk_name + '.avi'
    out = cv2.VideoWriter(output_vid,cv2.VideoWriter_fourcc('M','J','P','G'), goal_rate,(frame_width,frame_height))


    while(True):
        atk_ret, atk_frame = atk_cap.read(atk_rate)
        goal_ret, goal_frame = goal_cap.read(goal_rate)
        if goal_ret == True:
                
                if atk_ret == True: 
                    cv2.imshow(atk_name,atk_frame)

                out.write(goal_frame)

                # Display the resulting frame    
                # cv2.imshow('frame',frame)

                # Press Q on keyboard to stop recording
                if cv2.waitKey(1) & 0xFF == ord('q'):
                      break

                t1 = time.time() # current time
                num_seconds = t1 - t0 # diff
                if num_seconds > duration + 2:
                    break
        else:
            break 

    atk_cap.release()
    goal_cap.release()
    cv2.destroyAllWindows()


def script(iterations, name):
    path = "./record/goal/" + name + "/"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
        
    for n in range(1, iterations+1):
        print("Processed video :" + str(n))
        read_and_record(path + name,n)
        time.sleep(1) 
        
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='recording simulation run')
    parser.add_argument('--runs', type=int, default=1)

    args = parser.parse_args()

    now = datetime.now() # current date and time

    curr_date = now.strftime("%b-%d-%Y")
    script(args.runs,curr_date)
