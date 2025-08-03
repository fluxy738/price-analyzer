import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
from src.notifier.notification_manager import NotificationManager
from src.analyzer.price_analyzer import PriceAlert
from src.scraper.scraper import Product

class TestNotificationManager(unittest.TestCase):
    def setUp(self):
        self.notifier = NotificationManager()
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

    @patch('smtplib.SMTP')
    async def test_send_email_alert(self, mock_smtp):
        """Teste l'envoi d'alertes par email."""
        # Configure les variables d'environnement pour le test
        with patch.dict('os.environ', {
            'EMAIL_SENDER': 'test@example.com',
            'EMAIL_PASSWORD': 'password123'
        }):
            # Réinitialise le notifier pour prendre en compte les nouvelles variables
            self.notifier = NotificationManager()
            
            # Configure le mock SMTP
            mock_smtp_instance = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

            # Envoie l'alerte
            await self.notifier._send_email_alert(self.sample_alert)

            # Vérifie que l'email a été envoyé correctement
            mock_smtp_instance.starttls.assert_called_once()
            mock_smtp_instance.login.assert_called_once()
            mock_smtp_instance.send_message.assert_called_once()

    @patch('telegram.Bot')
    async def test_send_telegram_alert(self, mock_bot):
        """Teste l'envoi d'alertes via Telegram."""
        # Configure les variables d'environnement pour le test
        with patch.dict('os.environ', {
            'TELEGRAM_TOKEN': 'test_token',
            'TELEGRAM_CHAT_ID': 'test_chat_id'
        }):
            # Réinitialise le notifier
            self.notifier = NotificationManager()
            
            # Configure le mock du bot Telegram
            mock_bot_instance = AsyncMock()
            mock_bot.return_value = mock_bot_instance

            # Envoie l'alerte
            await self.notifier._send_telegram_alert(self.sample_alert)

            # Vérifie que le message a été envoyé
            mock_bot_instance.send_message.assert_called_once()
            args, kwargs = mock_bot_instance.send_message.call_args
            self.assertEqual(kwargs['chat_id'], 'test_chat_id')
            self.assertIn(self.sample_product.name, kwargs['text'])

    @patch('aiohttp.ClientSession')
    async def test_send_discord_alert(self, mock_session):
        """Teste l'envoi d'alertes via Discord."""
        # Configure les variables d'environnement pour le test
        with patch.dict('os.environ', {
            'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test'
        }):
            # Réinitialise le notifier
            self.notifier = NotificationManager()
            
            # Configure le mock de la session aiohttp
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance

            # Envoie l'alerte
            await self.notifier._send_discord_alert(self.sample_alert)

            # Vérifie que le webhook a été appelé
            self.assertTrue(mock_session_instance.post.called)

    def test_format_alert_message(self):
        """Teste le formatage des messages d'alerte."""
        message = self.notifier._format_alert_message(self.sample_alert)

        # Vérifie que le message contient toutes les informations importantes
        self.assertIn(self.sample_product.name, message)
        self.assertIn(str(self.sample_product.price), message)
        self.assertIn(str(self.sample_product.original_price), message)
        self.assertIn(self.sample_product.site, message)
        self.assertIn(self.sample_product.category, message)
        self.assertIn(str(round(self.sample_alert.confidence * 100, 1)), message)
        self.assertIn(self.sample_alert.alert_type, message)
        self.assertIn(self.sample_product.url, message)

    async def test_send_notifications_all_channels(self):
        """Teste l'envoi d'alertes sur tous les canaux configurés."""
        with patch.multiple(self.notifier,
                          _send_email_alert=AsyncMock(),
                          _send_telegram_alert=AsyncMock(),
                          _send_discord_alert=AsyncMock()):
            
            await self.notifier.send_notifications([self.sample_alert])

            # Vérifie que chaque méthode d'envoi a été appelée
            self.notifier._send_email_alert.assert_called_once_with(self.sample_alert)
            self.notifier._send_telegram_alert.assert_called_once_with(self.sample_alert)
            self.notifier._send_discord_alert.assert_called_once_with(self.sample_alert)

if __name__ == '__main__':
    unittest.main()