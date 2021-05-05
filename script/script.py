from graphviz import render
import glob, os
os.chdir("C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\")
for file in glob.glob("*.dot"):
    render('dot','png','C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\'+file)
    os.remove('C:\\Users\\MASSON\\Desktop\\STAGE_EPINOCHE\\moduleMorpho\\'+file)