import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    original_price: Optional[float]
    url: str
    site: str
    category: str
    timestamp: datetime

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.sites_config = {
            'amazon': {
                'base_url': 'https://www.amazon.fr',
                'search_url': 'https://www.amazon.fr/s?k={query}',
                'selectors': {
                    'products': '.s-result-item',
                    'name': '.a-text-normal',
                    'price': '.a-price-whole',
                    'original_price': '.a-text-price'
                }
            },
            # Ajouter d'autres sites ici
        }

    async def scrape_site(self, site: str, query: str) -> List[Product]:
        """Scrape un site spécifique pour les produits."""
        products = []
        config = self.sites_config.get(site)
        if not config:
            return products

        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                url = config['search_url'].format(query=query)
                response = await client.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    products.extend(self._parse_products(soup, site, config))
        except Exception as e:
            print(f"Erreur lors du scraping de {site}: {str(e)}")

        return products

    def _parse_products(self, soup: BeautifulSoup, site: str, config: Dict) -> List[Product]:
        """Parse la page HTML pour extraire les produits."""
        products = []
        selectors = config['selectors']

        for product_elem in soup.select(selectors['products']):
            try:
                name = product_elem.select_one(selectors['name']).text.strip()
                price_elem = product_elem.select_one(selectors['price'])
                if not price_elem:
                    continue

                price = float(price_elem.text.replace(',', '.').replace('€', '').strip())
                original_price = None

                original_price_elem = product_elem.select_one(selectors['original_price'])
                if original_price_elem:
                    try:
                        original_price = float(original_price_elem.text
                            .replace(',', '.')
                            .replace('€', '')
                            .strip())
                    except ValueError:
                        pass

                url = config['base_url'] + product_elem.find('a')['href']
                
                products.append(Product(
                    name=name,
                    price=price,
                    original_price=original_price,
                    url=url,
                    site=site,
                    category=self._detect_category(name),
                    timestamp=datetime.now()
                ))
            except Exception as e:
                print(f"Erreur lors du parsing d'un produit: {str(e)}")
                continue

        return products

    def _detect_category(self, product_name: str) -> str:
        """Détecte la catégorie du produit basée sur son nom."""
        # TODO: Implémenter une détection plus sophistiquée
        categories = {
            'Électronique': ['smartphone', 'ordinateur', 'tablette', 'tv', 'console'],
            'Mode': ['chaussures', 'vêtement', 'montre', 'sac'],
            'Maison': ['meuble', 'cuisine', 'déco'],
            'Sports': ['sport', 'fitness', 'vélo']
        }

        product_name = product_name.lower()
        for category, keywords in categories.items():
            if any(keyword in product_name for keyword in keywords):
                return category

        return "Autre"