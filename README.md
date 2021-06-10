# MorphoEpinoche (ongoing project - ETA : mid-september)

The purpose of this project is to classify the gender of a Three Spined Stickleback based on automatic landmarks detection and maching learning classification

# Landmarks detection #

Specific landmarks are first computed through image processing : body length, body depth, head length, head depth...

<p align="center">
<img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/illustration.jpg" width="200">
</p>

Then, they are detected with regression trees according to [1],[2],[3] :   
  
    
- *Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," doi: 10.1109/CVPR.2014.241.       2014*  
- *Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" doi: 10.1016/j.imavis.2020.103976   2020*  
- *Porto, Voje "ML-morph: [...] automated [...] landmarking of biological structures in images" 10.1111/2041-210X.13373      2020*  
- *Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application"  2019*  


<p align="center">
<img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/test.jpg" width="200">
</p>


# Distances calculation #

Once points are detected, all combinations of distances and angles are calculated : 

<p align="center">
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/illustration2.jpg" width="200" />
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/illustration3.jpg" width="400" /> 
</p>

# Sex prediction #

Finally, a machine learning model predicts the gender of the Three Spined Stickleback :  
<p align="center">
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/gui.png" width="600" />
</p>

