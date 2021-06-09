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
            Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014
            Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020
            Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020
            Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019



    """

    def preprocess_folder(imagefolder_path,tpsfile_path):
        """!
        Séparation des images en image de train et de test (80% 20%)
        @param imagefolder_path : dossier où se trouvent toutes les images pointées
        @param tpsfile_path : fichier tps avec les coordonnées des points
        @return None deux fichiers xml Train et Test
        """
        file_sizes=utils.split_train_test(imagefolder_path)
        dict_tps=utils.read_tps(tpsfile_path)

        utils.generate_dlib_xml(dict_tps,file_sizes['train'],folder=ML_pointage.path+"train",out_file=ML_pointage.path +"train.xml")
        utils.generate_dlib_xml(dict_tps,file_sizes['test'],folder=ML_pointage.path+"test",out_file=ML_pointage.path+"test.xml")
        utils.dlib_xml_to_tps(ML_pointage.path+"train.xml")
        utils.dlib_xml_to_tps(ML_pointage.path+"test.xml")

    def parameter_model(num_trees,nu,threads,tree_depth,cascade_depth,feature_pool_size,test_splits,oversampling):
        """!
        Réglage du modèle
        @param --num-trees      number of regression trees (default = 500)

        @param --nu            regularization parameter (default = 0.1)
            Values closer to 1 will make our model fit the training data closer,
            but could potentially lead to overfitting.
            Values closer to  0 will help our model generalize;
            however, there is a caveat to the generalization power
            — the closer nu is to  0, the more training data you’ll need.
            Typically, for small values of nu you’ll need 1000s of training examples.

        @param --threads       number of threads to be used (default = 1)

        @param --tree-depth    choice of tree depth (default = 4)
            # define the depth of each regression tree -- there will be a total
            # of 2^tree_depth leaves in each tree; small values of tree_depth
            # will be *faster* but *less accurate* while larger values will
            # generate trees that are *deeper*, *more accurate*, but will run
            # *far slower* when making predictions
            # Typical values for tree_depth are in the range [2, 8].


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
        Lance l'apprentissage du modèle avec les valeurs par défaut
        @param trainfolder : path+"train.xml"
        """
        ML_pointage.parameter_model(500,0.6,1,6,18,700,40,500)
        dlib.train_shape_predictor(trainfolder_path,ML_pointage.path+"predictor.dat",ML_pointage.options)
        print("Training error (average pixel deviation): {}".format(dlib.test_shape_predictor(trainfolder_path, "predictor.dat")))

    def test_model(testfolder_path):
        """!
        Teste le modèle obtenu
        @param testfolder_path path+"test.xml"
        """
        print("Testing error (average pixel deviation): {}".format(dlib.test_shape_predictor(testfolder_path,ML_pointage.path+"predictor.dat")))

    def predict(foldernewimage,predictor_path):
        """!
        Prédit les points d'une image
        @param foldernewimage : dossier avec l'image à prédire
        @param predictor_path : "C:\\.....\\predictor.dat"
        """
        utils.predictions_to_xml(ML_pointage.path+"predictor.dat", dir=foldernewimage,ignore=None,out_file=ML_pointage.path+"test\\output.xml")
        ML_pointage.base_points = utils.dlib_xml_to_pandas(ML_pointage.path + "test\\output.xml")

        return ML_pointage.base_points

    def listePoints(n):
        """!
        @param n nombre de points sur l'image attendus
        """
        df = ML_pointage.base_points
        for i in range(n):
            print(df['X'+str(i)][0],' ',df['Y'+str(i)][0])



