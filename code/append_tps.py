## Append 2 tps files
import sys
import pandas as pd

def append_2_tps_files(fileV1,fileV2_temp,cheminV2):
    print("\nLecture des fichiers en cours...\n\n")
    f0 = open(fileV1,'r')
    f0 = f0.read()
    f1 = open(fileV2_temp,'r')
    f1 = f1.read()
    f2 = f0+f1
    print("Concatenation des fichiers en cours...\n\n")
    f3 = open(cheminV2+"\\v2_v.TPS",'w+')
    f3.write(f2)
    print("Renumerotation des ID en cours.. \n\n")
    f3.close()
    correct_id(cheminV2+"\\v2_v.TPS",cheminV2)
    print("Fichier final ok v2.TPS... \n\n")



def correct_id(fileV2,cheminV2):
    import pandas as pd
    import os

    df = pd.read_csv(fileV2, delimiter = "\t",header=None)
    nb_image = len(df[(df[0]=='LM=10')])
    liste_id = list(range(nb_image))
    k=0
    for i in range(len(df)):
        if('ID=' in df.loc[i][0]):
            df.loc[i] = "ID="+str(liste_id[k])
            k+=1

    df.to_csv(cheminV2+"\\v2_temp2.TPS", header=None, index=None, sep=' ', mode='a')
    f1 = open(cheminV2+"\\v2_temp2.TPS",'r')
    f2 = open(cheminV2+"\\v2.TPS",'w+')
    ff = f1.read()
    ff=ff.replace('"','')
    f2.write(ff)
    f2.close()
    f1.close()
    os.remove(cheminV2+"\\v2_temp2.TPS")
    os.remove(cheminV2+"\\v2_v.TPS")

if __name__ == "__main__":
    append_2_tps_files(sys.argv[1],sys.argv[2],sys.argv[3])

