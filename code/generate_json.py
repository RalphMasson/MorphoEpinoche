## Generate json file
import sys
import os
def generate_json(pathJson09,pathNew,versionModelePointage):


    f = open(pathJson09)
    fjson = f.read()

    filedata = fjson.replace('C:/Users/MASSON/Desktop/STAGE_EPINOCHE/moduleMorpho', 'C:/Users/MASSON/Desktop/STAGE_EPINOCHE/modoleMorpho')
    filedata = filedata.replace('predictor_head2.dat', 'predictor_head'+versionModelePointage+".dat")


    f.close()
    print("\\".join(pathJson09.split("\\")[:-1])+"\\new_json.json")
    new_json = open("\\".join(pathJson09.split("\\")[:-1])+"\\new_json.json",'w')
    new_json.write(filedata)
    new_json.close()
    print("\n#############################")
    print("\n##### Fichier Json ok #####\n")
    print("#############################\n")




if __name__ == "__main__":
    generate_json(sys.argv[1],sys.argv[2],sys.argv[3])


