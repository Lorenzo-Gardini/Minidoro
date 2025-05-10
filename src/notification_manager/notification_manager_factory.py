from src.notification_manager.notification_manager_interface import NotificationManager
from src.notification_manager.windows_notification_manager import WindowsNotificationManager
import platform

class _DummyNotificationManager(NotificationManager):
    """
    Dummy implementation of :class:`~src.notification_manager.notification_manager_interface.NotificationManager`
    for non-Windows platforms.

    This class implements all methods of the :class:`NotificationManager` interface,
    but performs no actions. It is used as a safe fallback when desktop notifications
    are not supported on the current system.
    """

    def time_to_break(self):
        """
        Do nothing.

        Called when it's time for a break. Implements
        :meth:`~src.notification_manager.notification_manager_interface.NotificationManager.time_to_break`.
        """
        pass

    def time_to_study(self):
        """
        Do nothing.

        Called when it's time to study. Implements
        :meth:`~src.notification_manager.notification_manager_interface.NotificationManager.time_to_study`.
        """
        pass

    def study_is_over(self):
        """
        Do nothing.

        Called when the study session is over. Implements
        :meth:`~src.notification_manager.notification_manager_interface.NotificationManager.study_is_over`.
        """
        pass


class NotificationManagerFactory:
    @staticmethod
    def create_notification_manager() -> NotificationManager:
        """
        Factory method to create a :class:`~src.notification_manager.notification_manager_interface.NotificationManager` instance.

        :returns: An instance of :class:`~src.notification_manager.windows_notification_manager.WindowsNotificationManager` if the platform is Windows, otherwise an instance of :class:`_DummyNotificationManager` which performs no actions.
        :rtype: :class:`NotificationManager`
        """
        return WindowsNotificationManager() if platform.system() == "Windows" else _DummyNotificationManager()

