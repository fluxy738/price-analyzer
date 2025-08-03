Guide d'Utilisation
=================

Ce guide explique comment utiliser efficacement le Détecteur d'Erreurs de Prix.

Interface Principale
------------------

L'interface utilisateur est divisée en plusieurs sections:

1. Barre latérale
~~~~~~~~~~~~~~~

* **Filtres de prix**:
    * Prix minimum
    * Prix maximum
    * Catégorie de produits

* **Configuration**:
    * Seuils d'alerte
    * Fréquence de scan
    * Sources de données

2. Tableau de bord principal
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Alertes récentes**:
    * Liste des dernières erreurs de prix détectées
    * Pourcentage de réduction
    * Niveau de confiance

* **Statistiques**:
    * Nombre total d'alertes
    * Économies potentielles
    * Taux de succès

3. Liste des produits
~~~~~~~~~~~~~~~~~~

* Affichage détaillé des produits détectés
* Tri par différents critères
* Filtrage avancé

Configuration des Alertes
-----------------------

1. Email
~~~~~~~

* Configurez votre adresse email dans `.env`
* Personnalisez la fréquence des notifications
* Définissez des seuils de prix personnalisés

2. Telegram
~~~~~~~~~~

* Créez un bot Telegram avec @BotFather
* Configurez le token dans `.env`
* Ajoutez le bot à votre groupe/canal
* Récupérez le chat_id

3. Discord
~~~~~~~~~

* Créez un webhook Discord
* Configurez l'URL dans `.env`
* Personnalisez le format des messages

Utilisation Avancée
-----------------

1. Filtres personnalisés
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Exemple de filtre personnalisé
   min_price = 100
   max_price = 1000
   category = "Électronique"
   reduction_min = 50  # %

2. Exportation des données
~~~~~~~~~~~~~~~~~~~~~~~

* Format CSV
* Format JSON
* Historique des prix
* Statistiques détaillées

3. Automatisation
~~~~~~~~~~~~~~~

* Planification des scans
* Rapports automatiques
* Intégration avec d'autres outils

Bonnes Pratiques
--------------

1. Configuration optimale
~~~~~~~~~~~~~~~~~~~~~~

* Définissez des seuils réalistes
* Évitez les plages de prix trop larges
* Utilisez des catégories spécifiques

2. Gestion des alertes
~~~~~~~~~~~~~~~~~~~

* Vérifiez régulièrement les alertes
* Validez les réductions importantes
* Suivez l'historique des prix

3. Maintenance
~~~~~~~~~~~~

* Mettez à jour régulièrement les sources
* Surveillez les logs d'erreurs
* Ajustez les seuils si nécessaire

Dépannage
--------

1. Problèmes courants
~~~~~~~~~~~~~~~~~~

* **Pas d'alertes**:
    * Vérifiez la connexion internet
    * Vérifiez les seuils configurés
    * Consultez les logs

* **Fausses alertes**:
    * Ajustez les seuils de confiance
    * Affinez les catégories
    * Mettez à jour les sources

* **Notifications**:
    * Vérifiez la configuration
    * Testez les connexions
    * Consultez les logs

2. Solutions
~~~~~~~~~~

* Redémarrez l'application
* Vérifiez la configuration
* Consultez la documentation
* Créez une issue GitHub

Astuces et Conseils
-----------------

1. Performance
~~~~~~~~~~~~

* Limitez le nombre de sources
* Optimisez les intervalles de scan
* Utilisez des filtres précis

2. Fiabilité
~~~~~~~~~~

* Vérifiez les prix manuellement
* Maintenez une liste blanche
* Documentez les faux positifs

3. Personnalisation
~~~~~~~~~~~~~~~~

* Créez des filtres personnalisés
* Adaptez les seuils par catégorie
* Personnalisez les notifications