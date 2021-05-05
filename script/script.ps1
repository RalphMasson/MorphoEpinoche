cd ..
Pyreverse -o dot -p Interface Interface_Sexage.py
Pyreverse -o dot -p Placement Placement.py
Pyreverse -o dot -p Classification Classification.py
Pyreverse -o dot -p Fonctions Fonctions.py
cd script
python script.py