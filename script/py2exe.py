import glob, os,shutil
chemin = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\script\\"
chemin2 = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\code\\"
chemin0 = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\"



def copier_spec():
    os.chdir(chemin)
    for file in glob.glob("*.spec"):
        shutil.copyfile(chemin+file,chemin2+file)



def supprimer_spec():
    os.chdir(chemin2)
    for file in glob.glob("*.spec"):
        os.remove(chemin2+file)

def supprimer_build():
    shutil.rmtree(chemin2+"build\\")
    shutil.rmtree(chemin+"build\\")

def deplacer_exe():
    chemin3 = chemin2+"dist\\"
    os.chdir(chemin3)
    for file in glob.glob("*.exe"):
        os.replace(chemin3+file,chemin0+"executable\\"+file)

def supprimer_dist():
    os.rmdir(chemin2+"dist\\")

def supprimer_pycache():
    all_folders = [x[0] for x in list(os.walk(chemin0))]
    for x in all_folders:
        if("__pycache__" in x):
            shutil.rmtree(x)
    try:
        os.rmdir(chemin+"dist\\")
    except:
        None