class Prediction():
    """!
        Classe de prediction du sexe du poisson par Machine Learning
        Nécessite d'avoir un modèle de prédiction des points et du sexe avec un image

        Adapted from :
            Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014
            Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020
            Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020
            Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019
    """
    def preprocess():
        return 0

    def train():
        return 0

    def test():
        return 0

    def predict():
        from random import randrange,uniform
        labels = ('Male','Female')
        # choice = randrange(2)
        p = uniform(0,1)
        if(p>0.5):
            fg='blue'
            choice = 0
            p = p
        if(p<0.5):
            fg='red'
            choice = 1
            p = 1 - p
        return labels[choice],fg,p