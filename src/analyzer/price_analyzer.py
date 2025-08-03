from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from sklearn.ensemble import IsolationForest
import numpy as np
from scraper.scraper import Product

@dataclass
class PriceAlert:
    product: Product
    confidence: float
    price_difference: float
    timestamp: datetime
    alert_type: str  # 'low_price' ou 'price_drop'

class PriceAnalyzer:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.price_history: Dict[str, List[float]] = {}
        self.category_stats: Dict[str, Dict[str, float]] = {}

    def analyze_prices(self, products: List[Product]) -> List[PriceAlert]:
        """Analyse les prix des produits pour détecter les anomalies."""
        alerts = []

        # Mise à jour des statistiques par catégorie
        self._update_category_stats(products)

        # Analyse individuelle des produits
        for product in products:
            alert = self._analyze_product(product)
            if alert:
                alerts.append(alert)

        return alerts

    def _update_category_stats(self, products: List[Product]) -> None:
        """Met à jour les statistiques de prix par catégorie."""
        category_prices: Dict[str, List[float]] = {}

        # Collecte des prix par catégorie
        for product in products:
            if product.category not in category_prices:
                category_prices[product.category] = []
            category_prices[product.category].append(product.price)

        # Calcul des statistiques
        for category, prices in category_prices.items():
            if len(prices) > 1:  # Vérifie qu'il y a assez de données
                self.category_stats[category] = {
                    'mean': np.mean(prices),
                    'std': np.std(prices),
                    'median': np.median(prices),
                    'q1': np.percentile(prices, 25),
                    'q3': np.percentile(prices, 75)
                }

    def _analyze_product(self, product: Product) -> Optional[PriceAlert]:
        """Analyse un produit individuel pour détecter les anomalies de prix."""
        if product.category not in self.category_stats:
            return None

        stats = self.category_stats[product.category]
        price = product.price

        # Calcul du score d'anomalie
        z_score = (price - stats['mean']) / stats['std'] if stats['std'] > 0 else 0
        iqr = stats['q3'] - stats['q1']
        price_difference = 0

        # Détection des prix anormalement bas
        if price < stats['q1'] - 1.5 * iqr:
            confidence = min(abs(z_score) / 3, 1.0)  # Normalisation de la confiance
            price_difference = stats['median'] - price
            
            return PriceAlert(
                product=product,
                confidence=confidence,
                price_difference=price_difference,
                timestamp=datetime.now(),
                alert_type='low_price'
            )

        # Détection des baisses de prix significatives
        if product.original_price and product.original_price > 0:
            price_drop_ratio = (product.original_price - price) / product.original_price
            if price_drop_ratio > 0.5:  # Baisse de plus de 50%
                confidence = min(price_drop_ratio, 1.0)
                price_difference = product.original_price - price
                
                return PriceAlert(
                    product=product,
                    confidence=confidence,
                    price_difference=price_difference,
                    timestamp=datetime.now(),
                    alert_type='price_drop'
                )

        return None

    def _is_price_history_anomaly(self, product_id: str, price: float) -> bool:
        """Vérifie si le prix est une anomalie basée sur l'historique."""
        if product_id not in self.price_history or len(self.price_history[product_id]) < 5:
            return False

        # Utilisation de Isolation Forest pour la détection d'anomalies
        prices = np.array(self.price_history[product_id]).reshape(-1, 1)
        self.model.fit(prices)
        prediction = self.model.predict([[price]])
        return prediction[0] == -1  # -1 indique une anomalie