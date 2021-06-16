from graphviz import render
import glob, os
chemin = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\"
chemin2 = chemin+"code\\"
os.chdir(chemin2)

for file in glob.glob("*.dot"):
    render('dot','png',chemin+"code\\"+file)
    os.remove(chemin2+file)


def getNewVersion(chemin3):
    return str(max([int(os.listdir(chemin3)[i].split('v')[1].split('.')[0]) for i in range(len(os.listdir(chemin3)))])+1)


for file in glob.glob("*.png"):

    if('Classification' in file):
        chemin3 = chemin+"class_diagram\\IA_sexage\\"
        new_version = getNewVersion(chemin3)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('utils' in file):
        chemin3 = chemin+"class_diagram\\IA_tools\\"
        try:
            new_version = getNewVersion(chemin3)
            os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

        except:
            last_version = 0
            new_version = str(int(last_version)+1)
            os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('ml' in file):
        chemin3 = chemin+"class_diagram\\IA_morph\\"
        new_version = getNewVersion(chemin3)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('Fonctions' in file):
        chemin3 = chemin+"class_diagram\\XY_tools\\"
        new_version = getNewVersion(chemin3)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('Placement' in file):
        chemin3 = chemin+"class_diagram\\XY_compute\\"
        new_version = getNewVersion(chemin3)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('Normal' in file):
        chemin3 = chemin+"class_diagram\\GUI_normal\\"
        new_version = getNewVersion(chemin3)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('Little' in file):
        chemin3 = chemin+"class_diagram\\GUI_little\\"
        new_version = getNewVersion(chemin3)
        os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

    if('Update' in file):
        chemin3 = chemin+"class_diagram\\GUI_update\\"
        try:
            new_version = getNewVersion(chemin3)
            os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")

        except:
            last_version = 0
            new_version = str(int(last_version)+1)
            os.replace(chemin2+file,chemin3+"class_diagram_v"+new_version+".png")
