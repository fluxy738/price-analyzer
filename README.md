# Détecteur d'Erreurs de Prix 💰

Un logiciel intelligent pour détecter automatiquement les erreurs de prix sur les sites e-commerce.

## Fonctionnalités

- 🔍 **Détection Automatique** : Scan continu des sites e-commerce pour identifier les erreurs de prix
- 📊 **Interface Simple** : Dashboard intuitif avec filtres et historique
- ⚡ **Alertes Temps Réel** : Notifications instantanées par email, Telegram et Discord
- 📈 **Historique des Prix** : Suivi de l'évolution des prix et détection des tendances
- 🌐 **Multi-Sources** : Surveillance de plusieurs sites marchands (Amazon, eBay, etc.)

## Installation

1. Clonez le repository :
```bash
git clone [url-du-repo]
cd price-analyzer
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement :
```bash
cp .env.example .env
```
Modifiez le fichier `.env` avec vos propres paramètres.

5. Initialisez la base de données PostgreSQL et créez une base de données nommée `price_analyzer`

## Utilisation

1. Lancez l'application :
```bash
streamlit run src/main.py
```

2. Accédez à l'interface via votre navigateur à l'adresse : `http://localhost:8501`

## Configuration

### Base de données
- `DB_NAME` : Nom de la base de données
- `DB_USER` : Nom d'utilisateur PostgreSQL
- `DB_PASSWORD` : Mot de passe PostgreSQL
- `DB_HOST` : Hôte de la base de données
- `DB_PORT` : Port de la base de données

### Notifications
- `EMAIL_SENDER` : Adresse email pour l'envoi des notifications
- `EMAIL_PASSWORD` : Mot de passe de l'email (mot de passe d'application pour Gmail)
- `TELEGRAM_TOKEN` : Token du bot Telegram
- `TELEGRAM_CHAT_ID` : ID du chat Telegram
- `DISCORD_WEBHOOK_URL` : URL du webhook Discord

## Structure du Projet

```
├── src/
│   ├── analyzer/        # Analyse des prix et détection d'anomalies
│   ├── database/        # Gestion de la base de données
│   ├── notifier/        # Système de notifications
│   ├── scraper/         # Collecte des données de prix
│   └── main.py          # Point d'entrée de l'application
├── .env                 # Variables d'environnement
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.