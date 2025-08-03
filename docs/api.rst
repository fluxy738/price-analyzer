Documentation de l'API
===================

Cette section détaille l'API interne du Détecteur d'Erreurs de Prix.

Module Scraper
------------

Scraper
~~~~~~~

.. py:class:: scraper.Scraper

   Classe principale pour le scraping des sites e-commerce.

   .. py:method:: __init__()

      Initialise le scraper avec les configurations par défaut.

   .. py:method:: async scrape_site(site: str, query: str) -> List[Product]

      Scrape un site spécifique pour les produits correspondant à la requête.

      :param site: Nom du site à scraper (ex: 'amazon')
      :param query: Terme de recherche
      :return: Liste des produits trouvés

Product
~~~~~~~

.. py:class:: scraper.Product

   Dataclass représentant un produit.

   :param name: Nom du produit
   :param price: Prix actuel
   :param original_price: Prix original (optionnel)
   :param url: URL du produit
   :param site: Site source
   :param category: Catégorie du produit
   :param timestamp: Date de collecte

Module Analyzer
-------------

PriceAnalyzer
~~~~~~~~~~~~

.. py:class:: analyzer.PriceAnalyzer

   Classe pour l'analyse et la détection des anomalies de prix.

   .. py:method:: __init__()

      Initialise l'analyseur avec le modèle de détection d'anomalies.

   .. py:method:: analyze_prices(products: List[Product]) -> List[PriceAlert]

      Analyse une liste de produits pour détecter les anomalies de prix.

      :param products: Liste des produits à analyser
      :return: Liste des alertes générées

PriceAlert
~~~~~~~~~

.. py:class:: analyzer.PriceAlert

   Dataclass représentant une alerte de prix.

   :param product: Produit concerné
   :param confidence: Niveau de confiance (0-1)
   :param price_difference: Différence de prix
   :param timestamp: Date de détection
   :param alert_type: Type d'alerte ('low_price' ou 'price_drop')

Module Notifier
-------------

NotificationManager
~~~~~~~~~~~~~~~~~

.. py:class:: notifier.NotificationManager

   Gestionnaire des notifications multi-canaux.

   .. py:method:: __init__()

      Initialise le gestionnaire avec les configurations des différents canaux.

   .. py:method:: async send_notifications(alerts: List[PriceAlert]) -> None

      Envoie les notifications pour une liste d'alertes.

      :param alerts: Liste des alertes à notifier

   .. py:method:: async _send_email_alert(alert: PriceAlert) -> None

      Envoie une alerte par email.

   .. py:method:: async _send_telegram_alert(alert: PriceAlert) -> None

      Envoie une alerte via Telegram.

   .. py:method:: async _send_discord_alert(alert: PriceAlert) -> None

      Envoie une alerte via Discord.

Module Database
-------------

DatabaseManager
~~~~~~~~~~~~~

.. py:class:: database.DatabaseManager

   Gestionnaire de la base de données.

   .. py:method:: __init__()

      Initialise la connexion à la base de données et crée les tables.

   .. py:method:: save_product(product: Product) -> Optional[int]

      Sauvegarde un produit dans la base de données.

      :param product: Produit à sauvegarder
      :return: ID du produit ou None en cas d'erreur

   .. py:method:: save_alert(alert: PriceAlert) -> None

      Sauvegarde une alerte dans la base de données.

      :param alert: Alerte à sauvegarder

   .. py:method:: get_price_history(product_url: str) -> List[Dict]

      Récupère l'historique des prix d'un produit.

      :param product_url: URL du produit
      :return: Liste des prix historiques

   .. py:method:: get_recent_alerts(limit: int = 10) -> List[Dict]

      Récupère les alertes récentes.

      :param limit: Nombre maximum d'alertes à retourner
      :return: Liste des alertes récentes

Exemples d'Utilisation
-------------------

Scraping de Produits
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   scraper = Scraper()
   products = await scraper.scrape_site('amazon', 'smartphone')

Analyse des Prix
~~~~~~~~~~~~~~

.. code-block:: python

   analyzer = PriceAnalyzer()
   alerts = analyzer.analyze_prices(products)

Envoi de Notifications
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   notifier = NotificationManager()
   await notifier.send_notifications(alerts)

Gestion de la Base de Données
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   db = DatabaseManager()
   product_id = db.save_product(product)
   history = db.get_price_history(product.url)