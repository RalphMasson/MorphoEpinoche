### mise en forme du fichier de pointage


import pandas as pd

cheminModeleCSV = r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\Results_dataset10c.csv"
listeCoordonneesPourModele = pd.read_csv(cheminModeleCSV,sep=";")
listeLabel=  list(dict.fromkeys(listeCoordonneesPourModele['Label']))
listeLabel2 = list(listeCoordonneesPourModele['Label'])

k=-1
f = open(r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\rapports\v4.TPS",'w+')
for j in range(len(listeCoordonneesPourModele)):
    if j%10==0:
        f.write("LM=10\n")
        k+=1
    f.write(str(float(listeCoordonneesPourModele['X'].loc[j]))+" "+str(float(listeCoordonneesPourModele['Y'].loc[j]))+"\n")
    if j%10==9:
        f.write("IMAGE="+str(listeLabel[j//10])+"\n")
        f.write("ID="+str(k)+"\n")
f.close()


liste = os.listdir(r"C:\Users\MASSON\Desktop\POINTAGe\all")