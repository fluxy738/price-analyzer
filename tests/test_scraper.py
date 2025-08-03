import unittest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from src.scraper.scraper import Scraper, Product

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()
        self.sample_html = """
        <div class="s-result-item">
            <h2 class="a-text-normal">Test Product</h2>
            <span class="a-price-whole">99</span>
            <span class="a-text-price">199.99</span>
            <a href="/product/123">Link</a>
        </div>
        <div class="s-result-item">
            <h2 class="a-text-normal">Another Product</h2>
            <span class="a-price-whole">149</span>
            <span class="a-text-price">299.99</span>
            <a href="/product/456">Link</a>
        </div>
        """

    @patch('httpx.AsyncClient')
    async def test_scrape_site(self, mock_client):
        """Teste le scraping d'un site."""
        # Configure le mock
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        # Exécute le scraping
        products = await self.scraper.scrape_site('amazon', 'test')

        # Vérifie les résultats
        self.assertEqual(len(products), 2)
        self.assertIsInstance(products[0], Product)
        self.assertEqual(products[0].name, 'Test Product')
        self.assertEqual(products[0].price, 99.0)
        self.assertEqual(products[0].original_price, 199.99)

    def test_parse_products(self):
        """Teste le parsing des produits depuis le HTML."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.sample_html, 'html.parser')
        
        products = self.scraper._parse_products(
            soup,
            'amazon',
            self.scraper.sites_config['amazon']
        )

        self.assertEqual(len(products), 2)
        product = products[0]
        
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 99.0)
        self.assertEqual(product.original_price, 199.99)
        self.assertEqual(product.site, 'amazon')
        self.assertTrue(product.url.startswith('https://www.amazon.fr/product/'))

    def test_detect_category(self):
        """Teste la détection de catégorie basée sur le nom du produit."""
        test_cases = [
            ("Smartphone Samsung Galaxy", "Électronique"),
            ("Chaussures de sport Nike", "Mode"),
            ("Table de cuisine", "Maison"),
            ("Vélo de montagne", "Sports"),
            ("Produit inconnu", "Autre")
        ]

        for product_name, expected_category in test_cases:
            category = self.scraper._detect_category(product_name)
            self.assertEqual(
                category,
                expected_category,
                f"Erreur pour {product_name}: attendu {expected_category}, obtenu {category}"
            )

    @patch('httpx.AsyncClient')
    async def test_error_handling(self, mock_client):
        """Teste la gestion des erreurs lors du scraping."""
        # Simule une erreur de connexion
        mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Erreur de connexion")

        # Vérifie que le scraper gère l'erreur gracieusement
        products = await self.scraper.scrape_site('amazon', 'test')
        self.assertEqual(len(products), 0)

    def test_invalid_price_handling(self):
        """Teste la gestion des prix invalides."""
        from bs4 import BeautifulSoup
        
        # HTML avec un prix invalide
        invalid_html = """
        <div class="s-result-item">
            <h2 class="a-text-normal">Test Product</h2>
            <span class="a-price-whole">Invalid</span>
            <a href="/product/123">Link</a>
        </div>
        """
        
        soup = BeautifulSoup(invalid_html, 'html.parser')
        products = self.scraper._parse_products(
            soup,
            'amazon',
            self.scraper.sites_config['amazon']
        )

        # Vérifie que le produit avec prix invalide est ignoré
        self.assertEqual(len(products), 0)

if __name__ == '__main__':
    unittest.main()