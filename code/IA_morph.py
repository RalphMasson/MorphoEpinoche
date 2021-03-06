import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

import IA_tools as utils
import XY_tools
import dlib
import numpy as np

"""!
    Classe de placement de points par Machine Learning
    Nécessite d'avoir pointé au préalable les images avec tpsDig

    Adapted from :
        Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014
        Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020
        Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020
        Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019
"""

class ML_pointage():

    def __init__(self,dossier_modele,fichier_image):
        """!
        Instanciation du modèle de detection des points
        @param dossier_modele:str chemin menant au fichier predictor.dat s'il existe
        @param fichier_image:str chemin menant à l'image à pointer
        """
        self.path_create_model = dossier_modele
        self.path_predict_image = fichier_image
        self.options = None
        self.base_points = None

    def preprocess_folder(self,imagefolder_path,tpsfile_path):
        """!
        Séparation des images en image de train et de test (80% 20%)
        @param imagefolder_path : dossier où se trouvent toutes les images pointées
        @param tpsfile_path : fichier tps avec les coordonnées des points
        @return None deux fichiers xml Train et Test
        """
        file_sizes=utils.utils.split_train_test(imagefolder_path)


        dict_tps=utils.utils.read_tps(tpsfile_path)


        utils.utils.generate_dlib_xml(dict_tps,file_sizes['train'],folder=self.path_create_model+"train",out_file=self.path_create_model +"train.xml")
        utils.utils.generate_dlib_xml(dict_tps,file_sizes['test'],folder=self.path_create_model+"test",out_file=self.path_create_model+"test.xml")
        utils.utils.dlib_xml_to_tps(self.path_create_model+"train.xml")
        utils.utils.dlib_xml_to_tps(self.path_create_model+"test.xml")

    def parameter_model(self,tree,nu,threads,cascade_depth,feature_pool_size,test_splits,os):
        """!
        Réglage du modèle
        @param tree = [num_trees,tree_depth]
            @param --num-trees      number of regression trees (default = 500)
            @param --tree-depth    choice of tree depth (default = 4)
                # define the depth of each regression tree -- there will be a total
                # of 2^tree_depth leaves in each tree; small values of tree_depth
                # will be *faster* but *less accurate* while larger values will
                # generate trees that are *deeper*, *more accurate*, but will run
                # *far slower* when making predictions
                # Typical values for tree_depth are in the range [2, 8].



        @param --nu            regularization parameter (default = 0.1)
            Values closer to 1 will make our model fit the training data closer,
            but could potentially lead to overfitting.
            Values closer to  0 will help our model generalize;
            however, there is a caveat to the generalization power
            — the closer nu is to  0, the more training data you’ll need.
            Typically, for small values of nu you’ll need 1000s of training examples.

        @param --threads       number of threads to be used (default = 1)



        @param --cascade-depth  choice of cascade depth (default = 15)
            # the cascade_depth will have a dramatic impact on both the accuracy and the output file size of your model.
            # in the range [6, 18],

        @param --feature-pool-size choice of feature pool size (default = 500) (could be 400)
            # The feature_pool_size controls the number of pixels used
            # to generate features for the random trees in each cascade.
            # My recommendation here is that you should use large values for feature_pools_size
            # if inference speed is not a concern. Otherwise, you should use smaller values for faster prediction speed



        @param --test-splits    number of test splits (default = 20)
            # selects best features at each cascade when training -- the larger
            # this value is, the *longer* it will take to train but (potentially)
            # the more *accurate* your model will be

        @param --oversampling oversampling amount (default = 10) (could be 5)
            # controls amount of "jitter" (i.e., data augmentation) when training
            # the shape predictor -- applies the supplied number of random
            # deformations, thereby performing regularization and increasing the
            # ability of our model to generalize
            # in range (0,50) : 50 means nb_image * 50
            # !!!! can increase a lot training time !!!!
        """
        num_trees,tree_depth = tree[0],tree[1]
        options = dlib.shape_predictor_training_options()
        options.num_trees_per_cascade_level=num_trees
        options.nu = nu
        options.num_threads = threads
        options.tree_depth = tree_depth
        options.cascade_depth = cascade_depth
        options.feature_pool_size = feature_pool_size
        options.num_test_splits = test_splits
        options.oversampling_amount = os
        options.be_verbose = True
        self.options = options
        return self.options

    def train_model(self,trainfolder_path):
        """!
        Lance l'apprentissage du modèle avec les valeurs par défaut
        @param trainfolder : path+"train.xml"
        """
        # self.parameter_model([500,6],0.6,1,18,700,40,500)

        dlib.train_shape_predictor(trainfolder_path,self.path_create_model+"predictor.dat",self.options)

        return "Training error (average pixel deviation): {}".format(dlib.test_shape_predictor(trainfolder_path, self.path_create_model+"predictor.dat"))

    def partial_train(self,imagefolder_path,tpsfile_path,trainfolder_path,n_max):
        """!
        Lance l'apprentissage du modèle avec les valeurs par défaut
        @param trainfolder : path+"train.xml"
        @param n_max : nombre max d'images à prendre pour l'apprentissage (0-1)
        """
        print("split")
        file_sizes=utils.utils.split_train_test(imagefolder_path,n_max)
        print("read_tps")
        dict_tps=utils.utils.read_tps(tpsfile_path)
        print("generate xml")
        utils.utils.generate_dlib_xml(dict_tps,file_sizes['train'],folder=self.path_create_model+"train",out_file=self.path_create_model +"train.xml")
        utils.utils.generate_dlib_xml(dict_tps,file_sizes['test'],folder=self.path_create_model+"test",out_file=self.path_create_model+"test.xml")
        utils.utils.dlib_xml_to_tps(self.path_create_model+"train.xml")
        utils.utils.dlib_xml_to_tps(self.path_create_model+"test.xml")
        print("options")
        self.parameter_model([500,3],0.08,1,20,700,20,200)
        print("train")
        dlib.train_shape_predictor(trainfolder_path,self.path_create_model+"predictor.dat",self.options)

    def test_model(self,testfolder_path):
        """!
        Teste le modèle obtenu
        @param testfolder_path path+"test.xml"
        """
        print("Testing error (average pixel deviation): {}".format(dlib.test_shape_predictor(testfolder_path,self.path_create_model+"predictor.dat")))

    def predict(self,path_newimage,predictor_path,predictor_name):
        """!
        Prédit les points d'une image
        @param foldernewimage : dossier avec l'image à prédire
        @param predictor_path : "C:\\.....\\predictor.dat"
        @param predictor_name : default predictor.dat
        """
        print(self.path_create_model+"output.xml")
        print(self.path_create_model+predictor_name)
        print(path_newimage)

        # utils.utils.predictions_to_xml2(self.path_create_model+predictor_name, dir=path_newimage,ignore=None,out_file=self.path_create_model+"output.xml")
        utils.utils.predictions_to_xml(self.path_create_model+predictor_name, img_path=path_newimage,ignore=None,out_file=self.path_create_model+"output.xml")

        self.base_points = utils.utils.dlib_xml_to_pandas(self.path_create_model + "output.xml")

        return self.base_points

    def xmltolist(xmlfile,num_image_max):
        """!
            Affiche les coordonnées des points prédits (de la première image)
        """
        df = utils.utils.dlib_xml_to_pandas(xmlfile)
        col = list(df.columns)
        liste_coord = []
        for k in range(num_image_max):
            liste_coord.append([[df[col[i+4]][k],1440-df[col[i+5]][k]] for i in range(0,df.shape[1]-4,2)])
        return liste_coord


    def xmltolistY(xmlfile,num_image_max):
        """!
            Affiche les coordonnées des points prédits (de la première image)
        """
        df = utils.utils.dlib_xml_to_pandas(xmlfile)
        col = list(df.columns)
        liste_coord = []
        liste_coord.append([[df[col[i+4]][num_image_max],df[col[i+5]][num_image_max]] for i in range(0,df.shape[1]-4,2)])
        return liste_coord


    def listePoints(self,num_image_max):
        """!
        Affiche les coordonnées des points prédits du fichier output
        """
        print(self.path_predict_image,self.path_create_model+"/predictor.dat")
        print(num_image_max)
        self.predict(self.path_predict_image,self.path_create_model+"/predictor.dat","predictor.dat")
        return ML_pointage.xmltolist(self.path_create_model + "/output.xml",num_image_max)

        # try:
        #     self.predict(self.path_predict_image,self.path_create_model+"\\predictor.dat")
        #     return ML_pointage.xmltolist(self.path_create_model + "\\output.xml")
        # except (AttributeError,RuntimeError):
        #     print("Fichier predictor.dat introuvable - Entrainez le modèle ou vérifier le chemin du modèle")
        # except KeyError:
        #     print("Image à prédire introuvable - Selectionner une image ou vérifier le chemin de l'image'")

    def vecteurDetail(vecteur1):
        import math
        return math.atan2(vecteur1[1],vecteur1[0])*180/math.pi,np.sqrt(vecteur1[0]**2+vecteur1[1]**2)

    def getErrorPerLandmark(self,XY_predict,XY_truth):
        """!
        Donne l'erreur pour chaque points dans le but de conserver les points les mieux détectés
        @param XY_predict points trouvés par le modèle (liste [[x1,y1],[x2,y2]...]
        @param XY_truth points trouvé par l'expérimentateur (liste [[x1,y1],[x2,y2]...]
        @return listErrorPerLandmark
        """
        listErrorPerLandmark = [dict.fromkeys(['id_point','error']) for _ in range(len(XY_predict))]
        for indx,(measured,real) in enumerate(zip(XY_predict,XY_truth)):

            # statsMeasured = ML_pointage.vecteurDetail(measured)
            # statsReal = ML_pointage.vecteurDetail(real)
            # dTheta = round(abs(statsMeasured[0]-statsReal[0]),6)
            # dNorm = round(abs(statsMeasured[1]-statsReal[1]),6)
            # error = round(16*dTheta+0.5*dNorm,6)
            error = round(XY_tools.Externes.euclide(measured,real))
            answer = "{mispositioning of point n°"+str(indx)+"} : "+str(error)+" pixels\n"
            print(answer)
            listErrorPerLandmark[indx]['id_point']=indx
            listErrorPerLandmark[indx]['error']=error

        return listErrorPerLandmark




