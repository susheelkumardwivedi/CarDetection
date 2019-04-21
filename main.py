# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 02:15:16 2019

@author: susheeldwivedi

"""
import cv2
import datetime
import numpy as np
import sys
import os

def rectangleArea(x,y,w,h):
   return w*h

def frameConfig(frame,carcounter=5):
        if carcounter > 6:
            color = (0,255,0)
        else:
            color = (0,0,255)        
        #displaying current date and time
        hight, width,channels = frame.shape
        currentTime = '{date:%Y/%m/%d::%H:%M:%S}'.format( date=datetime.datetime.now() )
        cv2.rectangle(frame,(width-380,hight-90),(width,hight),(0,0,255),-1)
        cv2.putText(frame,currentTime,(width-380,hight-50),cv2.FONT_HERSHEY_COMPLEX,1.0,(255,255,255))
        
        #create a rectangular black box
        cv2.rectangle(frame,(0,0),(250,60),(0,0,0),-1)
        cv2.circle(frame,(30,30),30,color,-1)
        #displying total number of car in current frame current frame
        cv2.putText(frame,str(carcounter),(10,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,3.0,(255,255,255))
        cv2.putText(frame,'Car Detected',(65,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,255))

def capOption():
    if len(sys.argv)!=2:
        print('provide argument followed by filename int or string')
    capture_option= None
    try:
        capture_option = int(sys.argv[1])
    except:
        capture_option = sys.argv[1]
    return capture_option

def directoryConfiguration():
    if os.path.isdir('detected_frame') is False:
        os.mkdir('detected_frame')
    if os.path.isdir('original_frame') is False:
        os.mkdir('original_frame')

def main():
    cap_option = capOption()
    cascade_file = 'car.xml' # present in current working directory
    frame_count=1
    cascade = cv2.CascadeClassifier(cascade_file)
    cap = cv2.VideoCapture(cap_option)
    cv2.namedWindow("Original Frame",cv2.WND_PROP_ASPECT_RATIO)
    while cap.isOpened():
        ret,frame = cap.read()
        if ret == False:
            break
        original = frame.copy()
        frame = cv2.GaussianBlur(frame,(5,5),0.3)
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cars = cascade.detectMultiScale(frame_gray,1.1,1)
        carcounter = 0
        for (x,y,w,h) in cars:
            if rectangleArea(x,y,w,h)> 3500:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.rectangle(frame,(x,y),(x+w,y+10),(0,255,0),-1)
                carcounter = carcounter+1
        
        #print number of car in current frame
        print('Current frame contin ',carcounter,' car')
         # displying a some effect on detecting window
        frameConfig(frame,carcounter)
        cv2.putText(original,'Live',(50,50),cv2.FONT_HERSHEY_TRIPLEX,2.0,(255,255,255))
        cv2.imwrite('detected_frame\detect_frame'+str(frame_count)+'.jpg',frame)
        cv2.imwrite('original_frame\original_frame'+str(frame_count)+'.jpg',original)
        cv2.imshow('Car Detection Frame',frame)
        cv2.imshow('Original Frame',original)
        frame_count=frame_count+1
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    directoryConfiguration()
    main()