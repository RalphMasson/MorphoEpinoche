import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)

import utilsML as utils
import dlib

# à incorporer à l'interface
# et aux dossiers utilisateurs

class ML_pointage():

    path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\test_pointage_ML\\img\\"

    """!

        Classe de placement de points par Machine Learning
        Nécessite d'avoir pointé au préalable les images avec tpsDig

        Adapted from :
            Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.
            Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976
            Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373



    """

    def preprocess_folder(imagefolder_path,tpsfile_path):
        """!
        Séparation des images en image de train et de test (80% 20%)
        @param imagefolder_path : dossier où se trouvent toutes les images pointées
        @param tpsfile_path : fichier tps avec les coordonnées des points
        @return None deux fichiers xml Train et Test
        """
        file_sizes=utils.split_train_test(imagefolder_path)
        print(file_sizes)
        dict_tps=utils.read_tps(tpsfile_path)

        utils.generate_dlib_xml(dict_tps,file_sizes['train'],folder=ML_pointage.path+"train",out_file=ML_pointage.path +"train.xml")
        utils.generate_dlib_xml(dict_tps,file_sizes['test'],folder=ML_pointage.path+"test",out_file=ML_pointage.path+"test.xml")
        utils.dlib_xml_to_tps(ML_pointage.path+"train.xml")
        utils.dlib_xml_to_tps(ML_pointage.path+"test.xml")

    def parameter_model(num_trees,nu,threads,tree_depth,cascade_depth,feature_pool_size,test_splits,oversampling):
        """!
        Réglage du modèle
        --num-trees      number of regression trees (default = 500)
        --nu            regularization parameter (default = 0.1)
        --threads       number of threads to be used (default = 1)
        --tree-depth    choice of tree depth (default = 4)
        --cascade-depth  choice of cascade depth (default = 15)
        --feature-pool-size choice of feature pool size (default = 500)
        --test-splits    number of test splits (default = 20)
        --oversampling oversampling amount (default = 10)
        """
        options = dlib.shape_predictor_training_options()
        options.num_trees_per_cascade_level=num_trees
        options.nu = nu
        options.num_threads = threads
        options.tree_depth = tree_depth
        options.cascade_depth = cascade_depth
        options.feature_pool_size = feature_pool_size
        options.num_test_splits = test_splits
        options.oversampling_amount = oversampling
        options.be_verbose = True
        ML_pointage.options = options

    def train_model(trainfolder_path):
        """!
        Lance l'apprentissage du modèle
        trainfolder : path+"train.xml"
        """
        ML_pointage.parameter_model(500,0.1,1,4,15,500,20,10)
        dlib.train_shape_predictor(trainfolder_path,ML_pointage.path+"predictor.dat",ML_pointage.options)
        print("Training error (average pixel deviation): {}".format(dlib.test_shape_predictor(trainfolder_path, "predictor.dat")))

    def test_model(testfolder_path):
        """!
        Teste le modèle obtenu
        """
        print("Testing error (average pixel deviation): {}".format(dlib.test_shape_predictor(testfolder_path,ML_pointage.path+"predictor.dat")))

    def predict(foldernewimage):
        """!
        Prédit les points d'une image
        """
        utils.predictions_to_xml(ML_pointage.path+"predictor.dat", dir=foldernewimage,ignore=None,out_file="output.xml")
        utils.dlib_xml_to_tps("output.xml")

