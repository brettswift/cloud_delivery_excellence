#!/usr/bin/env bash

echo "Setting up dev env with .venv"
python3 -m venv .venv
pip install -r requirements.txt

echo ""
echo "Your turn: "
echo "activate .venv with:  . .venv/bin/activate "
