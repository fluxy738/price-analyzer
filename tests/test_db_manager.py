import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.scraper.scraper import Product
from src.analyzer.price_analyzer import PriceAlert

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Mock les variables d'environnement
        self.env_patcher = patch.dict('os.environ', {
            'DB_NAME': 'test_db',
            'DB_USER': 'test_user',
            'DB_PASSWORD': 'test_password',
            'DB_HOST': 'localhost',
            'DB_PORT': '5432'
        })
        self.env_patcher.start()
        
        self.db_manager = DatabaseManager()
        self.sample_product = Product(
            name="Test Product",
            price=99.99,
            original_price=199.99,
            url="https://example.com/test",
            site="amazon",
            category="Électronique",
            timestamp=datetime.now()
        )
        self.sample_alert = PriceAlert(
            product=self.sample_product,
            confidence=0.95,
            price_difference=100.0,
            timestamp=datetime.now(),
            alert_type='price_drop'
        )

    def tearDown(self):
        self.env_patcher.stop()

    @patch('psycopg2.connect')
    def test_init_database(self, mock_connect):
        """Teste l'initialisation de la base de données."""
        # Configure le mock
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Initialise la base de données
        self.db_manager._init_database()

        # Vérifie que les tables ont été créées
        self.assertEqual(mock_cursor.execute.call_count, 3)
        calls = mock_cursor.execute.call_args_list
        self.assertTrue(any('CREATE TABLE IF NOT EXISTS products' in str(call) for call in calls))
        self.assertTrue(any('CREATE TABLE IF NOT EXISTS price_history' in str(call) for call in calls))
        self.assertTrue(any('CREATE TABLE IF NOT EXISTS alerts' in str(call) for call in calls))

    @patch('psycopg2.connect')
    def test_save_product(self, mock_connect):
        """Teste la sauvegarde d'un produit."""
        # Configure le mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Simule l'ID retourné
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Sauvegarde le produit
        product_id = self.db_manager.save_product(self.sample_product)

        # Vérifie que le produit a été sauvegardé
        self.assertIsNotNone(product_id)
        self.assertEqual(product_id, 1)

        # Vérifie les requêtes SQL
        calls = mock_cursor.execute.call_args_list
        self.assertTrue(any('SELECT id FROM products WHERE url =' in str(call) for call in calls))
        self.assertTrue(any('INSERT INTO price_history' in str(call) for call in calls))

    @patch('psycopg2.connect')
    def test_save_alert(self, mock_connect):
        """Teste la sauvegarde d'une alerte."""
        # Configure le mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Simule l'ID du produit
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Sauvegarde l'alerte
        self.db_manager.save_alert(self.sample_alert)

        # Vérifie les requêtes SQL
        calls = mock_cursor.execute.call_args_list
        self.assertTrue(any('INSERT INTO alerts' in str(call) for call in calls))

    @patch('psycopg2.connect')
    def test_get_price_history(self, mock_connect):
        """Teste la récupération de l'historique des prix."""
        # Prépare les données de test
        test_history = [
            {'price': 99.99, 'timestamp': datetime.now()},
            {'price': 149.99, 'timestamp': datetime.now()}
        ]

        # Configure le mock
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = test_history
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Récupère l'historique
        history = self.db_manager.get_price_history("https://example.com/test")

        # Vérifie les résultats
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['price'], 99.99)

    @patch('psycopg2.connect')
    def test_get_recent_alerts(self, mock_connect):
        """Teste la récupération des alertes récentes."""
        # Prépare les données de test
        test_alerts = [
            {
                'id': 1,
                'price': 99.99,
                'original_price': 199.99,
                'confidence': 0.95,
                'price_difference': 100.0,
                'alert_type': 'price_drop',
                'name': 'Test Product',
                'url': 'https://example.com/test',
                'site': 'amazon',
                'category': 'Électronique'
            }
        ]

        # Configure le mock
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = test_alerts
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Récupère les alertes
        alerts = self.db_manager.get_recent_alerts(limit=5)

        # Vérifie les résultats
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['price'], 99.99)
        self.assertEqual(alerts[0]['name'], 'Test Product')

    @patch('psycopg2.connect')
    def test_error_handling(self, mock_connect):
        """Teste la gestion des erreurs de base de données."""
        # Simule une erreur de connexion
        mock_connect.side_effect = Exception("Erreur de connexion")

        # Vérifie que les méthodes gèrent gracieusement les erreurs
        product_id = self.db_manager.save_product(self.sample_product)
        self.assertIsNone(product_id)

        history = self.db_manager.get_price_history("https://example.com/test")
        self.assertEqual(len(history), 0)

        alerts = self.db_manager.get_recent_alerts()
        self.assertEqual(len(alerts), 0)

if __name__ == '__main__':
    unittest.main()