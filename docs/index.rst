Détecteur d'Erreurs de Prix
========================

Bienvenue dans la documentation du Détecteur d'Erreurs de Prix, un outil puissant pour surveiller et détecter les erreurs de prix sur les sites e-commerce.

Table des Matières
----------------

.. toctree::
   :maxdepth: 2
   :caption: Contenu:

   installation
   utilisation
   configuration
   architecture
   api
   tests
   deployment
   contribution

Fonctionnalités principales
-------------------------

* Détection automatique des erreurs de prix
* Interface utilisateur intuitive
* Notifications en temps réel
* Support multi-sources (Amazon, eBay, etc.)
* Analyse historique des prix

Guide rapide
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   git clone [url-du-repo]
   cd price-analyzer
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt

Configuration
~~~~~~~~~~~~

1. Copiez le fichier `.env.example` vers `.env`
2. Configurez vos variables d'environnement
3. Initialisez la base de données PostgreSQL

Utilisation
~~~~~~~~~~

.. code-block:: bash

   streamlit run src/main.py

Contribution
-----------

Nous accueillons toutes les contributions ! Consultez notre guide de contribution pour plus d'informations.

Licence
-------

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

Indices et tables
---------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`