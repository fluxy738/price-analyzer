Guide de Contribution
===================

Nous sommes ravis que vous souhaitiez contribuer au projet Détecteur d'Erreurs de Prix ! Ce guide vous aidera à comprendre le processus de contribution.

Prérequis
--------

1. Environnement de Développement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Python 3.8+
* PostgreSQL 12+
* Git
* Make (optionnel)

2. Configuration Initiale
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Cloner le dépôt
    git clone <repository_url>
    cd price-analyzer

    # Créer l'environnement virtuel
    python -m venv venv
    source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows

    # Installer les dépendances
    make install  # ou pip install -r requirements.txt

Guidelines de Code
----------------

1. Style de Code
~~~~~~~~~~~~~

* Suivre PEP 8
* Utiliser Black pour le formatage
* Docstrings pour toutes les fonctions/classes
* Type hints pour les paramètres/retours

2. Tests
~~~~~~

* Tests unitaires obligatoires
* Coverage minimum de 80%
* Tests d'intégration pour les fonctionnalités majeures

3. Documentation
~~~~~~~~~~~~~

* Docstrings en format Google
* README à jour
* Documentation Sphinx complète
* Exemples de code

Processus de Contribution
----------------------

1. Issues
~~~~~~~

* Vérifier les issues existantes
* Créer une nouvelle issue descriptive
* Attendre la validation des mainteneurs

2. Branches
~~~~~~~~~

.. code-block:: text

    main
    ├── feature/xxx
    ├── bugfix/xxx
    └── docs/xxx

3. Commits
~~~~~~~~

.. code-block:: text

    feat: description
    fix: description
    docs: description
    test: description
    refactor: description

4. Pull Requests
~~~~~~~~~~~~~

* Branch à jour avec main
* Tests passants
* Documentation mise à jour
* Description claire

Développement
-----------

1. Commandes Make
~~~~~~~~~~~~~~

.. code-block:: bash

    make install    # Installation
    make test       # Tests
    make lint       # Vérification style
    make docs       # Documentation
    make clean      # Nettoyage

2. Tests
~~~~~~

.. code-block:: bash

    # Tests unitaires
    pytest tests/

    # Coverage
    pytest --cov=src tests/

    # Tests spécifiques
    pytest tests/test_scraper.py -k test_amazon

3. Documentation
~~~~~~~~~~~~~

.. code-block:: bash

    # Générer la documentation
    cd docs
    make html

Bonnes Pratiques
--------------

1. Code
~~~~~

* DRY (Don't Repeat Yourself)
* SOLID principles
* Gestion des erreurs
* Logging approprié

2. Tests
~~~~~~

* Tests isolés
* Mocks pour les API externes
* Fixtures réutilisables
* Tests de cas limites

3. Performance
~~~~~~~~~~~

* Optimisation des requêtes
* Mise en cache
* Asynchrone quand possible
* Profilage régulier

Débogage
-------

1. Logs
~~~~~

.. code-block:: python

    import logging

    logging.debug("Message de debug")
    logging.info("Information")
    logging.warning("Avertissement")
    logging.error("Erreur")

2. Débogueur
~~~~~~~~~~

.. code-block:: python

    import pdb
    pdb.set_trace()

3. Profilage
~~~~~~~~~~

.. code-block:: bash

    python -m cProfile -o output.prof script.py
    snakeviz output.prof

Publication
----------

1. Versioning
~~~~~~~~~~~

* Semantic Versioning (MAJOR.MINOR.PATCH)
* CHANGELOG.md à jour
* Tags Git

2. Release
~~~~~~~~

* Tests complets
* Documentation à jour
* CHANGELOG validé
* Tag créé

Support
------

* Issues GitHub
* Discussions
* Pull Requests
* Documentation