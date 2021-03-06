import cv2
import mediapipe as mp
import numpy as np
import serial,os
from time import sleep
s=serial.Serial("/dev/cu.usbserial-14310",9600)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
dict_min = {
    "left":[],
    "right":[]
    }
left_min = 0.8371902799606323
right_min = 0.819582531452179

cap = cv2.VideoCapture("/Users/taikikimura/Desktop/mymovie.mp4")
pose= mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
while True:
    success, image = cap.read()
    try:
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
    
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('MediaPipe Pose', image)
        #各種座標をkeypointsという配列内に辞書形で格納している
        keypoints = []
        for data_point in results.pose_landmarks.landmark:
            keypoints.append({
                                'X': data_point.x,
                                'Y': data_point.y,
                                'Z': data_point.z,
                                'Visibility': data_point.visibility,
                                })
        print(keypoints[31])
        #各足の足先の座標を取得し、その座標から足を踏み込んでいるか判断する
        left_toe = keypoints[31]
        right_toe = keypoints[32]
        dict_min["left"].append(left_toe["Y"])
        dict_min["right"].append(right_toe["Y"])
        send_list = ""
        if left_toe["Y"] < left_min:
            if right_toe["Y"] < right_min:
                send_list = "0" #どちらも
            else:
                send_list = "1" #左だけ
        else:
            if right_toe["Y"] < right_min:
                send_list = "2" #右だけ
            else:
                send_list = "3" #どちらもなし

        s.write(str.encode(send_list))
        

        #print(len(keypoints))
        if cv2.waitKey(5) & 0xFF == 27:
            break
    except:
        print("fin")
        s.write(str.encode("3"))
        break

#動画全体の足先の座標から四分位を算出する
#踏み込んでいる座標を全体で記録された座標中の第一四分位数以下の座標とする

q75, q25 = np.percentile(dict_min["left"], [75 ,25])
iqr = q75 - q25
print("最低値",min(dict_min["left"]))
print("25パーセント点", q25)
print("75パーセント点", q75)
print("四分位範囲", iqr)
q75, q25 = np.percentile(dict_min["right"], [75 ,25])
iqr = q75 - q25
print("最低値",min(dict_min["right"]))
print("25パーセント点", q25)
print("75パーセント点", q75)
print("四分位範囲", iqr)
cap.release()
