#!/usr/bin/bash
chmod +x scripts/install_spacy.sh

# Install dependencies
# run only if on linux
if [ "$(uname)" == "Linux" ]; then
    sudo apt-get update
    sudo apt-get install -y python3
    sudo apt-get install -y python3-pip
fi


# Install python dependencies
pip3 install -r requirements.txt

# Run scripts folder 
bash ./scripts/install_spacy.sh
