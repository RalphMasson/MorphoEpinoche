# MorphoEpinoche (ongoing project - ETA : mid-september)

The purpose of this project is to classify the gender of a Three Spined Stickleback based on automatic landmarks detection and maching learning classification

# Landmarks detection #

10 Specific landmarks are computed through Machine Learning (regression trees) according to Kazemi method adapted to biological research [1,2,3,4] :
 
[1] *Kazemi,Sullivan, "One millisecond face alignment with an ensemble of regression trees," 2014*  

[2] *Perrot,Bourdon,Helbert "Implementing cascaded regression tree-based face landmarking" 2020*  

[3] *Porto, Voje "ML-morph: A fast, accurate and general approach for automated detection and landmarking of biological structures in images" 2020* 

[4] *Irani, Allada.. "Highly versatile facial landmarks detection models using ensemble of regression trees with application" 2019*  

<p align="center">
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/illustration.jpg" width="450" />
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/schema3.png" width="200" /> 
</p>

   
# Distances calculation #

Once points are detected, collection of 46 distances are calculated : body length, head length, jaw length...

<p align="center">
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/schema4.png" width="400" />
</p>

# Sex prediction #

Finally, a machine learning model predicts the gender of the Three Spined Stickleback :  
<p align="center">
  <img src="https://github.com/RalphMasson/MorphoEpinoche/blob/master/images/gui2.png" width="800" />
</p>

