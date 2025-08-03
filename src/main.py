import streamlit as st
from scraper.scraper import Scraper
from analyzer.price_analyzer import PriceAnalyzer
from notifier.notification_manager import NotificationManager
from database.db_manager import DatabaseManager

def main():
    st.set_page_config(
        page_title="Détecteur d'Erreurs de Prix",
        page_icon="💰",
        layout="wide"
    )

    st.title("Détecteur d'Erreurs de Prix 💰")

    # Sidebar pour les filtres
    with st.sidebar:
        st.header("Filtres")
        min_price = st.number_input("Prix minimum", value=0.0)
        max_price = st.number_input("Prix maximum", value=1000.0)
        category = st.selectbox(
            "Catégorie",
            ["Toutes", "Électronique", "Mode", "Maison", "Sports"]
        )

    # Interface principale
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dernières Alertes")
        # TODO: Implémenter l'affichage des alertes

    with col2:
        st.subheader("Statistiques")
        # TODO: Implémenter les statistiques

    # Section des produits détectés
    st.header("Produits Détectés")
    # TODO: Implémenter l'affichage des produits

if __name__ == "__main__":
    main()