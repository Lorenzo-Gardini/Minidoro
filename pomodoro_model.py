from collections import namedtuple
from enum import Enum

class PomodoroStates(Enum):
    IDLE = 0
    STUDYING = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3
    PAUSE = 4
    END = 5


PomodoroData = namedtuple(
    'PomodoroData',
    [
        'current_total_study_time',
        'current_study_time',
        'current_break_time',
        'breaks_done',
        'pomodoro_state'
    ]
)

PomodoroConfig = namedtuple('PomodoroConfig', [
    'total_study_time',
    'study_time',
    'short_break_time',
    'long_break_time',
    'long_break_interval'
])

class PomodoroTimer:

    def __init__(self,
                 total_study_time,
                 study_time=30,
                 short_break_time=5,
                 long_break_time=15,
                 long_break_interval=4):
        self._total_study_time = total_study_time * 60
        self._short_break_time = short_break_time * 60
        self._long_break_time = long_break_time * 60
        self._study_time = study_time * 60
        self._long_break_interval = long_break_interval
        self._current_total_study_time = 0
        self._current_study_time = 0
        self._current_break_time = 0
        self._breaks_done = 0
        self._pomodoro_state = PomodoroStates.IDLE

    @property
    def config(self):
        return PomodoroConfig(
            self._total_study_time,
            self._study_time,
            self._short_break_time,
            self._long_break_time,
            self._long_break_interval
        )

    def idle(self):
        if self._pomodoro_state not in {PomodoroStates.PAUSE, PomodoroStates.END}:
            self._pomodoro_state = PomodoroStates.IDLE
            self._reset_timers()

    def study(self):
        if self._pomodoro_state != PomodoroStates.END:
            self._pomodoro_state = PomodoroStates.STUDYING
            self._reset_timers()

    def pause(self):
        if self._pomodoro_state == PomodoroStates.STUDYING:
            self._pomodoro_state = PomodoroStates.PAUSE

    def resume(self):
        if self._pomodoro_state == PomodoroStates.PAUSE:
            self._pomodoro_state = PomodoroStates.STUDYING

    def take_break(self):
        if self._pomodoro_state in {PomodoroStates.STUDYING, PomodoroStates.PAUSE}:
            self._breaks_done += 1
            if self._breaks_done % self._long_break_interval == 0:
                self._pomodoro_state = PomodoroStates.LONG_BREAK
            else:
                self._pomodoro_state = PomodoroStates.SHORT_BREAK
            self._reset_timers()

    def end_of_study(self):
        self._pomodoro_state = PomodoroStates.END
        self._reset_timers()

    @property
    def data(self):
        return PomodoroData(
            self._current_total_study_time,
            self._current_study_time,
            self._current_break_time,
            self._breaks_done,
            self._pomodoro_state
        )

    def update(self):
        if self._pomodoro_state == PomodoroStates.STUDYING:

            if self._current_total_study_time >= self._total_study_time:
                self.end_of_study()

            self._current_study_time += 1
            self. _current_total_study_time += 1

        elif self._pomodoro_state in {PomodoroStates.LONG_BREAK, PomodoroStates.SHORT_BREAK}:
            self._current_break_time += 1

    def _reset_timers(self):
        self._current_break_time = 0
        self._current_study_time = 0