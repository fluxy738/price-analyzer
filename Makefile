# Variables
PYTHON = python
PIP = pip
VENV = venv
TESTS = tests

# Commandes Windows
ifeq ($(OS),Windows_NT)
	PYTHON_VENV = .\$(VENV)\Scripts\python
	PIP_VENV = .\$(VENV)\Scripts\pip
	ACTIVATE = .\$(VENV)\Scripts\activate
	SEP = \\
else
	PYTHON_VENV = ./$(VENV)/bin/python
	PIP_VENV = ./$(VENV)/bin/pip
	ACTIVATE = . ./$(VENV)/bin/activate
	SEP = /
endif

.PHONY: help setup install test lint clean run

help:
	@echo "Commandes disponibles:"
	@echo "  make setup    - Crée l'environnement virtuel et installe les dépendances"
	@echo "  make install  - Installe les dépendances"
	@echo "  make test     - Lance les tests"
	@echo "  make lint     - Vérifie le style du code"
	@echo "  make clean    - Nettoie les fichiers temporaires"
	@echo "  make run      - Lance l'application"

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP_VENV) install --upgrade pip
	$(PIP_VENV) install -r requirements.txt

install:
	$(PIP_VENV) install -r requirements.txt

test:
	$(PYTHON_VENV) -m pytest $(TESTS)

lint:
	$(PYTHON_VENV) -m flake8 src tests
	$(PYTHON_VENV) -m black src tests --check

clean:
	rd /s /q __pycache__ 2>nul || true
	rd /s /q .pytest_cache 2>nul || true
	rd /s /q build 2>nul || true
	rd /s /q dist 2>nul || true
	rd /s /q *.egg-info 2>nul || true
	del /f /q .coverage 2>nul || true

# Lance l'application
run:
	$(PYTHON_VENV) -m streamlit run src$(SEP)main.py