Guide de Configuration
====================

Ce guide détaille toutes les options de configuration disponibles pour le Détecteur d'Erreurs de Prix.

Configuration de Base
------------------

1. Variables d'Environnement
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Base de données
    DATABASE_URL=postgresql://user:password@localhost:5432/price_analyzer
    DATABASE_POOL_SIZE=10
    DATABASE_MAX_OVERFLOW=20

    # Scraping
    SCRAPING_INTERVAL=3600  # secondes
    MAX_CONCURRENT_REQUESTS=5
    REQUEST_TIMEOUT=30
    USER_AGENT_ROTATION=true

    # Analyse
    ANOMALY_THRESHOLD=0.8
    MIN_PRICE_DIFFERENCE=20
    PRICE_HISTORY_DAYS=30

    # Notifications
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=your@email.com
    SMTP_PASSWORD=your_password

    TELEGRAM_BOT_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id

    DISCORD_WEBHOOK_URL=your_webhook_url

2. Fichier .env
~~~~~~~~~~~~

.. code-block:: text

    # .env.example
    # Copier vers .env et configurer

    # Application
    APP_NAME=Price Analyzer
    DEBUG=false
    LOG_LEVEL=INFO

    # Base de données
    DATABASE_URL=postgresql://user:password@localhost:5432/price_analyzer

    # Notifications
    ENABLE_EMAIL=true
    ENABLE_TELEGRAM=true
    ENABLE_DISCORD=true

Configuration Avancée
-------------------

1. Scraping
~~~~~~~~~

.. code-block:: python

    # config/scraping.py
    SCRAPING_CONFIG = {
        'amazon': {
            'base_url': 'https://www.amazon.fr',
            'selectors': {
                'name': '#productTitle',
                'price': '#price_inside_buybox',
                'original_price': '#priceblock_ourprice'
            },
            'headers': {
                'Accept-Language': 'fr-FR'
            }
        },
        'cdiscount': {
            'base_url': 'https://www.cdiscount.com',
            'selectors': {
                'name': 'h1',
                'price': '#fpPrice',
                'original_price': '#strikedPrice'
            }
        }
    }

2. Analyse
~~~~~~~~

.. code-block:: python

    # config/analysis.py
    ANALYSIS_CONFIG = {
        'anomaly_detection': {
            'model': 'isolation_forest',
            'params': {
                'contamination': 0.1,
                'random_state': 42
            }
        },
        'price_drop': {
            'min_percentage': 20,
            'min_absolute': 10
        },
        'categories': {
            'smartphone': {
                'min_price': 100,
                'max_price': 2000
            },
            'laptop': {
                'min_price': 300,
                'max_price': 5000
            }
        }
    }

3. Notifications
~~~~~~~~~~~~~

.. code-block:: python

    # config/notifications.py
    NOTIFICATION_CONFIG = {
        'email': {
            'template': 'templates/email.html',
            'subject': 'Alerte Prix - {product_name}',
            'from': 'alerts@price-analyzer.com'
        },
        'telegram': {
            'template': 'templates/telegram.md',
            'parse_mode': 'Markdown'
        },
        'discord': {
            'template': 'templates/discord.json',
            'username': 'Price Analyzer Bot'
        }
    }

Configuration de Logging
---------------------

1. Fichier
~~~~~~~~

.. code-block:: python

    # config/logging.py
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/price_analyzer.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'INFO'
            }
        }
    }

2. Sentry
~~~~~~~

.. code-block:: python

    # config/sentry.py
    SENTRY_CONFIG = {
        'dsn': 'your-sentry-dsn',
        'environment': 'production',
        'traces_sample_rate': 0.1
    }

Configuration de Cache
-------------------

1. Redis
~~~~~~

.. code-block:: python

    # config/cache.py
    REDIS_CONFIG = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,
        'ttl': 3600  # 1 heure
    }

2. Mémoire
~~~~~~~~

.. code-block:: python

    # config/cache.py
    MEMORY_CACHE_CONFIG = {
        'ttl': 1800,  # 30 minutes
        'max_size': 1000  # entrées
    }

Configuration de l'Interface
-------------------------

1. Streamlit
~~~~~~~~~~

.. code-block:: python

    # config/ui.py
    STREAMLIT_CONFIG = {
        'page_title': 'Détecteur d\'Erreurs de Prix',
        'page_icon': '💰',
        'layout': 'wide',
        'initial_sidebar_state': 'expanded'
    }

2. Thème
~~~~~~

.. code-block:: python

    # config/theme.py
    THEME_CONFIG = {
        'primaryColor': '#FF4B4B',
        'backgroundColor': '#FFFFFF',
        'secondaryBackgroundColor': '#F0F2F6',
        'textColor': '#262730',
        'font': 'sans serif'
    }

Configuration des Tests
--------------------

1. Pytest
~~~~~~~

.. code-block:: ini

    # pytest.ini
    [pytest]
    testpaths = tests
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    addopts = --verbose --cov=src --cov-report=html

2. Coverage
~~~~~~~~~

.. code-block:: ini

    # .coveragerc
    [run]
    source = src
    omit = tests/*

    [report]
    exclude_lines =
        pragma: no cover
        def __repr__
        raise NotImplementedError