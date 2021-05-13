python -c "import py2exe; py2exe.copier_spec()"
cd ..
cd code
pyinstaller interface.spec
cd ..
cd script
python -c "import py2exe; py2exe.supprimer_spec()"
python -c "import py2exe; py2exe.supprimer_build()"
python -c "import py2exe; py2exe.deplacer_exe()"
python -c "import py2exe; py2exe.supprimer_dist()"
python -c "import py2exe; py2exe.supprimer_pycache()"