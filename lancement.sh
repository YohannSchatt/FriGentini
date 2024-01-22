#!/bin/bash

lancement() {
    echo "lancement du script"
    cd ~/frigentini/Python/
    streamlit run Menu.py & python3 main.py && fg
}
lancement
