from PIL import Image

import numpy as np

import PIL.ImageOps



img = Image.open(r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\test_pointage_ML\resultats\1_Modele.png")
b, g, r = img.split()
img = Image.merge("RGB", (r, g, b)).convert("RGBA")

background = Image.open(r"C:\Users\MASSON\Desktop\STAGE_EPINOCHE\moduleMorpho\test_pointage_ML\resultats\1_Cyril.png").convert("RGBA")

# background.paste(img, (0, 0), img)


blended = Image.blend(img, background, alpha=0.5)


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1)
ax.imshow(blended)

t = 1 ## alpha value
cmap = {1:[0.1,0.1,1.0,t],2:[1.0,0.1,0.1,t]}
labels = {1:'Pointage Modèle',2:'Pointage Cyril'}
patches =[mpatches.Patch(color=cmap[i],label=labels[i]) for i in cmap]
plt.legend(handles=patches)
plt.show()