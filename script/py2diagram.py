from graphviz import render
import glob, os
chemin = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\"
chemin2 = chemin+"code\\"
os.chdir(chemin2)

for file in glob.glob("*.dot"):
    render('dot','png',chemin+"code\\"+file)
    os.remove(chemin2+file)

for file in glob.glob("*.png"):
    if('Classification' in file):
        chemin3 = chemin+"class_diagram\\classification\\"
        liste_fichiers = os.listdir(chemin3)
        liste_version = [liste_fichiers[i][-5] for i in range(len(liste_fichiers))]
        last_version = max(liste_version)
        new_version = str(int(last_version)+1)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")
    if('Fonctions' in file):
        chemin3 = chemin+"class_diagram\\fonctions\\"
        liste_fichiers = os.listdir(chemin3)
        liste_version = [liste_fichiers[i][-5] for i in range(len(liste_fichiers))]
        last_version = max(liste_version)
        new_version = str(int(last_version)+1)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")
    if('Normal' in file):
        chemin3 = chemin+"class_diagram\\interface\\"
        liste_fichiers = os.listdir(chemin3)
        liste_version = [liste_fichiers[i][-5] for i in range(len(liste_fichiers))]
        last_version = max(liste_version)
        new_version = str(int(last_version)+1)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")
    if('Little' in file):
        chemin3 = chemin+"class_diagram\\interface_mini\\"
        liste_fichiers = os.listdir(chemin3)
        try:
            liste_version = [liste_fichiers[i][-5] for i in range(len(liste_fichiers))]
            last_version = max(liste_version)
            new_version = str(int(last_version)+1)
            os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")
        except:
            last_version = 1
            new_version = str(int(last_version)+1)
            os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")
    if('Placement' in file):
        chemin3 = chemin+"class_diagram\\placement\\"
        liste_fichiers = os.listdir(chemin3)
        liste_version = [liste_fichiers[i][-5] for i in range(len(liste_fichiers))]
        last_version = max(liste_version)
        new_version = str(int(last_version)+1)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")