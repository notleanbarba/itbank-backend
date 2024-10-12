#!/bin/bash

cd dist
pip install --user itbank*.whl
cd ..
cp ./itbank/itbankcli.sh $HOME/.local/bin/itbankcli
chmod +x $HOME/.local/bin/itbankcli
