import cv2, time
from datetime import datetime
import pandas
import numpy

"""
This program uses a webcam to detect new objects in frame and returns a bokeh plot
that shows when foreign object shows onscreen and when it leaves.
"""

first_frame=None
status_list=[None, None]
times=[]
df=pandas.DataFrame(columns=["Start", "End"])


video=cv2.VideoCapture(0)


while True:
    check, frame = video.read()
    status=0
    #load current frame
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (21,21), 0)
    #determine if its the first frame - if so continue to next frame
    if first_frame is None:
        first_frame = gray
        continue
    #difference between first frame and change
    #delta frame is overlay of first image, threshframe measure differences in contrast view
    delta_frame=cv2.absdiff(first_frame, gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 225, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _)  = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #contours have a greater area of 1000 pixels, create green rectangle
    for contour in cnts:
        if cv2.contourArea(contour)< 1000:
            continue
        status=1
        #Draw rectangle to current Frame
        (x, y, w, h)= cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)

    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    #show 4 different frames
    # cv2.imshow("Grayframe", gray)
    # cv2.imshow("delta_frame", delta_frame)
    # cv2.imshow("Threshhold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)


    #once q is pressed, program is exited
    key = cv2.waitKey(1)

    if key == ord('q'):
        if status==1:
            times.append(datetime.now())
        break



# print(times)

for i in range(0,len(times), 2):
    df=df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()
