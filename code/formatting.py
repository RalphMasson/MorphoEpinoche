## Mise en forme du fichier de pointage (imageJ -> tps)

import pandas as pd
import sys

def csv_to_tps(cheminFichierCSV):
    print("\n Lecture du fichier csv \n")
    print("\n Conversion du fichier en cours... \n")
    cheminDossierCSV = '\\'.join(cheminFichierCSV.split("\\")[:-1])
    listeCoordonneesPourModele = pd.read_csv(cheminFichierCSV,sep=";")
    listeLabel=  list(dict.fromkeys(listeCoordonneesPourModele['Label']))
    k=-1
    f = open(cheminDossierCSV+"\\v1_new.TPS",'w+')
    for j in range(len(listeCoordonneesPourModele)):
        # print("Conversion du fichier en cours... \n")
        if j%10==0:
            f.write("LM=10\n")
            k+=1
        f.write(str(float(listeCoordonneesPourModele['X'].loc[j]))+" "+str(float(listeCoordonneesPourModele['Y'].loc[j]))+"\n")
        if j%10==9:
            f.write("IMAGE="+str(listeLabel[k])+"\n")
            # print(listeLabel[j//10])
            # print(k)
            f.write("ID="+str(k+202)+"\n")
    f.close()
    print("\n Fichier tps crée \n")

if __name__ == "__main__":
    csv_to_tps(sys.argv[1])


