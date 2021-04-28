import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

img_path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\gimp_cut\\male\\IMGP1152M.JPG"
img = cv2.cvtColor(cv2.imread(img_path),cv2.COLOR_BGR2RGB)

'''
* Méthode pour obtenir le contours du poisson
* input : image img (type numpy.array) de taille 4000x3000 (ou même ratio) --> 1300x975
* return : contours c (type numpy.array)
'''
def contoursCorps(img):
    diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    diamond[0, 0] = 0
    diamond[0, 1] = 0
    diamond[1, 0] = 0
    diamond[4, 4] = 0
    diamond[4, 3] = 0
    diamond[3, 4] = 0
    diamond[4, 0] = 0
    diamond[4, 1] = 0
    diamond[3, 0] = 0
    diamond[0, 3] = 0
    diamond[0, 4] = 0
    diamond[1, 4] = 0
    #avant 1500 1125
    #apres 1300 975
    img = cv2.resize(img,(1300,975))
    dst = cv2.addWeighted(img, 2, img, 0, 2)
    # plt.figure()
    # plt.imshow(dst)
    dst = cv2.resize(dst,(1300,975))
    dst = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
    closing = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, diamond,iterations=1)
    dilated = cv2.dilate(closing,diamond,iterations=1)
    blured = cv2.medianBlur(dilated,ksize=1)
    binarized = cv2.threshold(blured,245,250,cv2.THRESH_BINARY)[1]
    # plt.figure()
    # plt.imshow(binarized,cmap='gray')
    contours, hierarchy = cv2.findContours(binarized,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    list_area = [cv2.contourArea(c) for c in contours]
    for c in contours:
        area = cv2.contourArea(c)
        if area < 100:
            cv2.fillPoly(binarized, pts=[c], color=0)
            continue
    binarized = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4)));
    imgcopy = img.copy()
    imgcopy2 = np.copy(img)
    # plt.imshow(binarized,cmap='gray')
    contours2, hierarchy2 = cv2.findContours(binarized,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # plt.figure()
    # plt.imshow(imgcopy2,cmap="gray")
    cv2.drawContours(imgcopy2,contours2,-1,(255,0,0),4)
    # plt.figure()
    # plt.imshow(imgcopy2,cmap="gray")
    list_area2 = [cv2.contourArea(c) for c in contours2]
    drawing = np.ones((img.shape[0], img.shape[1], 3), np.uint8)*255
    cv2.fillPoly(drawing,pts=contours2,color=(0,0,0))
    drawing = cv2.dilate(drawing,diamond,iterations=1)
    # plt.figure()
    # plt.imshow(drawing)
    drawing = cv2.morphologyEx(drawing, cv2.MORPH_CLOSE, diamond,iterations=5)
    # plt.figure()
    # plt.imshow(drawing,cmap="gray")
    contours3, hierarchy3 = cv2.findContours(cv2.cvtColor(drawing,cv2.COLOR_BGR2GRAY),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Affichage du plus grand contours
    # cv2.drawContours(img, max(contours3, key = cv2.contourArea), -1, (0,255,0), 3)
    # plt.imshow(img)
    # plt.show()
    out_mask = np.zeros_like(img)
    contours3 = sorted(contours3, key=cv2.contourArea)
    out=img.copy()
    # cv2.drawContours(out, [contours3[-1]], -1, (255,0,0), 3)
    # out[out_mask == 0] = 255
    c=max(contours3, key=cv2.contourArea)
    return out,c


def contoursCorpsBig(img):
    diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    diamond[0, 0] = 0
    diamond[0, 1] = 0
    diamond[1, 0] = 0
    diamond[4, 4] = 0
    diamond[4, 3] = 0
    diamond[3, 4] = 0
    diamond[4, 0] = 0
    diamond[4, 1] = 0
    diamond[3, 0] = 0
    diamond[0, 3] = 0
    diamond[0, 4] = 0
    diamond[1, 4] = 0
    #avant 1500 1125
    #apres 1300 975
    img = cv2.resize(img,(3500,2625))
    dst = cv2.addWeighted(img, 2, img, 0, 2)
    # plt.figure()
    # plt.imshow(dst)
    dst = cv2.resize(dst,(3500,2625))
    dst = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
    closing = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, diamond,iterations=1)
    dilated = cv2.dilate(closing,diamond,iterations=1)
    blured = cv2.medianBlur(dilated,ksize=1)
    binarized = cv2.threshold(blured,245,250,cv2.THRESH_BINARY)[1]
    # plt.figure()
    # plt.imshow(binarized,cmap='gray')
    contours, hierarchy = cv2.findContours(binarized,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    list_area = [cv2.contourArea(c) for c in contours]
    for c in contours:
        area = cv2.contourArea(c)
        if area < 100:
            cv2.fillPoly(binarized, pts=[c], color=0)
            continue
    binarized = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4)));
    imgcopy = img.copy()
    imgcopy2 = np.copy(img)
    # plt.imshow(binarized,cmap='gray')
    contours2, hierarchy2 = cv2.findContours(binarized,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # plt.figure()
    # plt.imshow(imgcopy2,cmap="gray")
    # cv2.drawContours(imgcopy2,contours2,-1,(255,0,0),4)
    # plt.figure()
    # plt.imshow(imgcopy2,cmap="gray")
    list_area2 = [cv2.contourArea(c) for c in contours2]
    drawing = np.ones((img.shape[0], img.shape[1], 3), np.uint8)*255
    cv2.fillPoly(drawing,pts=contours2,color=(0,0,0))
    drawing = cv2.dilate(drawing,diamond,iterations=1)
    # plt.figure()
    # plt.imshow(drawing)
    drawing = cv2.morphologyEx(drawing, cv2.MORPH_CLOSE, diamond,iterations=5)
    # plt.figure()
    # plt.imshow(drawing,cmap="gray")
    contours3, hierarchy3 = cv2.findContours(cv2.cvtColor(drawing,cv2.COLOR_BGR2GRAY),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Affichage du plus grand contours
    # cv2.drawContours(img, max(contours3, key = cv2.contourArea), -1, (0,255,0), 3)
    # plt.imshow(img)
    # plt.show()
    out_mask = np.zeros_like(img)
    contours3 = sorted(contours3, key=cv2.contourArea)
    out=img.copy()
    # cv2.drawContours(out, [contours3[-1]], -1, (255,0,0), 3)
    # out[out_mask == 0] = 255
    c=max(contours3, key=cv2.contourArea)
    return out,c


'''
* Méthode pour avoir les 4 points extrêmes du poisson
* input : contours c (type numpy.array) issu de l'image 1300x975
* return : [left,right,top,bottom] (type list of numpy.array)
'''
def pointExtremeContours(c):
    left = tuple(c[c[:, :, 0].argmin()][0])
    right = tuple(c[c[:, :, 0].argmax()][0])
    top = tuple(c[c[:, :, 1].argmin()][0])
    bottom = tuple(c[c[:, :, 1].argmax()][0])
    return [left,right,top,bottom]





'''
* Méthode pour avoir l'angle de rotation
* input : points left et right (type tuple) issu de l'image 1300x975
* return : angle (type float en degrés) et centre (type tuple of float)
'''
def angleRot(left,right):
    # rotate with angle to properly have top and bottom
    x1,y1 = left
    x2,y2 = right
    m=(y2-y1)/(x2-x1)
    angle = math.atan2(m,1)*180/math.pi
    centre = ((x1+x2)/2,(y1+y2)/2)
    return [angle,centre]





'''
* Méthode pour repencher l'image si necessaire
* input : image (type numpy.array) 1300x975, angle (type float en degrés), center (list of float)
* return : result (type numpy.array)
'''
def rotate_image(image, angle,center):
  rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR,borderValue=(255,255,255))
  return result





'''
* Routine pour détecter les points 3 et 19 (oeil)
* input : image (type numpy.array)
* return : pt3,pt19
'''
def points3_19(img):
    img = cv2.resize(img,(3500,2625))
    imgNB = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # imgNB = cv2.GaussianBlur(imgNB,(15,15),0)
    imgNB = cv2.addWeighted(imgNB, 4, imgNB, 0, 1)
    # plt.figure()
    # plt.imshow(imgNB,cmap="gray")
    # plt.show()
    #95 et minRAdius 30
    # 40 et minRadius 20
    circles = cv2.HoughCircles(imgNB, cv2.HOUGH_GRADIENT, 2, 100,minRadius=65,maxRadius=85)
    print(circles)
    # print(circles)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
    # points 3 et 19
    # cv2.line(out,(circles[0][0],circles[0][1]),(circles[0][0]+circles[0][2],circles[0][1]),(255, 0, 0), 1)
    # cv2.line(out,(circles[0][0],circles[0][1]),(circles[0][0]-circles[0][2],circles[0][1]),(255, 0, 0), 1)
    # plt.imshow(out)
    # plt.show()
    pt3 = (circles[0][0]-circles[0][2],circles[0][1])
    pt19 = (circles[0][0]+circles[0][2],circles[0][1])
    print(pt3)
    print(pt19)
    return [pt3,pt19]





''' Méthode calculant la distance euclidienne entre deux points '''
def euclideDist(a,b):
  import numpy as np
  x1 = a[0]
  y1 = a[1]
  x2 = b[0]
  y2 = b[1]
  norme = np.sqrt((x2-x1)**2+(y2-y1)**2)
  return norme






''' Méthode calculant l'angle par la loi des cosinus '''
def calculAngle(pt1,pt2,pt3):
  #calcul par alkashi des angles en degres du triangle reliant les 3 points
  #        pt2
  #     b /     \ a
  #  pt1 ----- pt3
  #         c
  #angle au niveau du pt2
  b = euclideDist(pt1,pt2)
  a = euclideDist(pt2,pt3)
  c = euclideDist(pt1,pt3)
  from math import acos,pi
  Apt2 = acos((b**2+a**2-c**2)/(2*b*a))*180/pi
  return Apt2







'''
* Routine pour détecter le point 9 (menton)
* input : contours (type numpy.array), pt19 (tuple of float)
* return : pt9
'''
def point9(c,pt19):
  approx = cv2.approxPolyDP(c,20,closed=True)
  # cv2.drawContours(out,approx,-1,(255,0,0),2)
  # cv2.polylines(imagerot, [approx], True, (255,0,0), 1)
  # approx = approx.flatten()
  x19,y19 = pt19
  # plt.imshow(imagerot)
  # plt.show()
  approxM = np.matrix(approx)
  listPointsPotentiels = np.where(np.logical_and(approxM[:,0]<x19,approxM[:,1]>y19)==True)[0]
  listPointsPotentiels2 = []
  listPointsPotentiels2_aug = []
  anglePointsPotentiels = []
  for i in range(len(listPointsPotentiels)):
    index = listPointsPotentiels[i]
    listPointsPotentiels2.append(list(approx[index][0]))
    listPointsPotentiels2_aug.append([list(approx[index-1][0]),list(approx[index][0]),list(approx[(index+1)%(len(approx))][0])])
  for triplet in listPointsPotentiels2_aug:
    theta = calculAngle(triplet[0],triplet[1],triplet[2])
    anglePointsPotentiels.append(theta)
  [x9,y9] = listPointsPotentiels2[np.argmax(anglePointsPotentiels)]
  pt9 = (x9,y9)
  return pt9






'''
* Routine pour détecter les points 15 et 13 (ouverture bronchiale)
* input : img (type numpy.array)
* return : pt15,pt13 (type tuple of tuple)
'''

def points15_13(img):
    # img = cv2.medianBlur(img,7)
    img = cv2.GaussianBlur(img,(7,7),0)
    img = cv2.addWeighted(img, 2, img, 0, -2)

    # plt.figure()
    # plt.imshow(img)
    img = cv2.threshold(img,40,255,cv2.THRESH_TOZERO)[1]

    # img = cv2.GaussianBlur(img,(11,11),0)

    # plt.figure()
    # plt.imshow(img)


    '''valeurs du filtre canny : 30,40'''
    edges = cv2.Canny(img,10,30)
    edgecopy = edges.copy()
    # plt.figure()
    # plt.imshow(edges,cmap="gray")
    # img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=15, minLineLength=35, maxLineGap=30)
    # lines = cv2.HoughLinesP(grad, rho=1, theta=np.pi/180, threshold=40, minLineLength=100, maxLineGap=45)

    pointsbronchie = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = abs((y2-y1)/(x2-x1))
            # print(slope)
            if(slope > 3):
                # print(slope)
                # cv2.line(out, (x1, y1), (x2, y2), (255, 0, 0), 3)
                pointsbronchie.append(x1)
                pointsbronchie.append(x2)
                pointsbronchie.append(y1)
                pointsbronchie.append(y2)

    # plt.figure()
    # plt.imshow(out)
    # plt.show()
    pt15 = (x1,y1)
    pt13 = (x2,y2)
    return pt15,pt13


def points5_7(img,pt9):
    import scipy.signal
    from scipy.signal import savgol_filter
    from scipy import interpolate
    from scipy.interpolate import InterpolatedUnivariateSpline
    from scipy.signal import argrelextrema



    _,c = contoursCorpsBig(img)
    approxBouche = cv2.approxPolyDP(c,0.00001,closed=False)
    approxBouche2 = []

    i=0
    for x in approxBouche:
        if x[0][0]<pt9[0]:
            approxBouche2.append(x)
            i+=1
    approxBouche2 = np.asarray(approxBouche2)

    pt5 = [0,0]
    pt7 = [0,0]

    blank = np.ones_like(img)*255
    # cv2.polylines(blank, [approxBouche2], False, (255,0,0), 3)
    approxBouche2 = approxBouche2[:,0,:]
    abscisses = approxBouche2.T[0]
    ordonnees = approxBouche2.T[1]
    # plt.figure()
    # plt.plot(ordonnees,abscisses,'r.',label='Contour bouche')

    #smoothing the contours of the mouth
    tck,u = interpolate.splprep([ordonnees,abscisses],k=3,s=16)
    u=np.linspace(0,1,num=len(ordonnees),endpoint=True)
    outBouche = interpolate.splev(u,tck)
    # plt.plot(outBouche[0], outBouche[1], 'b',label='Contour bouche lissé' )
    # plt.legend()
    # print(len(outBouche[0]))

    # compute the 1st derivative
    f_prime = np.gradient (outBouche[1])
    # plt.figure()
    # plt.plot(outBouche[0],f_prime,label='dérivée première')
    # smoothing the 1st derivative
    tck,u = interpolate.splprep([outBouche[0],f_prime],k=3,s=5)
    u=np.linspace(0,1,num=len(f_prime),endpoint=True)
    out = interpolate.splev(u,tck)
    # print(len(out[0]))

    # plt.figure()
    # plt.plot(out[0],out[1],label='dérivée première lissée')
    # plt.legend()

    # compute the 2nd derivative
    f_second = np.gradient(out[1])
    # plt.figure()
    # plt.plot(out[0],f_second,label='dérivée 2nd lissée')

    # indices = np.where (np.diff (np.sign (f_prime))) [0] # Find the inflection point.
    infls = np.where(np.diff(np.sign(f_second)))[0]
    # print(len(infls))
    # print(infls)
    # plt.figure()
    # plt.plot(outBouche[0],outBouche[1],'r.',label='Contour bouche')

    local_maxima = argrelextrema(outBouche[1], np.less, order = 10, mode = 'wrap')
    # print(list(local_maxima))
    mini = np.argmin(abscisses)
    # for i, infl in enumerate(list(local_maxima[0]), 1):
        # plt.axvline(x=ordonnees[infl], color='k', label=f'Inflection Point {i}')
    local_maxima = list(local_maxima[0])[0]
    # print(local_maxima)

    # av erifier
    pt5 = (abscisses[mini],ordonnees[mini])

    pt7 = (abscisses[local_maxima],ordonnees[local_maxima])
    print("pt5")
    print(pt5)
    print("pt7")
    print(pt7)
    # plt.axvline(x=ordonnees[mini],color='k')
    # print(local_maxima)
    # plt.plot(yhat)'
    # plt.figure()
    # plt.imshow(img)
    # plt.legend()

    # plt.show()
    return pt5,pt7



'''
*
* Main function
*
'''


# out,c = contoursCorpsBig(img)

# #
# # out,c = contoursCorps(img)
# [left,right,top,bottom] = pointExtremeContours(c)
# imagerot = rotate_image(out,angleRot(left,right)[0],angleRot(left,right)[1])
# #
# _,c = contoursCorpsBig(imagerot)
# [left,right,top,bottom] = pointExtremeContours(c)
# #
#
# [pt3,pt19]=points3_19(imagerot)
#
#
# pt9 = point9(c,pt19)
#
# #ne fonctionne pas pour l'instant
# # [pt15,pt13] = points15_13(imagerot)
# # cv2.circle(imagerot, pt15, 4, (255, 0, 0), -1)
# # cv2.circle(imagerot, pt13, 4, (255, 0, 0), -1)
#
# pt5,pt7 = points5_7(imagerot,pt9)
#


# cv2.circle(imagerot, left, 12, (0, 50, 255), -1)
# cv2.circle(imagerot, right, 12, (0, 255, 255), -1)
# cv2.circle(imagerot, top, 12, (255, 50, 0), -1)
# cv2.circle(imagerot, bottom, 12, (255, 255, 0), -1)
# cv2.circle(imagerot, pt3, 12, (255, 0, 0), -1)
# cv2.circle(imagerot, pt19, 12, (255, 0, 0), -1)
# cv2.circle(imagerot, pt9, 12, (255, 0, 0), -1)
# cv2.circle(imagerot, pt5, 8, (0, 255, 0), -1)
# cv2.circle(imagerot, pt7, 8, (0, 255, 0), -1)
# plt.imshow(imagerot)
# plt.show()
#


#

