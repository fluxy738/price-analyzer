Guide de Déploiement
==================

Ce guide détaille les différentes options de déploiement du Détecteur d'Erreurs de Prix.

Prérequis
--------

1. Système
~~~~~~~~

* Python 3.8+
* PostgreSQL 12+
* Git
* Supervisord (optionnel)
* Docker (optionnel)

2. Ressources Recommandées
~~~~~~~~~~~~~~~~~~~~~~~

* CPU : 2+ cœurs
* RAM : 4+ GB
* Stockage : 20+ GB
* Bande passante : 10+ Mbps

Déploiement Local
---------------

1. Installation
~~~~~~~~~~~~

.. code-block:: bash

    # Cloner le dépôt
    git clone <repository_url>
    cd price-analyzer

    # Environnement virtuel
    python -m venv venv
    source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows

    # Dépendances
    pip install -r requirements.txt

2. Configuration
~~~~~~~~~~~~~

.. code-block:: bash

    # Copier le template
    cp .env.example .env

    # Éditer les variables
    nano .env

3. Base de Données
~~~~~~~~~~~~~~~

.. code-block:: bash

    # Créer la base
    createdb price_analyzer

    # Initialiser les tables
    python scripts/init_db.py

4. Lancement
~~~~~~~~~~

.. code-block:: bash

    # Démarrer l'application
    streamlit run src/main.py

Déploiement Docker
---------------

1. Construction
~~~~~~~~~~~~

.. code-block:: dockerfile

    FROM python:3.8-slim

    WORKDIR /app
    COPY . .

    RUN pip install -r requirements.txt

    EXPOSE 8501
    CMD ["streamlit", "run", "src/main.py"]

2. Compose
~~~~~~~~

.. code-block:: yaml

    version: '3'
    services:
      web:
        build: .
        ports:
          - "8501:8501"
        env_file: .env
        depends_on:
          - db
      db:
        image: postgres:12
        environment:
          POSTGRES_DB: price_analyzer
          POSTGRES_PASSWORD: password

3. Déploiement
~~~~~~~~~~~

.. code-block:: bash

    # Construire et démarrer
    docker-compose up -d

    # Logs
    docker-compose logs -f

    # Arrêt
    docker-compose down

Déploiement Cloud
--------------

1. Heroku
~~~~~~~

.. code-block:: bash

    # Login
    heroku login

    # Créer l'application
    heroku create price-analyzer

    # Configuration
    heroku config:set $(cat .env)

    # Déploiement
    git push heroku main

2. AWS
~~~~

.. code-block:: bash

    # Configuration EB
    eb init -p python-3.8 price-analyzer

    # Créer l'environnement
    eb create production

    # Déploiement
    eb deploy

3. Google Cloud
~~~~~~~~~~~~

.. code-block:: bash

    # Build container
    gcloud builds submit --tag gcr.io/project/price-analyzer

    # Déployer
    gcloud run deploy --image gcr.io/project/price-analyzer

Supervision
----------

1. Supervisord
~~~~~~~~~~~

.. code-block:: ini

    [program:price-analyzer]
    command=/path/to/venv/bin/streamlit run src/main.py
    directory=/path/to/price-analyzer
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/price-analyzer.err.log
    stdout_logfile=/var/log/price-analyzer.out.log

2. Systemd
~~~~~~~~

.. code-block:: ini

    [Unit]
    Description=Price Analyzer
    After=network.target

    [Service]
    User=price-analyzer
    WorkingDirectory=/path/to/price-analyzer
    ExecStart=/path/to/venv/bin/streamlit run src/main.py
    Restart=always

    [Install]
    WantedBy=multi-user.target

Sauvegarde
---------

1. Base de Données
~~~~~~~~~~~~~~~

.. code-block:: bash

    # Backup
    pg_dump price_analyzer > backup.sql

    # Restore
    psql price_analyzer < backup.sql

2. Automatisation
~~~~~~~~~~~~~~

.. code-block:: bash

    #!/bin/bash
    # backup.sh
    DATE=$(date +%Y%m%d)
    BACKUP_DIR=/backups

    pg_dump price_analyzer > $BACKUP_DIR/backup_$DATE.sql
    find $BACKUP_DIR -mtime +7 -delete

Sécurité
-------

1. SSL/TLS
~~~~~~~~

.. code-block:: nginx

    server {
        listen 443 ssl;
        server_name price-analyzer.com;

        ssl_certificate /etc/letsencrypt/live/price-analyzer.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/price-analyzer.com/privkey.pem;

        location / {
            proxy_pass http://localhost:8501;
        }
    }

2. Firewall
~~~~~~~~~

.. code-block:: bash

    # UFW
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 5432/tcp

Maintenance
----------

1. Mises à Jour
~~~~~~~~~~~~

.. code-block:: bash

    # Code
    git pull
    pip install -r requirements.txt

    # Base de données
    python scripts/migrate_db.py

2. Monitoring
~~~~~~~~~~

.. code-block:: bash

    # Logs
    tail -f /var/log/price-analyzer.log

    # Métriques
    htop
    df -h

3. Alertes
~~~~~~~~

.. code-block:: python

    # monitoring.py
    def check_system_health():
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()

        if any([cpu_usage > 80, memory_usage > 80, disk_usage > 80]):
            send_alert('Ressources système critiques')