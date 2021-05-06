import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

img_path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\images_all\\gimp_cut\\male\\IMGP1107M.JPG"
# img_path = 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/images_all/IA_fond_blanc/1-1.JPG'
# img_path = 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/images_all/IA_fond_blanc/2.JPG'
# img_path = 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/images_all/IA_fond_blanc/3-3.JPG'

img = cv2.imread(img_path)

img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
import sys
sys.path.insert(0, 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho')
import Fonctions


class Points():
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


    def detect_eye(img):
        import cv2
        import numpy as np
        img_couleur = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray,21)
        circles1 = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=70,param2=65, minDist=100, minRadius=25,maxRadius=45)
        circles = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=100,param2=30, minDist=120, minRadius=80,maxRadius=95)
        circles = np.round(circles[0, :]).astype("int32")
        return circles1[0][0]


    '''
    * Routine pour détecter les points 3 et 19 (oeil)
    * input : image (type numpy.array)
    * return : pt3,pt19
    '''
    def points3_19(img):
        img = cv2.resize(img,(3500,2625))
        pupille = Points.detect_eye(img)
        # print("toto")
        # print(pupille)
        imgNB = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # imgNB = cv2.GaussianBlur(imgNB,(15,15),0)
        imgNB = cv2.addWeighted(imgNB, 4, imgNB, 0, 1)
        # plt.figure()
        # plt.imshow(imgNB,cmap="gray")
        # plt.show()
        #95 et minRAdius 30
        # 40 et minRadius 20
        circles = cv2.HoughCircles(imgNB, cv2.HOUGH_GRADIENT, 2.8, 300,minRadius=60,maxRadius=90)
        # circles = cv2.HoughCircles(imgNB, cv2.HOUGH_GRADIENT, 2.8, 300,minRadius=60,maxRadius=90)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
        listPotentiels = [x[0] for x in circles]

        i = Fonctions.Externes.find_nearest(listPotentiels,pupille[0])
        print(circles[i][0])
        # points 3 et 19
        # cv2.line(out,(circles[0][0],circles[0][1]),(circles[0][0]+circles[0][2],circles[0][1]),(255, 0, 0), 1)
        # cv2.line(out,(circles[0][0],circles[0][1]),(circles[0][0]-circles[0][2],circles[0][1]),(255, 0, 0), 1)
        # plt.imshow(out)
        # plt.show()
        pt3 = (circles[i][0]-circles[i][2],circles[i][1])
        pt19 = (circles[i][0]+circles[i][2],circles[i][1])
        print(pt3)
        print(pt19)
        return [pt3,pt19]
        # return circles





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
        approx = cv2.approxPolyDP(c,25,closed=True)
        # cv2.drawContours(out,approx,-1,(255,0,0),2)
        # cv2.polylines(imagerot, [approx], True, (255,0,0), 4)
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
            theta = Fonctions.Externes.calculAngleBis(triplet[0],triplet[1],triplet[2])
            anglePointsPotentiels.append(theta)
        [x9,y9] = listPointsPotentiels2[np.argmax(anglePointsPotentiels)]
        pt9 = (x9,y9)
        print(pt9)
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


    def points5_7(img,pt9,left):
        import scipy.signal
        from scipy.signal import savgol_filter
        from scipy import interpolate
        from scipy.interpolate import InterpolatedUnivariateSpline
        from scipy.signal import argrelextrema

        _,c = Points.contoursCorpsBig(img)
        approxBouche = cv2.approxPolyDP(c,0.1e-10,closed=False)

        approxBouche2 = []

        i=0
        for x in approxBouche:
            if (x[0][0]<pt9[0] and x[0][1]<left[1]):
                approxBouche2.append(x)
                i+=1
        approxBouche2 = np.asarray(approxBouche2)
        pt5 = [0,0]
        pt7 = [0,0]

        blank = np.ones_like(img)*255
        # cv2.polylines(blank, [approxBouche2], False, (255,0,0), 3)
        approxBouche2 = approxBouche2[:,0,:]
        # cv2.drawContours(img, [approxBouche2], -1, (0, 255, 0), 3)
        # plt.imshow(img)
        # print("toto")
        # print(approxBouche2)
        # plt.figure()
        # plt.plot(approxBouche2.T[0],-approxBouche2.T[1])
        # approxBouche2 = approxBouche[::2]
        approxBouche2 = np.array([list(approxBouche2[::2][i]) for i in range(len(approxBouche2)//2)])
        # print("toto")
        # print(approxBouche2)
        # cv2.drawContours(img, [approxBouche2], -1, (0, 0, 255), 1)
        # plt.imshow(img)
        abscisses = approxBouche2.T[0]
        ordonnees = approxBouche2.T[1]
        # plt.figure()
        # plt.plot(-ordonnees,-1*abscisses,'r',label='Contour bouche')

        #smoothing the contours of the mouth
        tck,u = interpolate.splprep([ordonnees,-1*abscisses],k=3,s=16)
        u=np.linspace(0,1,num=len(ordonnees),endpoint=True)
        outBouche = interpolate.splev(u,tck)
        # plt.plot(- outBouche[0], outBouche[1], 'b',label='Contour bouche lissé' )
        # plt.legend()
        # print(len(outBouche[0]))
        # print(outBouche[1])

        ''' zscore '''
        zscore=scipy.stats.zscore(outBouche[1])
        # print(len(outBouche[1]))
        input = zscore
        signal = (input > np.roll(input,1)) & (input > np.roll(input,-1))
        # plt.plot(input)
        # print(signal)
        # plt.plot(signal.nonzero()[0], input[signal], 'ro')
        # plt.plot(X2,F2)

        ''' wavelet transform and zerocrossing '''
        # import pywt
        # swt = pywt.swt(outBouche[1][:-1], 'rbio3.1')
        # cA = [x for x in swt[0][0]]
        # cD = [x for x in swt[0][1]]
        # # plt.figure()
        # # plt.plot(cD)
        # zc = np.where(np.diff(np.sign(cD)))[0]
        # # plt.figure()
        # # plt.plot(ordonnees,abscisses, 'b')
        # # plt.plot(ordonnees[zc+1],abscisses[zc+1],'ro')
        # print(zc)
        # # plt.figure()
        # # plt.plot(outBouche[0],zscore)
        # # plt.figure()

        '''find peak cwt'''
        peakind = scipy.signal.find_peaks(-1*abscisses,prominence=0.)
        # print(ordonnees)
        # print(peakind[0])
        # plt.figure()
        # plt.plot(ordonnees,-1*abscisses, 'b')
        # plt.plot(ordonnees[peakind[0]],-1*abscisses[peakind[0]],'ro')
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

        ''' distance to line'''
        pente =(approxBouche2[0][1]-left[1])/(approxBouche2[0][0]-left[0])
        intercept = approxBouche2[0][1]-pente*approxBouche2[0][0]
        xx = np.linspace(max(approxBouche2[0][0],left[0]),min(approxBouche2[0][0],left[0]),len(abscisses))
        yy = np.round(pente*xx+intercept)
        # print(pente)
        # print(intercept)
        # plt.figure()
        # plt.plot(xx,yy,'r')
        # plt.plot(xx,ordonnees,'b')
        projete = [np.round(Fonctions.Externes.projeteOrtho(pente,intercept,xx[i],ordonnees[i])) for i in range(len(xx))]
        projete = [x.flatten().tolist() for x in projete]
        xxx=np.array(projete).T[0]
        yyy = np.array(projete).T[1]
        # plt.plot(xx[10],ordonnees[10],'go')
        # plt.plot(projete[0],projete[1],'ko')
        # plt.plot(xxx,yyy,'g')
        # print("droite")
        # print(yy)
        # print("points")
        # # print(ordonnees)
        # print("projetés")
        # print(yyy)
        # erreur = [(yy[i]-ordonnees[i])**2 for i in range(len(yy))]
        erreur2 = [(yy[i]-yyy[i])**2 for i in range(len(yyy))]
        # print("erreur")
        # print(erreur2)
        # plt.figure()
        # plt.plot(xx,erreur)
        # plt.plot(xx,erreur2)

        print(np.max(erreur2))
        indx = np.argmax(erreur2)
        # plt.plot(xx[indx],ordonnees[indx],'yo')




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
        pt5 = (left[0],left[1])
        pt7 = (int(xx[indx]),int(ordonnees[indx]))
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
        # return swt


    def randomPoints():
        pt3 = [249.0, 250.0]
        pt5 = [122.0, 259.0]
        pt7 = [105.0, 312.0]
        pt9 = [207.0, 393.0]
        pt11 = [396.0, 415.0]
        pt13 = [414.0, 343.0]
        pt15 = [438.0, 239.0]
        pt17 = [473.0, 119.0]
        pt19 = [379.0, 248.0]
        corps= [pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19]
        echelle10mm = [[112,181],[300,186]]
        echelle3mm = [[67,74],[199,74]]
        return corps,echelle10mm,echelle3mm

    def randomPointsBis():
        pt3 = [1086.0, 1131.0]
        pt5 = [422.0, 509.0]
        pt7 = [405.0, 562.0]
        pt9 = [507.0, 643.0]
        pt11 = [396.0, 415.0]
        pt13 = [414.0, 343.0]
        pt15 = [438.0, 239.0]
        pt17 = [473.0, 119.0]
        pt19 = [679.0, 498.0]
        corps= [pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19]
        echelle10mm = [[112,181],[300,186]]
        echelle3mm = [[67,74],[199,74]]
        return corps,echelle10mm,echelle3mm

    def randomPointsContours(c):
        pt3 = [1086.0, 1131.0]
        pt5 = [422.0, 509.0]
        pt7 = [405.0, 562.0]
        pt9 = [507.0, 643.0]
        pt11 = [396.0, 415.0]
        pt13 = [414.0, 343.0]
        pt15 = [438.0, 239.0]
        pt17 = [473.0, 119.0]
        pt19 = [679.0, 498.0]
        corps= [pt3,pt5,pt7,pt9,pt11,pt13,pt15,pt17,pt19]
        echelle10mm = [[112,181],[300,186]]
        echelle3mm = [[67,74],[199,74]]
        return corps,echelle10mm,echelle3mm


    def contoursCorpsNew(img):
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # img_hsv = cv2.bilateralFilter(img_hsv,15,75,75)

        plt.figure()
        plt.imshow(img_hsv)



        low_tail = np.array([90, 30, 160])
        high_tail = np.array([110, 138, 220])
        mask_tail = cv2.inRange(img_hsv, low_tail, high_tail)
        mask_tail = 255-mask_tail
        res = cv2.bitwise_and(img, img, mask=mask_tail)
        res_b = res[:,:,0]
        res_g = res[:,:,1]
        res_r = res[:,:,2]
        res_b[np.where(res_b==0)] = 230
        res_g[np.where(res_g==0)] = 230
        res_r[np.where(res_r==0)] = 230
        res[:,:,0]= res_b
        res[:,:,1]= res_g
        res[:,:,2]= res_r
        res = cv2.medianBlur(res,11)
        res_hsv = cv2.cvtColor(res,cv2.COLOR_BGR2HSV)



        low_shadow = np.array([107,6,65])
        high_shadow = np.array([125,30,125])
        mask_shadow = cv2.inRange(res_hsv,low_shadow,high_shadow)
        mask_shadow = 255-mask_shadow
        res = cv2.bitwise_and(res, res, mask=mask_shadow)
        res_b = res[:,:,0]
        res_g = res[:,:,1]
        res_r = res[:,:,2]
        res_b[np.where(res_b==0)] = 230
        res_g[np.where(res_g==0)] = 230
        res_r[np.where(res_r==0)] = 230
        res[:,:,0]= res_b
        res[:,:,1]= res_g
        res[:,:,2]= res_r
        res = cv2.medianBlur(res,11)
        res_hsv = cv2.cvtColor(res,cv2.COLOR_BGR2HSV)

        # color = ('b','g','r')
        # plt.figure()
        # for i, col in enumerate(color):
        #     histr = cv2.calcHist([img],[i],None,[256],[0,255])
        #     plt.plot(histr,color = col,label=str(col))
        #     plt.xlim([0,256])
        # plt.legend()
        # color = ('h','s','v')
        # plt.figure()
        # for i, col in enumerate(color):
        #     histr = cv2.calcHist([img_hsv],[i],None,[256],[0,255])
        #     plt.plot(histr,label=str(col))
        #     plt.xlim([0,256])
        # plt.legend()
        res_hsv_bgr = cv2.cvtColor(res_hsv,cv2.COLOR_HSV2BGR)
        res_hsv_gr = cv2.cvtColor(res_hsv_bgr,cv2.COLOR_BGR2GRAY)
        res_hsv_gr = cv2.dilate(res_hsv_gr,kernel = np.ones((5,5),np.uint8),iterations=3)
        # plt.imshow(res_hsv_gr)
        # plt.show()
        img_out1 = cv2.adaptiveThreshold(res_hsv_gr,220,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,21,2)
        plt.figure()
        plt.imshow(img_out1)
        # plt.figure()
        # plt.imshow(img_out2)
        # plt.figure()
        # plt.imshow(img)
        # plt.figure()
        # plt.imshow(img_hsv)
        plt.figure()
        plt.imshow(res)
        plt.show()
    def points11_17(img,pt13,pt15):
        _,c = Points.contoursCorpsBig(img)
        approxCorps = cv2.approxPolyDP(c,0.0000001,closed=False)
        slope = (pt15[1]-pt13[1])/(pt15[0]-pt13[0])
        slopes = []
        for p11 in approxCorps:
            p11 = list(p11[0])
            if (pt13[0]-p11[0]!=0):
                pente = (pt13[1]-p11[1])/(pt13[0]-p11[0])
                slopes.append(pente)
        slopes = [-1*(slopes[i] - slope)**2 for i in range(len(slopes))]
        slopes = [-30 if x<-30 else x for x in slopes]
        # print(slopes)
        x = np.arange(len(slopes))
        # plt.figure()
        # plt.plot(x,slopes)
        from scipy.signal import find_peaks, peak_prominences
        peaks, _ = find_peaks(slopes,distance=300)
        pt11 = list(approxCorps[peaks[0]][0])
        pt17 = list(approxCorps[peaks[1]][0])
        print(pt11)
        print(pt17)
        return pt11,pt17

    def centerPoint(pt,eye):
        return [pt[0]-(eye[0]-300),pt[1]-(eye[1]-250)]

    def decenterPoint(A,eye):
        return [A[0]+eye[0]-300,A[1]+eye[1]-250]

    def centerPoints(lstpt,eye):
        new_lstpt = []
        for x in lstpt:
            new_lstpt.append(Points.centerPoint(x,eye))
        return new_lstpt

    def ImageCorps(imgPIL):
        from PIL import Image
        PIL_image = imgPIL.resize((1300,975), Image.ANTIALIAS)
        CV2_image = np.array(imgPIL)
        out,c = Points.contoursCorps(CV2_image)
        [left,right,top,bottom] = Points.pointExtremeContours(c)
        imagerot = Points.rotate_image(out,Points.angleRot(left,right)[0],Points.angleRot(left,right)[1])
        _,c = Points.contoursCorps(imagerot)
        [left,right,top,bottom] = Points.pointExtremeContours(c)
        corpsStandard = [[left[0],left[1]],[top[0],top[1]],[right[0],right[1]],[bottom[0],bottom[1]]]
        newPIL_image = Image.fromarray(imagerot)
        return corpsStandard,newPIL_image,left

    def ImageTete(imgPIL):
        from PIL import Image
        PIL_image_big = imgPIL.resize((3500,2625), Image.ANTIALIAS)
        PIL_image_big = np.flip(PIL_image_big,axis=2)
        CV2_image_big = np.array(PIL_image_big)
        CV2_image_big = CV2_image_big[:, :, ::-1].copy()
        out,c = Points.contoursCorpsBig(CV2_image_big)
        [left1,right1,top,bottom] = Points.pointExtremeContours(c)
        CV2_image_big = Points.rotate_image(out,Points.angleRot(left1,right1)[0],Points.angleRot(left1,right1)[1])
        _,c = Points.contoursCorpsBig(CV2_image_big)
        [left1,_,_,_] = Points.pointExtremeContours(c)
        print("\n### Chargement de l'image de la tête' ###")
        PIL_image_big = Image.fromarray(CV2_image_big)
        return PIL_image_big,CV2_image_big,left1
'''
*
* Main function
*
'''

# plt.figure()
# plt.imshow(img)
# plt.show()
# Points.contoursCorpsNew(img)
# plt.figure()
# plt.imshow(out)
# plt.show()
#
# # # # #
out,c = Points.contoursCorpsBig(img)
[left,right,top,bottom] = Points.pointExtremeContours(c)
imagerot = Points.rotate_image(out,Points.angleRot(left,right)[0],Points.angleRot(left,right)[1])
# #
_,c = Points.contoursCorpsBig(imagerot)
[left,right,top,bottom] = Points.pointExtremeContours(c)
print("left")
print(left)
# #
#
[pt3,pt19]=Points.points3_19(imagerot)
print(pt3)
print(pt19)
# circles = Points.points3_19(imagerot)
print("pt9")
pt9 = Points.point9(c,pt19)
#
# #ne fonctionne pas pour l'instant
# [pt15,pt13] =Points.points15_13(imagerot)
# pt13 = (1288, 1228)
# pt15 = (1308, 1098)
# cv2.circle(imagerot, pt15, 20, (255, 0, 0), -1)
# cv2.circle(imagerot, pt13, 20, (255, 0, 0), -1)
#
# pt5,pt7 = Points.points5_7(imagerot,pt9)
pt5,pt7= Points.points5_7(imagerot,pt9,left)
#
# pt11,pt17 = Points.points11_17(imagerot,pt13,pt15)
# pt11 = (pt11[0],pt11[1])
# pt17 = (pt17[0],pt17[1])
# cv2.circle(imagerot, left, 12, (0, 50, 255), -1)
# cv2.circle(imagerot, right, 12, (0, 255, 255), -1)
# cv2.circle(imagerot, top, 12, (255, 50, 0), -1)
# cv2.circle(imagerot, bottom, 12, (255, 255, 0), -1)
cv2.circle(imagerot, pt3, 4, (255, 0, 0), -1)
cv2.circle(imagerot, pt19, 4, (255, 0, 0), -1)
cv2.circle(imagerot, pt9, 8, (255, 0, 0), -1)
cv2.circle(imagerot, pt5, 8, (0, 255, 0), -1)
cv2.circle(imagerot, pt7, 8, (0, 255, 0), -1)
# cv2.circle(imagerot, pt11, 8, (0, 255, 0), -1)
# cv2.circle(imagerot, pt17, 8, (0, 255, 0), -1)
# plt.figure()
plt.imshow(imagerot)
plt.show()
#(


#

