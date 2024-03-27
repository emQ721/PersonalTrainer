import cv2
import mediapipe as mp
import numpy as np
import time
import math
def findAngle(img,p1,p2,p3,lmlist,draw=True):
    x1,y1 = lmlist[p1][1:]
    x2, y2 = lmlist[p2][1:]
    x3, y3 = lmlist[p3][1:]

    angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y2-y1,x1-x2))

    if angle <0:
        angle +=360

    if draw:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0), 2)
        cv2.circle(img,(x1,y1),10,(0,255,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x1, y1), 20, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 20, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 20, (0, 255, 255), cv2.FILLED)

        cv2.putText(img,str(angle),(x2-25,y2-25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    return angle



cap = cv2.VideoCapture("video2.mp4")
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
dir =0
count =0


while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    lmList = []

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)

        for id , lm in enumerate(results.pose_landmarks.landmark):
            h,w,_ = img.shape

            cx,cy =(int(lm.x*w),int(lm.y*h))
            lmList.append([id,cx,cy])

    if len(lmList) !=0:
        angle = findAngle(img,12,14,16,lmList)

        per = np.interp(angle,[275,285],[0,100])
        print(angle)

        if per ==100:
            if dir ==0:
                count +=0.5
                dir =1
        if per ==0:
            if dir ==1:
                count +=0.5
                dir =0

        print(count)
        cv2.putText(img,str(count),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        if count ==5:
            cv2.putText(img,"Basketball Player",(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)












    cv2.imshow('img',img)
    if cv2.waitKey(40) & 0xFF ==ord("q"):
        break



cap.release()
cv2.destroyAllWindows()





