Guide des Tests
=============

Ce document décrit la stratégie de test et les procédures pour le Détecteur d'Erreurs de Prix.

Vue d'ensemble
------------

Notre suite de tests comprend :

1. Tests Unitaires
2. Tests d'Intégration
3. Tests de Performance
4. Tests de Bout en Bout

Configuration
-----------

1. Prérequis
~~~~~~~~~~

* pytest
* pytest-asyncio
* pytest-cov
* pytest-mock
* pytest-env

2. Structure
~~~~~~~~~~

.. code-block:: text

    tests/
    ├── unit/
    │   ├── test_scraper.py
    │   ├── test_analyzer.py
    │   ├── test_notifier.py
    │   └── test_db.py
    ├── integration/
    │   ├── test_scraper_db.py
    │   └── test_analyzer_notifier.py
    ├── performance/
    │   └── test_load.py
    ├── e2e/
    │   └── test_workflow.py
    └── conftest.py

Tests Unitaires
-------------

1. Scraper
~~~~~~~~

.. code-block:: python

    def test_product_parsing():
        """Test le parsing des données produit."""
        html = load_fixture('product.html')
        product = scraper.parse_product(html)
        assert product.name == 'Test Product'
        assert product.price == 99.99

2. Analyzer
~~~~~~~~~

.. code-block:: python

    def test_anomaly_detection():
        """Test la détection d'anomalies de prix."""
        products = create_test_products()
        alerts = analyzer.detect_anomalies(products)
        assert len(alerts) > 0
        assert alerts[0].confidence > 0.8

3. Notifier
~~~~~~~~~

.. code-block:: python

    async def test_email_notification():
        """Test l'envoi d'emails."""
        alert = create_test_alert()
        with mock_smtp():
            await notifier.send_email(alert)
            assert email_sent()

4. Database
~~~~~~~~~

.. code-block:: python

    def test_product_save():
        """Test la sauvegarde des produits."""
        product = create_test_product()
        product_id = db.save_product(product)
        assert product_id is not None
        saved = db.get_product(product_id)
        assert saved.name == product.name

Tests d'Intégration
-----------------

1. Configuration
~~~~~~~~~~~~~

.. code-block:: python

    @pytest.fixture
    def test_db():
        """Configure une base de test."""
        db = create_test_database()
        yield db
        db.cleanup()

2. Exemples
~~~~~~~~~

.. code-block:: python

    async def test_scraper_to_db():
        """Test l'intégration scraper-database."""
        products = await scraper.scrape_site('test')
        for product in products:
            db.save_product(product)
        assert db.count_products() == len(products)

Tests de Performance
-----------------

1. Configuration
~~~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.performance
    def test_scraper_speed():
        """Test les performances du scraper."""
        start = time.time()
        products = scraper.scrape_batch(100)
        duration = time.time() - start
        assert duration < 5  # Max 5 secondes

2. Charge
~~~~~~~

.. code-block:: python

    @pytest.mark.performance
    async def test_system_load():
        """Test la charge système."""
        async with load_test(100, 10):
            response = await system.process_batch()
            assert response.latency < 1000  # Max 1s

Tests de Bout en Bout
------------------

1. Workflow
~~~~~~~~~

.. code-block:: python

    @pytest.mark.e2e
    async def test_complete_workflow():
        """Test le workflow complet."""
        # Scraping
        products = await scraper.scrape_site('test')
        
        # Analyse
        alerts = analyzer.analyze_prices(products)
        
        # Notification
        await notifier.send_notifications(alerts)
        
        # Vérification
        assert notifications_received()
        assert db.alerts_saved()

Bonnes Pratiques
--------------

1. Fixtures
~~~~~~~~~

.. code-block:: python

    @pytest.fixture
    def mock_http():
        """Mock les requêtes HTTP."""
        with aioresponses() as m:
            yield m

2. Mocks
~~~~~~

.. code-block:: python

    def test_with_mock(mocker):
        """Utilisation des mocks."""
        mock_service = mocker.patch('service.call')
        mock_service.return_value = 'test'
        result = function_under_test()
        assert result == 'test'

3. Paramètres
~~~~~~~~~~~

.. code-block:: python

    @pytest.mark.parametrize('price,expected', [
        (100, True),
        (1000, False),
        (0, True)
    ])
    def test_price_validation(price, expected):
        """Test avec différents prix."""
        assert validate_price(price) == expected

Exécution
--------

1. Commandes
~~~~~~~~~~

.. code-block:: bash

    # Tous les tests
    pytest

    # Tests spécifiques
    pytest tests/unit/
    pytest tests/test_scraper.py
    pytest -k "test_price"

    # Avec coverage
    pytest --cov=src

2. Marqueurs
~~~~~~~~~~

.. code-block:: bash

    # Tests de performance
    pytest -m performance

    # Tests d'intégration
    pytest -m integration

    # Tests bout en bout
    pytest -m e2e

3. Options
~~~~~~~~

.. code-block:: bash

    # Verbeux
    pytest -v

    # Arrêt au premier échec
    pytest -x

    # Debug
    pytest --pdb

Rapports
-------

1. Coverage
~~~~~~~~~

.. code-block:: bash

    # Rapport HTML
    pytest --cov=src --cov-report=html

2. JUnit
~~~~~~

.. code-block:: bash

    # Rapport XML
    pytest --junitxml=report.xml