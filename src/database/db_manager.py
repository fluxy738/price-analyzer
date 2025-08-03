import psycopg2
from psycopg2.extras import DictCursor
from typing import List, Dict, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from scraper.scraper import Product
from analyzer.price_analyzer import PriceAlert

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.conn_params = {
            'dbname': os.getenv('DB_NAME', 'price_analyzer'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self._init_database()

    def _init_database(self) -> None:
        """Initialise la structure de la base de données."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    # Table des produits
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(512) UNIQUE NOT NULL,
                        site VARCHAR(100) NOT NULL,
                        category VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)

                    # Table de l'historique des prix
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS price_history (
                        id SERIAL PRIMARY KEY,
                        product_id INTEGER REFERENCES products(id),
                        price DECIMAL(10,2) NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)

                    # Table des alertes
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        id SERIAL PRIMARY KEY,
                        product_id INTEGER REFERENCES products(id),
                        price DECIMAL(10,2) NOT NULL,
                        original_price DECIMAL(10,2),
                        confidence DECIMAL(5,4) NOT NULL,
                        price_difference DECIMAL(10,2) NOT NULL,
                        alert_type VARCHAR(50) NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
                conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {str(e)}")

    def save_product(self, product: Product) -> Optional[int]:
        """Sauvegarde un produit dans la base de données."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    # Vérifie si le produit existe déjà
                    cur.execute(
                        "SELECT id FROM products WHERE url = %s",
                        (product.url,)
                    )
                    result = cur.fetchone()

                    if result:
                        product_id = result[0]
                    else:
                        # Insère le nouveau produit
                        cur.execute("""
                        INSERT INTO products (name, url, site, category)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """, (product.name, product.url, product.site, product.category))
                        product_id = cur.fetchone()[0]

                    # Enregistre le prix actuel
                    cur.execute("""
                    INSERT INTO price_history (product_id, price)
                    VALUES (%s, %s)
                    """, (product_id, product.price))

                    conn.commit()
                    return product_id

        except Exception as e:
            print(f"Erreur lors de la sauvegarde du produit: {str(e)}")
            return None

    def save_alert(self, alert: PriceAlert) -> None:
        """Sauvegarde une alerte dans la base de données."""
        try:
            product_id = self.save_product(alert.product)
            if not product_id:
                return

            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO alerts (
                        product_id, price, original_price, confidence,
                        price_difference, alert_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        product_id,
                        alert.product.price,
                        alert.product.original_price,
                        alert.confidence,
                        alert.price_difference,
                        alert.alert_type
                    ))
                    conn.commit()

        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'alerte: {str(e)}")

    def get_price_history(self, product_url: str) -> List[Dict]:
        """Récupère l'historique des prix d'un produit."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute("""
                    SELECT ph.price, ph.timestamp
                    FROM price_history ph
                    JOIN products p ON p.id = ph.product_id
                    WHERE p.url = %s
                    ORDER BY ph.timestamp DESC
                    """, (product_url,))
                    return [dict(row) for row in cur.fetchall()]

        except Exception as e:
            print(f"Erreur lors de la récupération de l'historique des prix: {str(e)}")
            return []

    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Récupère les alertes récentes."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute("""
                    SELECT a.*, p.name, p.url, p.site, p.category
                    FROM alerts a
                    JOIN products p ON p.id = a.product_id
                    ORDER BY a.timestamp DESC
                    LIMIT %s
                    """, (limit,))
                    return [dict(row) for row in cur.fetchall()]

        except Exception as e:
            print(f"Erreur lors de la récupération des alertes: {str(e)}")
            return []