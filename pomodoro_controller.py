import threading
from collections import deque
from time import sleep

import yaml

from notification_manager.notification_manager_factory import NotificationManagerFactory
from notification_manager.windows_notification_manager import WindowsNotificationManager
from pomodoro_model import PomodoroTimer, PomodoroStates
from view import PomodoroView, PomodoroCommands


class PomodoroController:
    def __init__(self, config_path):
        self._opts = deque()
        self._pomodoro_timer = PomodoroTimer(**PomodoroController._read_config(config_path))
        self._notification_manager = NotificationManagerFactory.create_notification_manager()
        self._view = PomodoroView(play_action=lambda pomodoro_command: self._opts.append(pomodoro_command),
                                  break_action=lambda: self._opts.append(PomodoroCommands.BREAK))

    @staticmethod
    def _read_config(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def start(self):
        threading.Thread(target=self._main, daemon=True).start()
        self._view.show()

    def _main(self):
        pomodoro_config = self._pomodoro_timer.config
        while True:
            command = self._opts.popleft() if len(self._opts) else None
            if command == PomodoroCommands.STUDY:
                self._pomodoro_timer.study()
            elif command == PomodoroCommands.PAUSE:
                self._pomodoro_timer.pause()
            elif command == PomodoroCommands.RESUME:
                self._pomodoro_timer.resume()
            elif command == PomodoroCommands.BREAK:
                self._pomodoro_timer.take_break()
            else:
                self._pomodoro_timer.update()

            pomodoro_data = self._pomodoro_timer.data
            self._view.change_state_label(pomodoro_data.pomodoro_state)
            self._view.chage_total_time_remaning_label(pomodoro_data.current_total_study_time)

            if pomodoro_data.pomodoro_state == PomodoroStates.STUDYING:
                self._view.change_timer_label(pomodoro_data.current_study_time)
            elif pomodoro_data.pomodoro_state in {PomodoroStates.SHORT_BREAK, PomodoroStates.LONG_BREAK}:
                self._view.change_timer_label(pomodoro_data.current_break_time)

            if pomodoro_data.pomodoro_state == PomodoroStates.END:
                self._notification_manager.study_is_over()
                break


            if pomodoro_data.pomodoro_state in {PomodoroStates.SHORT_BREAK, PomodoroStates.LONG_BREAK}:
                if (pomodoro_data.pomodoro_state == PomodoroStates.LONG_BREAK and pomodoro_data.current_break_time == pomodoro_config.long_break_time) or \
                   (pomodoro_data.pomodoro_state == PomodoroStates.SHORT_BREAK and pomodoro_data.current_break_time == pomodoro_config.short_break_time):
                    self._notification_manager.time_to_study()
                    self._pomodoro_timer.idle()

            if pomodoro_data.pomodoro_state == PomodoroStates.STUDYING and pomodoro_data.current_study_time == pomodoro_config.study_time:
                self._notification_manager.time_to_break()

            sleep(1)