from collections import namedtuple
from enum import Enum

from src.model.pomodoro_model import PomodoroConfig, PomodoroState, PomodoroData, PomodoroTimer


class PomodoroTimerImpl(PomodoroTimer):

    def __init__(self,
                 total_study_time: int,
                 study_time: int = 30,
                 short_break_time: int = 5,
                 long_break_time: int = 15,
                 long_break_interval: int = 4,
                 stop_on_timeout: bool = False,
                 stop_on_end: bool = False) -> None:
        """
        Initializes the Pomodoro timer with the given configuration.

        :param total_study_time: Total study time in minutes.
        :type total_study_time: int

        :param study_time: Study session time in minutes (default is 30 minutes).
        :type study_time: int

        :param short_break_time: Short break time in minutes (default is 5 minutes).
        :type short_break_time: int

        :param long_break_time: Long break time in minutes (default is 15 minutes).
        :type long_break_time: int

        :param long_break_interval: The interval after which a long break occurs (default is every 4 cycles).
        :type long_break_interval: int

        :param stop_on_timeout: Flag to stop the timer when the study time is completed (default is False).
        :type stop_on_timeout: bool

        :param stop_on_end: Flag to stop the timer when the total study time is completed (default is False).
        :type stop_on_end: bool

        """
        self._total_study_time = total_study_time * 60
        self._short_break_time = short_break_time * 60
        self._long_break_time = long_break_time * 60
        self._study_time = study_time * 60
        self._long_break_interval = long_break_interval
        self._stop_on_timeout = stop_on_timeout
        self._stop_on_end = stop_on_end
        self._current_total_study_time = 0
        self._current_study_time = 0
        self._current_break_time = 0
        self._breaks_done = 0
        self._pomodoro_state = PomodoroState.IDLE

    def idle(self) -> None:
        """
        :reference:`idle` from :class:`PomodoroTimer`.
        """
        if self._pomodoro_state not in {PomodoroState.PAUSE, PomodoroState.END}:
            self._pomodoro_state = PomodoroState.IDLE
            self._reset_timers()

    def study(self) -> None:
        """
        :reference:`study` from :class:`PomodoroTimer`.
        """
        if self._pomodoro_state != PomodoroState.END:
            self._pomodoro_state = PomodoroState.STUDYING
            self._reset_timers()

    def pause(self) -> None:
        """
        :reference:`pause` from :class:`PomodoroTimer`.
        """
        if self._pomodoro_state == PomodoroState.STUDYING:
            self._pomodoro_state = PomodoroState.PAUSE

    def resume(self) -> None:
        """
        :reference:`resume` from :class:`PomodoroTimer`.
        """
        if self._pomodoro_state == PomodoroState.PAUSE:
            self._pomodoro_state = PomodoroState.STUDYING

    def take_break(self) -> None:
        """
        :reference:`take_break` from :class:`PomodoroTimer`.
        """
        if self._pomodoro_state in {PomodoroState.STUDYING, PomodoroState.PAUSE}:
            self._breaks_done += 1
            if self._breaks_done % self._long_break_interval == 0:
                self._pomodoro_state = PomodoroState.LONG_BREAK
            else:
                self._pomodoro_state = PomodoroState.SHORT_BREAK
            self._reset_timers()

    def end_of_study(self) -> None:
        """
        :reference:`end_of_study` from :class:`PomodoroTimer`.
        """
        self._pomodoro_state = PomodoroState.END
        self._reset_timers()

    def update(self):
        """
        :reference:`update` from :class:`PomodoroTimer`.
        """
        if self._pomodoro_state == PomodoroState.STUDYING:
            if self._current_total_study_time >= self._total_study_time and self._stop_on_end:
                self.end_of_study()

            if self._current_study_time >= self._study_time and self._stop_on_timeout:
                self.idle()
            else:
                self._current_study_time += 1
                self._current_total_study_time += 1

        elif self._pomodoro_state in {PomodoroState.LONG_BREAK, PomodoroState.SHORT_BREAK}:
            self._current_break_time += 1

    @property
    def data(self) -> PomodoroData:
        """
        :reference:`data` from :class:`PomodoroTimer`.
        """
        return PomodoroData(
            self._current_total_study_time,
            self._current_study_time,
            self._current_break_time,
            self._breaks_done,
            self._pomodoro_state
        )

    @property
    def config(self) -> PomodoroConfig:
        """
        :reference:`config` from :class:`PomodoroTimer`.
        """
        return PomodoroConfig(
            self._total_study_time,
            self._study_time,
            self._short_break_time,
            self._long_break_time,
            self._long_break_interval,
            self._stop_on_timeout,
            self._stop_on_end
        )

    def _reset_timers(self):
        """Reset the timers to their initial state."""
        self._current_break_time = 0
        self._current_study_time = 0