## Evaluation perf modèle pointage pour apprentissage


def subliste(l1,l2):
    return XY_tools.Externes.euclide(l1,l2)

def evaluateTrain():

    a = ML_pointage(r"C://Users//MASSON//Desktop//POINTAGe//v3/",r"C:\Users\MASSON\Desktop\POINTAGe\v3\train\\")
    predictTrain = a.listePoints(309)
    truthTrain = ML_pointage.xmltolist(r'C:\Users\MASSON\Desktop\POINTAGe\v3\train.xml',309)
    pt0 = []
    pt1 = []
    pt2 = []
    pt3 = []
    pt4 = []
    pt5 = []
    pt6 = []
    pt7 = []
    pt8 = []
    pt9 = []

    for x in truthTrain:
        pt0.append(x[0])
        pt1.append(x[1])
        pt2.append(x[2])
        pt3.append(x[3])
        pt4.append(x[4])
        pt5.append(x[5])
        pt6.append(x[6])
        pt7.append(x[7])
        pt8.append(x[8])
        pt9.append(x[9])

    pt0_pred = []
    pt1_pred = []
    pt2_pred = []
    pt3_pred = []
    pt4_pred = []
    pt5_pred = []
    pt6_pred = []
    pt7_pred = []
    pt8_pred = []
    pt9_pred = []

    for x in predictTrain:
        pt0_pred.append(x[0])
        pt1_pred.append(x[1])
        pt2_pred.append(x[2])
        pt3_pred.append(x[3])
        pt4_pred.append(x[4])
        pt5_pred.append(x[5])
        pt6_pred.append(x[6])
        pt7_pred.append(x[7])
        pt8_pred.append(x[8])
        pt9_pred.append(x[9])

    ecart_truth_pred0=[]
    ecart_truth_pred1=[]
    ecart_truth_pred2=[]
    ecart_truth_pred3=[]
    ecart_truth_pred4=[]
    ecart_truth_pred5=[]
    ecart_truth_pred6=[]
    ecart_truth_pred7=[]
    ecart_truth_pred8=[]
    ecart_truth_pred9=[]

    for i in range(len(pt0)):
        ecart0 = subliste(pt0[i],pt0_pred[i])
        print(ecart0)

        ecart1 = subliste(pt1[i],pt1_pred[i])
        ecart2 = subliste(pt2[i],pt2_pred[i])
        ecart3 = subliste(pt3[i],pt3_pred[i])
        ecart4 = subliste(pt4[i],pt4_pred[i])
        ecart5 = subliste(pt5[i],pt5_pred[i])
        ecart6 = subliste(pt6[i],pt6_pred[i])
        ecart7 = subliste(pt7[i],pt7_pred[i])
        ecart8 = subliste(pt8[i],pt8_pred[i])
        ecart9 = subliste(pt9[i],pt9_pred[i])
        ecart_truth_pred0.append(ecart0)
        ecart_truth_pred1.append(ecart1)
        ecart_truth_pred2.append(ecart2)
        ecart_truth_pred3.append(ecart3)
        ecart_truth_pred4.append(ecart4)
        ecart_truth_pred5.append(ecart5)
        ecart_truth_pred6.append(ecart6)
        ecart_truth_pred7.append(ecart7)
        ecart_truth_pred8.append(ecart8)
        ecart_truth_pred9.append(ecart9)

        import seaborn as sns
        import pandas as pd
        import matplotlib.pyplot as plt
        tests = [ecart_truth_pred0,ecart_truth_pred1,ecart_truth_pred2,ecart_truth_pred3,ecart_truth_pred4,ecart_truth_pred5,ecart_truth_pred6,ecart_truth_pred7,ecart_truth_pred8,ecart_truth_pred9]
        df = pd.DataFrame(tests, index=['pt1','pt2','pt3','pt4','pt5','pt6','pt7','pt8','pt9','pt10'])
        plt.figure()
        df.T.boxplot(vert=True,showbox=True,showmeans=True,showfliers=False,sym='',whis=50)
        plt.title("Error (euclidean distance in pixels) per landmark : Training dataset")
        plt.subplots_adjust(left=0.25)
        plt.ylim([-0.5,5])
        plt.show()
        import matplotlib.lines as mlines
        plt.figure()
        triangle = mlines.Line2D([], [], color='green', marker='^', linestyle='None', markersize=5, label='Mean')
        ax = sns.boxplot(data=df.T,orient="h",showmeans=True,showfliers=False,palette="Blues")
        plt.plot([], [], '-', linewidth=1, color='Crimson', label='mean')
        plt.legend(handles=[triangle])
        plt.xlim([-0.5,3])
        plt.title("Error (euclidean distance in pixels) per landmark : Training dataset")
        plt.grid(True)
        plt.show()


