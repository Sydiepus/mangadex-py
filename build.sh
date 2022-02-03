if python --version 2>&1 | grep -q '^Python 3\.'; then
    python setup.py sdist bdist_wheel
else
    python3 setup.py sdist bdist_wheel
fi
twine check dist/*
echo "Removing unneeded directories."
rm -r Sydiepus_mangadex_py.egg-info build