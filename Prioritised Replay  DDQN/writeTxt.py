import os

train_path = "C:/Users/ximen/Dropbox/PC/Desktop/Demo/train"
val_path = "C:/Users/ximen/Dropbox/PC/Desktop/Demo/val"

with open('val.txt','a') as file:
    for fileName in os.listdir(val_path):
        if fileName[-3:] == 'jpg':
            file.writelines(val_path + '/' + fileName + '\n')
