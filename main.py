import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import random
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8,maxHands=1)
class SnakeGameClass:
    def __init__(self,pathFood):
        self.points=[]
        self.lengths=[]
        self.currentLength=0
        self.allowedLength=150
        self.previousHead=0,0

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.imgFood = cv2.resize(self.imgFood, (50, 50), interpolation=cv2.INTER_AREA)
        self.hFood,self.wFood,_=self.imgFood.shape
        self.foodPoint=0,0
        self.randomFoodLocation()
        self.score=0
        self.GameOver=False

    def randomFoodLocation(self):
        self.foodPoint= random.randint(100,1000),random.randint(100,600)

    def update(self,imgMain,currentHead):
        if self.GameOver:
            cvzone.putTextRect(imgMain,"Game Over",[300,400],scale=7,thickness=5,offset=20)
            cvzone.putTextRect(imgMain,f"Your Score: {self.score}",[300,550],scale=7,thickness=5,offset=20)
            return imgMain
        
        px,py=self.previousHead
        cx,cy=currentHead

        self.points.append([cx,cy])
        distance=math.hypot(cx-px,cy-py)
        self.lengths.append(distance)
        self.currentLength+=distance
        self.previousHead=cx,cy

        if self.currentLength>self.allowedLength:
            for i,length in enumerate(self.lengths):
                self.currentLength-=length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentLength<self.allowedLength:
                    break

        rx,ry=self.foodPoint
        if rx-self.wFood//2<cx<rx+self.wFood//2 and ry-self.hFood//2<cy<ry+self.hFood//2:
            self.randomFoodLocation()
            self.allowedLength+=50
            self.score+=1
            print("Score:",self.score)

        if self.points:
            for i,point in enumerate(self.points):
                if i!=0:
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
            cv2.circle(imgMain,self.points[-1],20,(200,0,0),cv2.FILLED)

        imgMain=cvzone.overlayPNG(imgMain,self.imgFood,(rx-self.wFood//2,ry-self.hFood//2))
        cvzone.putTextRect(imgMain,f"Your Score: {self.score}",[50,80],scale=3,thickness=3,offset=10)

        if len(self.points) > 5:
            pts=np.array(self.points[:-5],np.int32)
            pts=pts.reshape((-1,1,2))
            cv2.polylines(imgMain,[pts],False,color=(255,0,0),thickness=3)
            minDist=cv2.pointPolygonTest(pts,(cx,cy),True)

            if -1<= minDist <=1:
                print("Hit")
                self.GameOver=True

        return imgMain

game=SnakeGameClass(r"C:\Users\ASUS\Desktop\ML Projects\Snake Game\laddu.png")
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    if hands:
        lmList=hands[0]['lmList']
        pointIndex=lmList[8][0:2]
        img = game.update(img,pointIndex)
    cv2.imshow("Image",img)
    
    key = cv2.waitKey(1)
    if key == ord('r'):
        game = SnakeGameClass(r"C:\Users\ASUS\Desktop\ML Projects\Snake Game\laddu.png")