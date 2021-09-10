## Vérification de l'installation des bibliothèques


def verif():
    print("Installation des bibliotheques suivantes ; \n")
    print("\t -numpy \n")
    print("\t -scipy \n")
    print("\t -sklearn \n")
    print("\t -pillow \n")
    print("\t -pandas \n")
    print("\t -opencv \n")
    print("\t -xgboost \n")
    print("\t -cmake \n\n")


    import os
    os.system("powershell.exe pip install numpy")
    os.system("powershell.exe pip install scipy")
    os.system("powershell.exe pip install sklearn")
    os.system("powershell.exe pip install pillow")
    os.system("powershell.exe pip install pandas")
    os.system("powershell.exe pip install opencv-contrib-python")
    os.system("powershell.exe pip install xgboost")
    os.system("powershell.exe pip install cmake")

    print("\n\nVérification\n\n")

    try:
        import sklearn
        print("\tsklearn ok\n")
    except (ModuleNotFoundError,ImportError) as e:
        print("\tSklearn non installé\n")

    try:
        import scipy
        print("\tscipy ok\n")

    except (ModuleNotFoundError,ImportError) as e:
        print("\tscipy non installé\n")

    try:
        import numpy
        print("\tnumpy ok\n")

    except (ModuleNotFoundError,ImportError) as e:
        print("\tnumpy non installé\n")

    try:
        import PIL
        print("\tPIL ok\n")
    except (ModuleNotFoundError,ImportError) as e:
        print("\tPIL non installé\n")
    try:
        import cv2
        print("\topencv ok\n")

    except (ModuleNotFoundError,ImportError) as e:
        print("\topencv non installé\n")

    try:
        import pandas
        print("\tpandas ok\n")

    except (ModuleNotFoundError,ImportError) as e:
        print("\tpandas non installé\n")

    try:
        import xgboost
        print("\txgboost ok\n")

    except (ModuleNotFoundError,ImportError) as e:
        print("\txgboost non installé\n")

    try:
        import cmake
        print("\tcmake ok\n")

    except (ModuleNotFoundError,ImportError) as e:
        print("\tcmake non installé\n")

if __name__ == "__main__":
    verif()