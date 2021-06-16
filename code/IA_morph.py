import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

import IA_tools as utils
import dlib

"""!
    Classe de placement de points par Machine Learning
    Nécessite d'avoir pointé au préalable les images avec tpsDig

    Adapted from :
        Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014
        Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020
        Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020
        Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019
"""

# à incorporer à l'interface
# et aux dossiers utilisateurs

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

        return "Training error (average pixel deviation): {}".format(dlib.test_shape_predictor(trainfolder_path, "predictor.dat"))

    def test_model(self,testfolder_path):
        """!
        Teste le modèle obtenu
        @param testfolder_path path+"test.xml"
        """
        print("Testing error (average pixel deviation): {}".format(dlib.test_shape_predictor(testfolder_path,self.path_create_model+"predictor.dat")))

    def predict(self,foldernewimage,predictor_path):
        """!
        Prédit les points d'une image
        @param foldernewimage : dossier avec l'image à prédire
        @param predictor_path : "C:\\.....\\predictor.dat"
        """
        utils.utils.predictions_to_xml(self.path_create_model+"predictor.dat", dir=foldernewimage,ignore=None,out_file=self.path_create_model+"test\\output.xml")
        self.base_points = utils.utils.dlib_xml_to_pandas(self.path_create_model + "test\\output.xml")

        return self.base_points

    def listePoints(self):
        """!
        Affiche les coordonnées des points prédits
        """
        try:
            self.predict(self.path_predict_image,self.path_create_model+"predictor.dat")
            df = self.base_points
            col = list(df.columns)

            return [[df[col[i+4]][0],df[col[i+5]][0]] for i in range(0,df.shape[1]-4,2)]
        except (AttributeError,RuntimeError):
            print("Fichier predictor.dat introuvable - Entrainez le modèle ou vérifier le chemin du modèle")
        except KeyError:
            print("Image à prédire introuvable - Selectionner une image ou vérifier le chemin de l'image'")


