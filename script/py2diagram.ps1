cd ..
cd code
echo "Conversion du code en graphe"
Pyreverse -o dot -p Interface Interface_Sexage.py
Pyreverse -o dot -p Placement Placement.py
Pyreverse -o dot -p Classification Classification.py
Pyreverse -o dot -p Fonctions Fonctions.py
cd ..
cd script
echo "Conversion du graphe en image"
python py2diagram.py