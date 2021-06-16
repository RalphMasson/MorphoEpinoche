cd ..
cd code
echo "Conversion du code en graphe"
Pyreverse -o dot -p Interface_Normal GUI_normal.py
Pyreverse -o dot -p Interface_Little GUI_little.py
Pyreverse -o dot -p Placement XY_compute.py
Pyreverse -o dot -p Fonctions XY_tools.py
Pyreverse -o dot -p Classification IA_sexage.py
Pyreverse -o dot -p ml_points IA_morph.py
Pyreverse -o dot -p utils IA_tools.py
cd ..
cd script
echo "Conversion du graphe en image"
python py2diagram.py
