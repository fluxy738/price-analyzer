Guide d'Installation
==================

Ce guide vous aidera à installer et configurer le Détecteur d'Erreurs de Prix sur votre système.

Prérequis
---------

* Python 3.8 ou supérieur
* PostgreSQL 12 ou supérieur
* Git
* Compte développeur pour les API (optionnel):
    * Telegram Bot
    * Discord Webhook

Installation
-----------

1. Clonez le repository
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone [url-du-repo]
   cd price-analyzer

2. Créez un environnement virtuel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Windows:**

.. code-block:: bash

   python -m venv venv
   .\venv\Scripts\activate

**Linux/Mac:**

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate

3. Installez les dépendances
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

4. Configuration de l'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Copiez le fichier d'exemple:

   .. code-block:: bash

      cp .env.example .env

2. Modifiez le fichier `.env` avec vos paramètres:

   .. code-block:: ini

      # Configuration de la base de données
      DB_NAME=price_analyzer
      DB_USER=votre_utilisateur
      DB_PASSWORD=votre_mot_de_passe
      DB_HOST=localhost
      DB_PORT=5432

      # Configuration email
      EMAIL_SENDER=votre_email@gmail.com
      EMAIL_PASSWORD=votre_mot_de_passe_app

      # Configuration Telegram
      TELEGRAM_TOKEN=votre_token_bot
      TELEGRAM_CHAT_ID=votre_chat_id

      # Configuration Discord
      DISCORD_WEBHOOK_URL=votre_webhook_url

5. Configuration de la base de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Créez une base de données PostgreSQL:

   .. code-block:: sql

      CREATE DATABASE price_analyzer;

2. La structure de la base de données sera automatiquement créée au premier lancement.

Vérification de l'installation
---------------------------

1. Lancez les tests:

   .. code-block:: bash

      pytest

2. Démarrez l'application:

   .. code-block:: bash

      streamlit run src/main.py

3. Ouvrez votre navigateur à l'adresse: ``http://localhost:8501``

Utilisation avec Make
------------------

Le projet inclut un Makefile pour simplifier les tâches courantes:

.. code-block:: bash

   make setup     # Installation complète
   make install   # Installation des dépendances
   make test      # Exécution des tests
   make lint      # Vérification du style de code
   make clean     # Nettoyage des fichiers temporaires
   make run       # Lancement de l'application

Dépannage
--------

Problèmes courants:

1. Erreur de connexion à la base de données
   
   * Vérifiez que PostgreSQL est en cours d'exécution
   * Vérifiez les informations de connexion dans `.env`
   * Vérifiez les droits d'accès de l'utilisateur

2. Erreur lors de l'installation des dépendances
   
   * Mettez à jour pip: ``pip install --upgrade pip``
   * Installez les outils de build: ``pip install wheel setuptools``

3. Erreur de notification
   
   * Vérifiez les tokens et URLs dans `.env`
   * Vérifiez la connexion internet
   * Vérifiez les logs pour plus de détails

Support
-------

Si vous rencontrez des problèmes:

1. Consultez les issues GitHub
2. Créez une nouvelle issue avec:
   * Description détaillée du problème
   * Logs d'erreur
   * Étapes pour reproduire
   * Environnement (OS, versions)