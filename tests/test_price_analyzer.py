import unittest
from datetime import datetime
from src.analyzer.price_analyzer import PriceAnalyzer, PriceAlert
from src.scraper.scraper import Product

class TestPriceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PriceAnalyzer()
        self.sample_products = [
            Product(
                name="Smartphone Test",
                price=299.99,
                original_price=599.99,
                url="https://example.com/smartphone",
                site="amazon",
                category="Électronique",
                timestamp=datetime.now()
            ),
            Product(
                name="TV 4K",
                price=499.99,
                original_price=999.99,
                url="https://example.com/tv",
                site="amazon",
                category="Électronique",
                timestamp=datetime.now()
            ),
            Product(
                name="Casque Audio",
                price=29.99,
                original_price=149.99,
                url="https://example.com/casque",
                site="amazon",
                category="Électronique",
                timestamp=datetime.now()
            )
        ]

    def test_analyze_prices(self):
        """Teste la détection d'anomalies de prix."""
        alerts = self.analyzer.analyze_prices(self.sample_products)
        self.assertIsInstance(alerts, list)
        
        # Vérifie qu'au moins une alerte est générée pour le casque audio
        # qui a une réduction de 80%
        casque_alerts = [alert for alert in alerts 
                        if "Casque Audio" in alert.product.name]
        self.assertTrue(len(casque_alerts) > 0)
        
        if casque_alerts:
            alert = casque_alerts[0]
            self.assertIsInstance(alert, PriceAlert)
            self.assertEqual(alert.alert_type, 'price_drop')
            self.assertGreater(alert.confidence, 0.5)

    def test_category_stats(self):
        """Teste le calcul des statistiques par catégorie."""
        self.analyzer._update_category_stats(self.sample_products)
        stats = self.analyzer.category_stats.get('Électronique')
        
        self.assertIsNotNone(stats)
        self.assertIn('mean', stats)
        self.assertIn('std', stats)
        self.assertIn('median', stats)
        self.assertIn('q1', stats)
        self.assertIn('q3', stats)

    def test_price_drop_detection(self):
        """Teste la détection des baisses de prix significatives."""
        product = Product(
            name="Test Product",
            price=100.0,
            original_price=300.0,  # 66% de réduction
            url="https://example.com/test",
            site="amazon",
            category="Test",
            timestamp=datetime.now()
        )
        
        alert = self.analyzer._analyze_product(product)
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert.alert_type, 'price_drop')
        self.assertGreater(alert.confidence, 0.6)
        self.assertEqual(alert.price_difference, 200.0)

    def test_low_price_detection(self):
        """Teste la détection des prix anormalement bas."""
        # Crée un ensemble de produits avec des prix normaux
        normal_products = [
            Product(
                name=f"Product {i}",
                price=100.0 + i * 10,
                original_price=None,
                url=f"https://example.com/product{i}",
                site="amazon",
                category="Test",
                timestamp=datetime.now()
            ) for i in range(10)
        ]
        
        # Ajoute un produit avec un prix anormalement bas
        anomaly_product = Product(
            name="Anomaly Product",
            price=20.0,  # Prix significativement plus bas
            original_price=None,
            url="https://example.com/anomaly",
            site="amazon",
            category="Test",
            timestamp=datetime.now()
        )
        
        # Met à jour les statistiques avec les produits normaux
        self.analyzer._update_category_stats(normal_products)
        
        # Teste la détection de l'anomalie
        alert = self.analyzer._analyze_product(anomaly_product)
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert.alert_type, 'low_price')
        self.assertGreater(alert.confidence, 0)

if __name__ == '__main__':
    unittest.main()