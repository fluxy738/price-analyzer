import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from analyzer.price_analyzer import PriceAlert

class NotificationManager:
    def __init__(self):
        load_dotenv()
        
        # Configuration email
        self.email_sender = os.getenv('EMAIL_SENDER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))

        # Configuration Telegram
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

        # Configuration Discord
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    async def send_notifications(self, alerts: List[PriceAlert]) -> None:
        """Envoie les notifications pour toutes les alertes."""
        for alert in alerts:
            await self._send_email_alert(alert)
            await self._send_telegram_alert(alert)
            await self._send_discord_alert(alert)

    async def _send_email_alert(self, alert: PriceAlert) -> None:
        """Envoie une alerte par email."""
        if not all([self.email_sender, self.email_password]):
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_sender  # Pour le MVP, on envoie à l'expéditeur
            msg['Subject'] = f"Alerte Prix - {alert.product.name}"

            body = self._format_alert_message(alert)
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)

        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {str(e)}")

    async def _send_telegram_alert(self, alert: PriceAlert) -> None:
        """Envoie une alerte via Telegram."""
        if not all([self.telegram_token, self.telegram_chat_id]):
            return

        try:
            bot = Bot(token=self.telegram_token)
            message = self._format_alert_message(alert)
            await bot.send_message(
                chat_id=self.telegram_chat_id,
                text=message,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Erreur lors de l'envoi sur Telegram: {str(e)}")

    async def _send_discord_alert(self, alert: PriceAlert) -> None:
        """Envoie une alerte via Discord."""
        if not self.discord_webhook_url:
            return

        try:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    self.discord_webhook_url,
                    adapter=AsyncWebhookAdapter(session)
                )
                message = self._format_alert_message(alert)
                await webhook.send(content=message)
        except Exception as e:
            print(f"Erreur lors de l'envoi sur Discord: {str(e)}")

    def _format_alert_message(self, alert: PriceAlert) -> str:
        """Formate le message d'alerte."""
        message = f"🔔 Alerte Prix Détectée!\n\n"
        message += f"Produit: {alert.product.name}\n"
        message += f"Prix actuel: {alert.product.price}€\n"
        
        if alert.product.original_price:
            message += f"Prix original: {alert.product.original_price}€\n"
            message += f"Économie: {alert.price_difference:.2f}€ "
            message += f"({(alert.price_difference/alert.product.original_price*100):.1f}%)\n"

        message += f"Site: {alert.product.site}\n"
        message += f"Catégorie: {alert.product.category}\n"
        message += f"Confiance: {alert.confidence*100:.1f}%\n"
        message += f"Type d'alerte: {alert.alert_type}\n"
        message += f"Lien: {alert.product.url}\n"
        message += f"\nDétecté le {alert.timestamp.strftime('%d/%m/%Y à %H:%M')}\n"

        return message