def evaluateTest():
    a = ML_pointage(r"C://Users//MASSON//Desktop//POINTAGe//v3//",r"C:\Users\MASSON\Desktop\POINTAGe\v3\test\\")
    predictTest = a.listePoints(78)
    truthTest = ML_pointage.xmltolist(r'C:\Users\MASSON\Desktop\POINTAGe\v3\test.xml',78)

    pt0 = []
    pt1 = []
    pt2 = []
    pt3 = []
    pt4 = []
    pt5 = []
    pt6 = []
    pt7 = []
    pt8 = []
    pt9 = []

    for x in truthTest:
        pt0.append(x[0])
        pt1.append(x[1])
        pt2.append(x[2])
        pt3.append(x[3])
        pt4.append(x[4])
        pt5.append(x[5])
        pt6.append(x[6])
        pt7.append(x[7])
        pt8.append(x[8])
        pt9.append(x[9])

    pt0_pred = []
    pt1_pred = []
    pt2_pred = []
    pt3_pred = []
    pt4_pred = []
    pt5_pred = []
    pt6_pred = []
    pt7_pred = []
    pt8_pred = []
    pt9_pred = []
    for x in predictTest:
        pt0_pred.append(x[0])
        pt1_pred.append(x[1])
        pt2_pred.append(x[2])
        pt3_pred.append(x[3])
        pt4_pred.append(x[4])
        pt5_pred.append(x[5])
        pt6_pred.append(x[6])
        pt7_pred.append(x[7])
        pt8_pred.append(x[8])
        pt9_pred.append(x[9])

    ecart_truth_pred0=[]
    ecart_truth_pred1=[]
    ecart_truth_pred2=[]
    ecart_truth_pred3=[]
    ecart_truth_pred4=[]
    ecart_truth_pred5=[]
    ecart_truth_pred6=[]
    ecart_truth_pred7=[]
    ecart_truth_pred8=[]
    ecart_truth_pred9=[]

    for i in range(len(pt0)):
        ecart0 = subliste(pt0[i],pt0_pred[i])
        print(ecart0)

        ecart1 = subliste(pt1[i],pt1_pred[i])
        ecart2 = subliste(pt2[i],pt2_pred[i])
        ecart3 = subliste(pt3[i],pt3_pred[i])
        ecart4 = subliste(pt4[i],pt4_pred[i])
        ecart5 = subliste(pt5[i],pt5_pred[i])
        ecart6 = subliste(pt6[i],pt6_pred[i])
        ecart7 = subliste(pt7[i],pt7_pred[i])
        ecart8 = subliste(pt8[i],pt8_pred[i])
        ecart9 = subliste(pt9[i],pt9_pred[i])
        ecart_truth_pred0.append(ecart0)
        ecart_truth_pred1.append(ecart1)
        ecart_truth_pred2.append(ecart2)
        ecart_truth_pred3.append(ecart3)
        ecart_truth_pred4.append(ecart4)
        ecart_truth_pred5.append(ecart5)
        ecart_truth_pred6.append(ecart6)
        ecart_truth_pred7.append(ecart7)
        ecart_truth_pred8.append(ecart8)
        ecart_truth_pred9.append(ecart9)

    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    tests = [ecart_truth_pred0,ecart_truth_pred1,ecart_truth_pred2,ecart_truth_pred3,ecart_truth_pred4,ecart_truth_pred5,ecart_truth_pred6,ecart_truth_pred7,ecart_truth_pred8,ecart_truth_pred9]
    df = pd.DataFrame(tests, index=['pt1','pt2','pt3','pt4','pt5','pt6','pt7','pt8','pt9','pt10'])
    plt.figure()
    df.T.boxplot(vert=False,showmeans=True)
    plt.title("Error Testing per landmark")
    plt.subplots_adjust(left=0.25)
    plt.xlim([0,20])
    plt.show()
    plt.figure()
    ax = sns.boxplot(data=df.T,orient="h",showmeans=True)
    plt.xlim([0,20])
    plt.title("Error Testing per landmark")
    plt.grid(True)
    plt.show()


    import matplotlib.lines as mlines
    plt.figure()
    triangle = mlines.Line2D([], [], color='green', marker='^', linestyle='None', markersize=5, label='Mean')
    ax = sns.boxplot(data=df.T,orient="h",showmeans=True,showfliers=True,palette="pastel")
    plt.plot([], [], '-', linewidth=1, color='Crimson', label='mean')
    plt.legend(handles=[triangle])
    plt.xlim([-0.5,17])
    plt.title("Error (euclidean distance in pixels) per landmark : Testing dataset")
    plt.grid(True)
    plt.show()


def tableLecture():
    import pandas as pd
    df0 = pd.DataFrame(tests[0]).describe()
    df1 = pd.DataFrame(tests[1]).describe()
    df2 = pd.DataFrame(tests[2]).describe()
    df3 = pd.DataFrame(tests[3]).describe()
    df4 = pd.DataFrame(tests[4]).describe()
    df5 = pd.DataFrame(tests[5]).describe()
    df6 = pd.DataFrame(tests[6]).describe()
    df7 = pd.DataFrame(tests[7]).describe()
    df8 = pd.DataFrame(tests[8]).describe()
    df9 = pd.DataFrame(tests[9]).describe()
    df0['1'] = df1
    df0['2'] = df2
    df0['3'] = df3
    df0['4'] = df4
    df0['5'] = df5
    df0['6'] = df6
    df0['7'] = df7
    df0['8'] = df8
    df0['9'] = df9
    df0.to_csv(r"C://Users//MASSON//Desktop//POINTAGe//resultatsTrainV1.csv",sep=";")
