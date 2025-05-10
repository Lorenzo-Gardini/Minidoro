from notification_manager.windows_notification_manager import WindowsNotificationManager
import platform


class NotificationManagerFactory:
    @staticmethod
    def create_notification_manager():
        """
        Factory method to create a notification manager instance.
        Currently, it only supports WindowsNotificationManager.
        """
        return WindowsNotificationManager() if platform.system() == "Windows" else None