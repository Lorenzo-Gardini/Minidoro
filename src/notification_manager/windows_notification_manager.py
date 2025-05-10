from src.notification_manager.notification_manager_interface import NotificationManager
from winotify import Notification, audio

class WindowsNotificationManager(NotificationManager):
    _APP_ID = "Pomodoro Timer"

    def time_to_break(self):
        notification = Notification(app_id=self._APP_ID,
                     title="Break time!",
                     msg="It's time to take a break to recharge",
                     duration="short")
        notification.set_audio(audio.Reminder, loop=False)
        notification.show()
    def time_to_study(self):
        notification = Notification(app_id=self._APP_ID,
                     title="Study time!",
                     msg="It's time to study hard",
                     duration="short")
        notification.set_audio(audio.LoopingAlarm, loop=True)
        notification.show()

    def study_is_over(self):
        notification = Notification(app_id=self._APP_ID,
                     title="End",
                     msg="Study session is over, good job!",
                     duration="short")
        notification.set_audio(audio.LoopingAlarm2, loop=False)
        notification.show()