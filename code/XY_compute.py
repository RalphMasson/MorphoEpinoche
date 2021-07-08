''' Bibliothèque de fonctions de placement '''

import cv2,math,sys
# # # # # # import matplotlib.pyplot as plt
import numpy as np
import sys,inspect
sys.path.insert(0,'/'.join(inspect.stack()[0][1].split('\\')[:-1]))
import XY_tools
import IA_morph as ML

class PointsML():
    """!

        Classe de placement de points par Machine Learning
        Nécessite d'avoir pointé au préalable les images avec tpsDig et de disposer d'un modèle
        (default : predictor.dat)

        Adapted from :
            Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014
            Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020
            Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020
            Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019
    """

    def __init__(self):
        self.pointsML = [[0,0]]*10

    def getXY(self,path_model,path_image):
        """!
        Récupère les coordonnées par machine learning
        @param path_model dossier où se trouve le modele regression trees
            (default = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\img\\")
        @param path_image dossier où se trouve le dossier de l'image à pointer
            (default = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\img\\test\\")
        The list is expected to be ordered
        """
        print("test")
        path_model = r"C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho/test_pointage_ML/v2/"
        path_image = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\img\\test\\"
        self.pointsML = ML.ML_pointage(os.path.join(sys._MEIPASS, path_model),path_image).listePoints()
        print(self.pointsML)
