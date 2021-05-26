''' Bibliothèque de fonctions de placement '''

import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

# img_path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\images_all\\gimp_cut\\male\\IMGP1152M.JPG"
# img_path = 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/images_all/IA_fond_blanc/1-1.JPG'
# img_path = 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/images_all/IA_fond_blanc/2.JPG'
# img_path = 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/images_all/IA_fond_blanc/3-3.JPG'
# # #
# # # male_path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\images_all\\gimp_cut\\male\\"
# # # import sys,os
# # # male_img = os.listdir(male_path)
# # # male_img = [male_path+x for x in male_img]
''' TESTE AVEC FEMALE 1220F.JPG '''
img_path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_final\\Dataset1\\IMGP1895M.JPG"
# img = cv2.imread(img_path)
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

import sys,inspect
sys.path.insert(0,'/'.join(inspect.stack()[0][1].split('\\')[:-1]))
import Fonctions

class Points():

    def contoursCorps(img,param):
        """!
        Méthode pour obtenir le contours du poisson
        @param image img (type numpy.array) de taille 4000x3000 (ou même ratio) --> 1300x975
        @param size : 'head' 'body' (1300,975) or (3500,2625)
        @return contours c (type numpy.array)
        """
        if param=='head':size=(3500,2625)
        if param=='body':size=(1300,975)
        diamond = Fonctions.Externes.diamondCV2()
        img = cv2.resize(img,size)
        # dst = cv2.addWeighted(img, 2, img, 0, 2)
        # plt.figure()
        # plt.imshow(dst)
        dst=img
        dst = cv2.resize(dst,size)
        dst = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        closing = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, diamond,iterations=1)
        dilated = cv2.dilate(closing,diamond,iterations=1)
        blured = cv2.medianBlur(dilated,ksize=1)
        binarized = cv2.threshold(blured,253,255,cv2.THRESH_BINARY)[1]
        # print(binarized)
        # binarized = blured
        # plt.figure()
        # plt.imshow(binarized,cmap='gray')
        # plt.show()
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

    def pointExtremeContours(c):
        """!
        Méthode pour avoir les 4 points extrêmes du poisson
        @param contours c (type numpy.array) issu de l'image 1300x975
        @return [left,right,top,bottom] (type list of numpy.array)
        """
        left = tuple(c[c[:, :, 0].argmin()][0])
        right = tuple(c[c[:, :, 0].argmax()][0])
        top = tuple(c[c[:, :, 1].argmin()][0])
        bottom = tuple(c[c[:, :, 1].argmax()][0])
        return [left,right,top,bottom]


    def angleRot(left,right):
        """!
        Méthode pour avoir l'angle de rotation
        @param points left et right (type tuple) issu de l'image 1300x975
        @return angle (type float en degrés) et centre (type tuple of float)
        """
        # rotate with angle to properly have top and bottom
        x1,y1 = left
        x2,y2 = right
        m=(y2-y1)/(x2-x1)
        angle = math.atan2(m,1)*180/math.pi
        centre = ((x1+x2)/2,(y1+y2)/2)
        return [angle,centre]


    def rotate_image(image, angle,center):
        """!
        Méthode pour repencher l'image si necessaire
        @param image (type numpy.array) 1300x975, angle (type float en degrés), center (list of float)
        @return result (type numpy.array)
        """
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR,borderValue=(255,255,255))
        return result


    def detect_eye(img):
        """!
        Méthode pour détecter la pupille
        @param img (type numpy.array)
        @return circles1[0][0] : centre de la pupille (type tuple)
        """
        img_couleur = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray,21)
        circles1 = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=70,param2=65, minDist=100, minRadius=25,maxRadius=45)
        circles = cv2.HoughCircles(image=img_gray, method=cv2.HOUGH_GRADIENT, dp=2,param1=100,param2=30, minDist=120, minRadius=80,maxRadius=95)
        circles = np.round(circles[0, :]).astype("int32")
        return circles1[0][0]

    def points3_19_independant(img):
        from scipy.signal import savgol_filter
        from scipy.signal import find_peaks,argrelextrema

        img = cv2.resize(img,(3500,2625))
        pupille = Points.detect_eye(img)
        imgNB = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgNB = cv2.erode(imgNB,(5,5),iterations=10)
        pt3 = [pupille[0]-2,pupille[1]]
        pt19 = [pupille[1]+2,pupille[1]]
        longueur_deplacement = np.linspace(0,180,181)
        #imgNB[y][x]
        intensite_est = savgol_filter([imgNB[int(pt3[1])][int(pt3[0]+x)] for x in longueur_deplacement],61,6)
        intensite_ouest = savgol_filter([imgNB[int(pt3[1])][int(pt3[0]-x)] for x in longueur_deplacement],61,6)
        intensite_est = [x if x<150 else 150 for x in intensite_est]
        intensite_ouest = [x if x<150 else 150 for x in intensite_ouest]
        intensite_est = [x if x>80 else 80 for x in intensite_est]
        intensite_ouest = [x if x>80 else 80 for x in intensite_ouest]

        peaks1, _ = find_peaks(intensite_est, prominence=1)
        print(peaks1)

        plt.figure()
        plt.plot(longueur_deplacement,intensite_est)
        ordo1 = [intensite_est[peak1] for peak1 in peaks1]
        plt.plot(peaks1, ordo1, "x")
        print(np.mean(intensite_est))
        print(np.median(intensite_est))
        plt.title("Est")
        plt.grid(True)

        peaks2, _ = find_peaks(intensite_ouest,prominence=1)

        plt.figure()
        plt.plot(longueur_deplacement,intensite_ouest)
        ordo2 = [intensite_est[peak2] for peak2 in peaks2]
        print(np.mean(intensite_ouest))
        print(np.median(intensite_ouest))
        plt.plot(peaks2, ordo2, "x")
        plt.title("Ouest")
        plt.grid(True)

        # cv2.circle(imgNB,(int(pupille[0]),int(pupille[1])),180,(255,0,0),3)
        # cv2.circle(imgNB,(int(pupille[0]),int(pupille[1])),2,(255,0,0),3)
        # plt.figure()
        # plt.imshow(imgNB)
        plt.show()

    def points3_19(img):
        """!
        Routine pour détecter les points 3 et 19 (oeil)
        @param image (type numpy.array)
        @return pt3,pt19
        """
        img = cv2.resize(img,(3500,2625))
        print(img[:,:,0][1000][1500])
        pupille = Points.detect_eye(img)
        # # print("toto")
        print(pupille)
        imgNB = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # imgNB = cv2.GaussianBlur(imgNB,(15,15),0)
        imgNB = cv2.addWeighted(imgNB, 4, imgNB, 0, 1)
        # # print(imgNB[1000][1500])
        # # print(imgNB[1000][1505])
        # # print(imgNB[1000][1510])
        # # print(imgNB[1000][1511])
        # # print(imgNB[1000][1512])
        # # print(imgNB[1000][1513])
        # # print(imgNB[1000][1514])
        # # print(imgNB[1001][1500])
        # # print(imgNB[1001][1505])
        # # print(imgNB[1001][1510])
        # # print(imgNB[1001][1511])
        # # print(imgNB[1001][1512])
        # # print(imgNB[1001][1513])
        # # print(imgNB[1001][1514])
        # plt.figure()
        # plt.imshow(imgNB,cmap="gray")
        # plt.show()
        #95 et minRAdius 30
        # 40 et minRadius 20
        circles = cv2.HoughCircles(imgNB, cv2.HOUGH_GRADIENT, 2.8, 300,minRadius=60,maxRadius=90)
        print(circles)

        # circles = cv2.HoughCircles(imgNB, cv2.HOUGH_GRADIENT, 2.8, 300,minRadius=60,maxRadius=90)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
        listPotentiels = [x[0] for x in circles]
        # # print(circles)
        i,dist = Fonctions.Externes.findNearestValueFromArray(listPotentiels,pupille[0])
        print("titi")
        # # print(i)
        # print(circles[i][0])
        # points 3 et 19
        # cv2.line(out,(circles[0][0],circles[0][1]),(circles[0][0]+circles[0][2],circles[0][1]),(255, 0, 0), 1)
        # cv2.line(out,(circles[0][0],circles[0][1]),(circles[0][0]-circles[0][2],circles[0][1]),(255, 0, 0), 1)
        # plt.imshow(out)
        # plt.show()
        if(dist>100):
            pt3 = (int(pupille[0]-120),int(pupille[1]))
            pt19 = (int(pupille[0]+120),int(pupille[1]))

        else:
            pt3 = (circles[i][0]-circles[i][2],circles[i][1])
            pt19 = (circles[i][0]+circles[i][2],circles[i][1])
        # # print(pt3)
        # # print(pt19)
        return [pt3,pt19]
        # return circles

    def point9(c,pt19):
        """!
        Routine pour détecter le point 9 (menton)
        @param contours (type numpy.array), pt19 (tuple of float)
        @return pt9
        """
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

    def points15_13(img,pt19,left,right):
        """!
        Routine pour détecter les points 15 et 13 (ouverture bronchiale)
        @param img (type numpy.array)
        @return pt15,pt13 (type tuple of tuple)
        """
        imgcopy = img.copy()
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        img[:,:int(pt19[0])]=255
        tiers = [(left[0]+right[0])/2.8,(left[1]+right[1])/2.8]
        # tiers = [(left[0]+right[0])/2.7,(left[1]+right[1])/2.7]
        img[:,int(tiers[0]):int(right[0])]=255
        # plt.imshow(img)
        # plt.show()
        img = cv2.GaussianBlur(img,(7,7),0)
        img = cv2.addWeighted(img, 2, img, 0, -2)
        img = cv2.threshold(img,40,255,cv2.THRESH_TOZERO)[1]

        #valeurs du filtre canny : 30,40   10,30  120,130
        edges = cv2.Canny(img,120,130)
        edges = cv2.blur(edges,(1,1))
        distances = []
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        pixelValue = np.array([], dtype=np.int64).reshape(0,2)

        for indx,x in enumerate(contours):
            longueur = cv2.arcLength(x,True)>100 and cv2.arcLength(x,True)<500
            pente = abs(Fonctions.Externes.isContoursLineLike(x)[0])>5
            top = tuple(x[x[:, :, 1].argmin()][0])
            bottom = tuple(x[x[:, :, 1].argmax()][0])
            distance = Fonctions.Externes.euclideDist(top,bottom)>80
            if(longueur and pente and distance):
                pixelValue = np.vstack([pixelValue,np.array([[Fonctions.Externes.averagePixelValue(img,x,5),int(indx)]])])

        for x in pixelValue.T[1]:
            if(len(pixelValue)==1):
                distances.append([Fonctions.Externes.isContoursLineLike(contours[int(x)])[0],Fonctions.Externes.isContoursLineLike(contours[int(x)])[1],x])
            if(len(pixelValue)>1):
                if(Fonctions.Externes.averagePixelValue(img,contours[int(x)],5)<np.percentile(pixelValue,40)):
                    distances.append([Fonctions.Externes.isContoursLineLike(contours[int(x)])[0],Fonctions.Externes.isContoursLineLike(contours[int(x)])[1],x])


        distances.sort(key=lambda x:x[1])

        try:
            contoursValide = contours[int(distances[0][2])]
            top = tuple(contoursValide[contoursValide[:, :, 1].argmin()][0])
            bottom = tuple(contoursValide[contoursValide[:, :, 1].argmax()][0])
            pt15 = top
            pt13 = bottom
        except:
            pt15=(0,0)
            pt13=(0,0)

        print(pt15)
        print(pt13)
        return pt15,pt13


    def points5_7(img,pt9,left):
        """!
        Routine pour détecter les points 5 et 7 (lèvres)
        @param img,pt9,left
        @return pt5,pt7 (type tuple of tuple)
        """
        from scipy.signal import find_peaks
        import statistics

        ''' contours du corps '''
        _,c = Points.contoursCorps(img,'head')
        cX = c.T[0][0]
        cY = c.T[1][0]
        cList = [[cX[i],cY[i]] for i in range(len(cX))]

        ''' contours de la bouche '''
        approxBouche = cv2.approxPolyDP(c,1e-16,closed=False)
        approxBouche2 = []
        for x in approxBouche:
            if (x[0][0]<pt9[0] and x[0][1]<left[1]):
                approxBouche2.append(x)
        approxBouche2 = np.asarray(approxBouche2)
        approxBouche2 = approxBouche2[:,0,:]
        approxBouche2 = np.array([list(approxBouche2[::2][i]) for i in range(len(approxBouche2)//2)])
        abscisses = approxBouche2.T[0]
        ordonnees = approxBouche2.T[1]

        ''' distance to line'''

        pente,intercept = Fonctions.Externes.penteIntercept(left,approxBouche2[0])
        xx = np.linspace(max(approxBouche2[0][0],left[0]),min(approxBouche2[0][0],left[0]),len(abscisses))
        yy = np.round(pente*xx+intercept)

        ''' calcul du projete '''
        projete = [np.round(Fonctions.Externes.projeteOrtho(pente,intercept,xx[i],ordonnees[i])) for i in range(len(xx))]
        projete = [x.flatten().tolist() for x in projete]
        xxx=np.array(projete).T[0]
        yyy = np.array(projete).T[1]

        ''' affichage controle '''
        # # plt.figure()
        # # plt.plot(-ordonnees,-1*abscisses,'r',label='Contour bouche')
        # # plt.figure()
        # # plt.imshow(img)
        # # # plt.plot(xx,yy,'r')
        # # plt.plot(abscisses,ordonnees,'b')
        # # plt.plot(xxx,yyy,'g')

        ''' calcul de la distance '''
        erreur3 = [Fonctions.Externes.euclideDist([xx[i],yy[i]],[xxx[i],yyy[i]]) for i in range(len(yyy))]
        erreur3 = [erreur3[i]-statistics.mean(erreur3) for i in range(len(erreur3))]
        peaks,_=find_peaks(erreur3,height=(0, None),distance=5,prominence=1)

        ''' affichage distance '''
        # plt.figure()
        # plt.plot(xx,erreur3)

        ''' choix du pic le plus proche de la lèvre inférieure '''
        if(len(peaks)>1):
            pointsPotentiels = [[xx[peaks[i]],ordonnees[peaks[i]]] for i in range(len(peaks))]
            indxx,_,_ = Fonctions.Externes.findNearestPointFromListOfPoints(left,pointsPotentiels)
            indxx = peaks[indxx]
        else:
            indxx = peaks


        pt5 = (left[0],left[1])
        pt7 = (int(xx[indxx]),int(ordonnees[indxx]))
        _,pointB,_ = Fonctions.Externes.findNearestPointFromListOfPoints(pt7,cList)
        pt7 = (pointB[0],pointB[1])
        print("pt5")
        print(pt5)
        print("pt7")
        print(pt7)

        return pt5,pt7

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


    def contoursCorpsFondBlanc(img):
        """!
        Routine pour détecter les points 5 et 7 (lèvres)
        @param img,pt9,left
        @return pt5,pt7 (type tuple of tuple)
        """
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # img_hsv = cv2.bilateralFilter(img_hsv,15,75,75)

        # plt.figure()
        # plt.imshow(img_hsv)

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
        # plt.figure()
        # plt.imshow(img_out1)
        # plt.figure()
        # plt.imshow(img_out2)
        # plt.figure()
        # plt.imshow(img)
        # plt.figure()
        # plt.imshow(img_hsv)
        # plt.figure()
        # plt.imshow(res)
        # plt.show()



    def points11_17(img,pt13,pt15):
        """!
        Routine pour détecter les points 11 et 17 (ouverture bronchiale)
        @param img (type numpy.array),pt13,pt15
        @return pt11,pt17 (type tuple of tuple)
        """
        _,c = Points.contoursCorps(img,'head')
        approxCorps = cv2.approxPolyDP(c,0.0000001,closed=False)
        if(pt15[0]-pt13[0]!=0):
            slope = (pt15[1]-pt13[1])/(pt15[0]-pt13[0])
        if(pt15[0]-pt13[0]==0):
            slope = (pt15[1]-pt13[1])/0.00001
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



    def ImageCorps(imgPIL):
        from PIL import Image
        PIL_image = imgPIL.resize((1300,975), Image.ANTIALIAS)
        CV2_image = np.array(imgPIL)
        out,c = Points.contoursCorps(CV2_image,'body')
        [left,right,top,bottom] = Points.pointExtremeContours(c)
        imagerot = Points.rotate_image(out,Points.angleRot(left,right)[0],Points.angleRot(left,right)[1])
        _,c = Points.contoursCorps(imagerot,'body')
        [left,right,top,bottom] = Points.pointExtremeContours(c)
        corpsStandard = [[left[0],left[1]],[top[0],top[1]],[right[0],right[1]],[bottom[0],bottom[1]]]
        newPIL_image = Image.fromarray(imagerot)
        return corpsStandard,newPIL_image,left

    def ImageTete(pathok,numImage):
        from PIL import Image
        import cv2
        imgPIL = Image.open(pathok[numImage])
        PIL_image_big = imgPIL.resize((3500,2625), Image.ANTIALIAS)
        PIL_image_big = np.flip(PIL_image_big,axis=2)
        CV2_image_big = cv2.imread(pathok[numImage])
        CV2_image_big = cv2.cvtColor(CV2_image_big,cv2.COLOR_BGR2RGB)
        # CV2_image_big = CV2_image_big[:, :, ::-1].copy()
        out,c = Points.contoursCorps(CV2_image_big,'head')
        [left1,right1,top,bottom] = Points.pointExtremeContours(c)
        CV2_image_big = Points.rotate_image(out,Points.angleRot(left1,right1)[0],Points.angleRot(left1,right1)[1])
        _,c = Points.contoursCorps(CV2_image_big,'head')
        [left1,right1,_,_] = Points.pointExtremeContours(c)
        print("\n### Chargement de l'image de la tête' ###")
        PIL_image_big = Image.fromarray(CV2_image_big)
        return PIL_image_big,CV2_image_big,left1,right1
'''
*
* Main function
*
'''
#
# plt.figure()
# plt.imshow(img)
# plt.show()
# Points.contoursCorpsFondBlanc(img)
# plt.figure()
# plt.imshow(out)
# plt.show()
# # # #
# # # # # # # # # #
# # # # out,c = Points.contoursCorpsBig(img)
# # # # [left,right,top,bottom] = Points.pointExtremeContours(c)
# # # # imagerot = Points.rotate_image(out,Points.angleRot(left,right)[0],Points.angleRot(left,right)[1])
# # # # # #
# # # # _,c = Points.contoursCorpsBig(imagerot)
# # # # [left,right,top,bottom] = Points.pointExtremeContours(c)
# # # # print("left")
# # # # print(left)
# # # # # #
# # # # print("toto")
# # # # print(imagerot.shape)
# # # # [pt3,pt19]=Points.points3_19(imagerot)
# # # # print("pt3")
# # # # print(pt3)
# # # # print("pt19")
# # # # print(pt19)
# # # # # circles = Points.points3_19(imagerot)
# # # # print("pt9")
# # # # pt9 = Points.point9(c,pt19)
# # # # #
# # # # # #ne fonctionne pas pour l'instant
# # # # [pt15,pt13] =Points.points15_13(imagerot,pt19,left,right)
# # # # # pt13 = (1288, 1228)
# # # # # pt15 = (1308, 1098)
# # # # cv2.circle(imagerot, pt15, 8, (255, 255, 0), -1)
# # # # cv2.circle(imagerot, pt13, 8, (255, 255, 0), -1)
# # # # #
# # # # # pt5,pt7 = Points.points5_7(imagerot,pt9)
# # # # pt5,pt7= Points.points5_7(imagerot,pt9,left)
# # # # #
# # # # # pt11,pt17 = Points.points11_17(imagerot,pt13,pt15)
# # # # # pt11 = (pt11[0],pt11[1])
# # # # # pt17 = (pt17[0],pt17[1])
# # # # cv2.circle(imagerot, left, 12, (0, 50, 255), -1)
# # # # cv2.circle(imagerot, right, 12, (0, 255, 255), -1)
# # # # # cv2.circle(imagerot, top, 12, (255, 50, 0), -1)
# # # # # cv2.circle(imagerot, bottom, 12, (255, 255, 0), -1)
# # # # cv2.circle(imagerot, pt3, 4, (255, 0, 0), -1)
# # # # cv2.circle(imagerot, pt19, 4, (255, 0, 0), -1)
# # # # cv2.circle(imagerot, pt9, 8, (255, 0, 0), -1)
# # # # cv2.circle(imagerot, pt5, 8, (0, 255, 0), -1)
# # # # cv2.circle(imagerot, pt7, 8, (0, 255, 0), -1)
# # # # # cv2.circle(imagerot, pt11, 8, (0, 255, 0), -1)
# # # # # cv2.circle(imagerot, pt17, 8, (0, 255, 0), -1)
# # # # plt.figure()
# # # # plt.imshow(imagerot)
# # # # plt.title("Vérification du positionnement des points avant interface")
# # # # plt.grid(True)
# # # # plt.show()

def test(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    out,c = Points.contoursCorps(img,'head')
    [left,right,top,bottom] = Points.pointExtremeContours(c)
    imagerot = Points.rotate_image(out,Points.angleRot(left,right)[0],Points.angleRot(left,right)[1])
    # #
    _,c = Points.contoursCorps(imagerot,'head')
    [left,right,top,bottom] = Points.pointExtremeContours(c)
    print("left")
    print(left)
    # #
    print("toto")
    print(imagerot.shape)
    [pt3,pt19]=Points.points3_19(imagerot)
    Points.points3_19_independant(imagerot)

    print("pt3")
    print(pt3)
    print("pt19")
    print(pt19)
    # circles = Points.points3_19(imagerot)
    print("pt9")
    pt9 = Points.point9(c,pt19)
    #
    # #ne fonctionne pas pour l'instant
    [pt15,pt13] =Points.points15_13(imagerot,pt19,left,right)
    # pt13 = (1288, 1228)
    # pt15 = (1308, 1098)
    cv2.circle(imagerot, pt15, 15, (255, 255, 0), -1)
    cv2.circle(imagerot, pt13, 15, (255, 255, 0), -1)
    #
    # pt5,pt7 = Points.points5_7(imagerot,pt9)
    pt5,pt7= Points.points5_7(imagerot,pt9,left)
    #
    pt11,pt17 = Points.points11_17(imagerot,pt13,pt15)
    pt11 = (pt11[0],pt11[1])
    pt17 = (pt17[0],pt17[1])
    cv2.circle(imagerot, left, 12, (0, 50, 255), -1)
    cv2.circle(imagerot, right, 12, (0, 255, 255), -1)
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
    # plt.imshow(imagerot)
    # plt.title("Vérification du positionnement des points avant interface")
    # plt.grid(True)
    # plt.show()
    return imagerot


test(img_path)

# # #
# # # test_male = [test(path) for path in male_img]
# # #
# # # import numpy as np
# # # import matplotlib.pyplot as plt
# # #
# # # w=10
# # # h=10
# # # fig=plt.figure(figsize=(8, 8))
# # # columns = 4
# # # rows = 3
# # # for i in range(1, columns*rows +1):
# # #     img = test_male[i-1]
# # #     fig.add_subplot(rows, columns, i)
# # #     plt.imshow(img)
# # # plt.show()