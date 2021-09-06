## Mise en forme du fichier de pointage (imageJ -> tps)


import pandas as pd

# cheminModeleCSV = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\Results_dataset10c.csv"
cheminModeleCSV = r"C:\Users\MASSON\Downloads\Dataset12\Results.csv"


listeCoordonneesPourModele = pd.read_csv(cheminModeleCSV,sep=";")
listeLabel=  list(dict.fromkeys(listeCoordonneesPourModele['Label']))
listeLabel2 = list(listeCoordonneesPourModele['Label'])

k=-1
f = open(r"C:\Users\MASSON\Downloads\Dataset12\v4.TPS",'w+')
for j in range(len(listeCoordonneesPourModele)):
    if j%10==0:
        f.write("LM=10\n")
        k+=1
    f.write(str(float(listeCoordonneesPourModele['X'].loc[j]))+" "+str(float(listeCoordonneesPourModele['Y'].loc[j]))+"\n")
    if j%10==9:
        f.write("IMAGE="+str(listeLabel[k])+"\n")
        print(listeLabel[j//10])
        print(k)
        f.write("ID="+str(k+202)+"\n")
f.close()


liste = os.listdir(r"C:\Users\MASSON\Downloads\Dataset12")



####
def filter_rows_by_values(df, col, values):
    return df[df[col].isin(values) == True]

import os,shutil
path1 = "C:\\Users\\MASSON\\Desktop\\POINTAGe\\all\\"
pathInit = "C:\\Users\\MASSON\\Desktop\\POINTAGe\\prog\\"
listeDossier = os.listdir("C:\\Users\\MASSON\\Desktop\\POINTAGe\\prog\\")
listeAllImage = os.listdir("C:\\Users\\MASSON\\Desktop\\POINTAGe\\all\\")

# # for x in listeDossier:
# #     # cheminModeleCSV = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\Results_dataset10c.csv"
# #     # listeCoordonneesPourModele = pd.read_csv(cheminModeleCSV,sep=";")
# #     print(pathInit+x)
# #     listeImages = os.listdir(pathInit+x+"\\all")
# #     print(len(listeImages))
# #     listeCoordonneesPourModele2 = filter_rows_by_values(listeCoordonneesPourModele,"Label",listeImages).reset_index(drop=True)
# #     listeLabel=  list(dict.fromkeys(listeCoordonneesPourModele2['Label']))
# #
# #     # print(listeCoordonneesPourModele2)
# #     k=-1
# #     f = open(pathInit+x+"\\all\\v2.TPS",'w+')
# #     for j in range(len(listeCoordonneesPourModele2)):
# #         if j%10==0:
# #             f.write("LM=10\n")
# #             k+=1
# #         f.write(str(float(listeCoordonneesPourModele2['X'].loc[j]))+" "+str(float(listeCoordonneesPourModele2['Y'].loc[j]))+"\n")
# #         if j%10==9:
# #             f.write("IMAGE="+str(listeLabel[j//10])+"\n")
# #             f.write("ID="+str(k)+"\n")
# #     f.close()


