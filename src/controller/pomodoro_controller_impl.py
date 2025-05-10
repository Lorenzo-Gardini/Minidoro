import threading
from collections import deque
from time import sleep

import yaml

from src.controller.pomodoro_controller import PomodoroController
from src.model.pomodoro_model import PomodoroState
from src.model.pomodoro_model_impl import PomodoroTimerImpl
from src.notification_manager.notification_manager_factory import NotificationManagerFactory
from src.view.basic_view import BasicView
from src.view.view import PomodoroCommand


class PomodoroControllerImpl(PomodoroController):
    def __init__(self, config_path: str) -> None:
        """
        Initializes the object with the provided configuration file path.

        :param config_path: The path to the configuration file.
        :type config_path: str

        :returns: None
        """
        self._opts = deque()
        self._pomodoro_timer = PomodoroTimerImpl(**PomodoroControllerImpl._read_config(config_path))
        self._notification_manager = NotificationManagerFactory.create_notification_manager()
        self._view = BasicView(play_action=lambda pomodoro_command: self._opts.append(pomodoro_command),
                               break_action=lambda: self._opts.append(PomodoroCommand.BREAK))

    def start(self):
        """
        :reference:`start` from :class:`PomodoroController`.
        """
        threading.Thread(target=self._main_loop, daemon=True).start()
        self._view.show()

    @staticmethod
    def _read_config(config_path) -> dict:
        """Reads the configuration file and returns the configuration as a dictionary."""
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def _main_loop(self) -> None:
        """Loop that runs the pomodoro timer and updates the view."""
        pomodoro_config = self._pomodoro_timer.config
        while True:
            command = self._opts.popleft() if len(self._opts) else None
            if command == PomodoroCommand.STUDY:
                self._pomodoro_timer.study()
            elif command == PomodoroCommand.PAUSE:
                self._pomodoro_timer.pause()
            elif command == PomodoroCommand.RESUME:
                self._pomodoro_timer.resume()
            elif command == PomodoroCommand.BREAK:
                self._pomodoro_timer.take_break()
            else:
                self._pomodoro_timer.update()

            pomodoro_data = self._pomodoro_timer.data
            self._view.change_state_label(pomodoro_data.pomodoro_state)
            self._view.chage_total_time_remaning_label(pomodoro_data.current_total_study_time)

            if pomodoro_data.pomodoro_state == PomodoroState.STUDYING:
                self._view.change_timer_label(pomodoro_data.current_study_time)
            elif pomodoro_data.pomodoro_state in {PomodoroState.SHORT_BREAK, PomodoroState.LONG_BREAK}:
                self._view.change_timer_label(pomodoro_data.current_break_time)

            if pomodoro_data.pomodoro_state == PomodoroState.END:
                self._notification_manager.study_is_over()
                break

            if pomodoro_data.pomodoro_state in {PomodoroState.SHORT_BREAK, PomodoroState.LONG_BREAK}:
                if (pomodoro_data.pomodoro_state == PomodoroState.LONG_BREAK and pomodoro_data.current_break_time == pomodoro_config.long_break_time) or \
                   (pomodoro_data.pomodoro_state == PomodoroState.SHORT_BREAK and pomodoro_data.current_break_time == pomodoro_config.short_break_time):
                    self._notification_manager.time_to_study()
                    self._pomodoro_timer.idle()

            if pomodoro_data.pomodoro_state == PomodoroState.STUDYING and pomodoro_data.current_study_time == pomodoro_config.study_time:
                self._notification_manager.time_to_break()

            sleep(1)