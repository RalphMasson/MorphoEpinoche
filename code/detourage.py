import sys,inspect
pypath = inspect.stack()[0][1]
pypath = pypath.split('\\')
pypath1 = '/'.join(pypath[:-1])
pypath3 = '/'.join(pypath[:-2])+"/executable"
pypath2 = '/'.join(pypath[:-2])
sys.path.insert(0,pypath1)
import os,glob,Fonctions

# path1 = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS\\"
# list_datasets = os.listdir(path1)
#
# total_image = []
# for x in list_datasets:
#     path = path1+x+"\\"
#     list_images = os.listdir(path)
#     new_list_images = []
#     for y in list_images:
#         y = path1+x+"\\"+y
#         new_list_images.append(y)
#
#     total_image = total_image + new_list_images
#
# total_image = ["" if not x.endswith(".JPG") else x for x in total_image]
# total_image = list(filter(None, total_image))
#


# Send and save the finished image
''' 0 à 199 fait : 200 pour l'instant'''
#from remove_bg_api import RemoveBg
# Initialize api wrapper
# removebg = RemoveBg('Wvq6yPrtHB9vX7s5hcVUDK24')
#
# for i in range(0,200):
#
#     input_path = total_image[i]
#     output_path = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_detoure\\"+total_image[i].split("\\")[-2]+"\\"+total_image[i].split("\\")[-1]
#     image = removebg.remove_bg_file(input_path=input_path, out_path=output_path, size="full", raw=False)
#


'''Dataset: 1, ok'''
path_img_pointe = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_pointe\\Dataset2\\"
path_img_detoure = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_detoure\\Dataset2\\"
# path_img_final = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_final\\Dataset1\\"

list = os.listdir(path_img_pointe)
import cv2
for x in list:
    path1 = path_img_pointe+x
    path2 = path_img_detoure+x
    img_final = Fonctions.Externes.traitement_final_pointage(path1,path2)
    path_final = "C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\DATASETS_final\\Dataset1\\"
    filename = path_final+x
    cv2.imwrite(filename,cv2.cvtColor(img_final, cv2.COLOR_RGB2BGR))
