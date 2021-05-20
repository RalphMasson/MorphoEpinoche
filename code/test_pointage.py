import cv2
import matplotlib.pyplot as plt
import numpy as np

IMG_POINTE = cv2.imread("C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_pointe\\Dataset1\\IMGP1862M.JPG")
IMG_POINTE = cv2.cvtColor(IMG_POINTE,cv2.COLOR_BGR2RGB)

IMG_DETOURE = cv2.imread("C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_detoure\\Dataset1\\IMGP1862M.JPG")
IMG_DETOURE = cv2.cvtColor(IMG_DETOURE,cv2.COLOR_BGR2RGB)
IMG_DETOURE = cv2.resize(IMG_DETOURE,(4000,3000))

IMG_DETOURE_gray = cv2.cvtColor(IMG_DETOURE, cv2.COLOR_RGB2GRAY)
mask = cv2.compare(IMG_DETOURE_gray,5,cv2.CMP_LT)
IMG_DETOURE[mask > 0] = 255

IMG_POINTE_hsv = cv2.cvtColor(IMG_POINTE,cv2.COLOR_RGB2HSV)
lower = np.array([0,230,230])
upper = np.array([1,255,255])
mask = cv2.inRange(IMG_POINTE_hsv, lower, upper)
IMG_DETOURE[mask != 0] = [255,0,0]

def grossir_point(iterations):
    for k in range(iterations):
        IMG_DETOURE_hsv = cv2.cvtColor(IMG_DETOURE,cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(IMG_DETOURE_hsv, lower, upper)
        x_red = np.where(mask!=0)[0]
        y_red = np.where(mask!=0)[1]
        for i in range(len(x_red)):
            IMG_DETOURE[x_red[i]-1][y_red[i]+1] = [255,0,0]
            IMG_DETOURE[x_red[i]][y_red[i]+1] = [255,0,0]
            IMG_DETOURE[x_red[i]+1][y_red[i]+1] = [255,0,0]
            IMG_DETOURE[x_red[i]-1][y_red[i]] = [255,0,0]
            IMG_DETOURE[x_red[i]+1][y_red[i]] = [255,0,0]
            IMG_DETOURE[x_red[i]-1][y_red[i]-1] = [255,0,0]
            IMG_DETOURE[x_red[i]][y_red[i]-1] = [255,0,0]
            IMG_DETOURE[x_red[i]+1][y_red[i]-1] = [255,0,0]

grossir_point(5)

plt.figure()
plt.imshow(IMG_POINTE)
plt.figure()
plt.imshow(IMG_DETOURE)
plt.show()