cd ..
cd code
echo "Conversion du code en graphe"
Pyreverse -o dot -p Interface_Normal Interface_Sexage_Normal.py
Pyreverse -o dot -p Interface_Little Interface_Sexage_Little.py
Pyreverse -o dot -p Placement Placement.py
Pyreverse -o dot -p Classification Classification.py
Pyreverse -o dot -p Fonctions Fonctions.py
Pyreverse -o dot -p ml_points modelPointageML.py
Pyreverse -o dot -p utils utilsML.py
cd ..
cd script
echo "Conversion du graphe en image"
python py2diagram.py
