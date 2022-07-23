import numpy as np
import cv2
import os

# 仔入模型
net = cv2.dnn.readNet("C:/Users/ximen/Dropbox/PC/Desktop/Demo/cfg/yolov4-tiny-obj.cfg",
                             "C:/Users/ximen/Dropbox/PC/Desktop/Demo/cfg/weight/yolov4-tiny-obj_final.weights")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416,416),scale=1/255.0)
model.setInputSwapRB(True)

#　載入分類名稱
with open('C:/Users/ximen/Dropbox/PC/Desktop/Demo/cfg/class.names', 'r') as file:
    label = file.read().splitlines()

# 預測
def Predict(img):
    classes, confs, boxes = model.detect(img,0.7, 0.5)
    return classes, confs, boxes

color = [(255,0,0),(0,255,0),(0,0,255)]
# 測試圖片位置
test_img = 'C:/Users/ximen/Dropbox/PC/Desktop/Demo/train'

for imgName in os.listdir(test_img):
    if(imgName[-3:] == 'jpg'):
        img = cv2.imread(test_img + '/' + imgName)
        classes, confs, boxes = Predict(img)
        for (classId, score, box) in zip(classes, confs, boxes):
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                          color=color[classId], thickness=2)

            text = '%s: %.2f' % (label[classId], score)
            cv2.putText(img, text, (box[0], box[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        color=color[classId], thickness=2)
        cv2.imshow('',img)

        if (cv2.waitKey(0) == 'n'):
            continue
