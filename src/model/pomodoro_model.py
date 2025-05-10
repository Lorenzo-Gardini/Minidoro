"""
Pomodoro timer core components.

This module defines the core interfaces and data structures used to implement a Pomodoro timer system.
"""

from abc import abstractmethod, ABC
from collections import namedtuple
from enum import Enum


class PomodoroState(Enum):
    """
    Enum representing the various states of the Pomodoro timer.

    Members
    -------
    IDLE : int
        The timer is inactive and waiting to start.
    STUDYING : int
        A study session is currently in progress.
    SHORT_BREAK : int
        A short break is active, usually between study sessions.
    LONG_BREAK : int
        A longer break after several study sessions.
    PAUSE : int
        The timer is paused (either during study or break).
    END : int
        The Pomodoro session has ended.
    """
    IDLE = 0
    STUDYING = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3
    PAUSE = 4
    END = 5



#: Named tuple holding the current runtime data of the Pomodoro timer.
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
"""
PomodoroData(current_total_study_time, current_study_time, current_break_time, breaks_done, pomodoro_state)

Attributes
----------
current_total_study_time : int
    Total accumulated study time in seconds.
current_study_time : int
    Time spent in the current study session.
current_break_time : int
    Time spent in the current break.
breaks_done : int
    Number of breaks taken so far.
pomodoro_state : PomodoroState
    Current state of the Pomodoro timer.
"""

#: Named tuple representing the configuration parameters for the Pomodoro timer.
PomodoroConfig = namedtuple('PomodoroConfig', [
    'total_study_time',
    'study_time',
    'short_break_time',
    'long_break_time',
    'long_break_interval',
    'stop_on_timeout',
    'stop_on_end'
])
"""
PomodoroConfig(total_study_time, study_time, short_break_time, long_break_time, long_break_interval, stop_on_timeout, stop_on_end)

Attributes
----------
total_study_time : int
    The total time to study before stopping or ending.
study_time : int
    Length of a single study session in seconds.
short_break_time : int
    Duration of a short break.
long_break_time : int
    Duration of a long break.
long_break_interval : int
    Number of breaks before a long break occurs.
stop_on_timeout : bool
    Whether the timer should stop after reaching total study time.
stop_on_end : bool
    Whether the timer should stop at the end of a Pomodoro cycle.
"""


class PomodoroTimer(ABC):
    @property
    @abstractmethod
    def config(self) -> PomodoroConfig:
        """
        :reference:`config` from :class:`PomodoroTimer`.

        Return the configuration of the Pomodoro timer.

        :return: The configuration of the Pomodoro timer.
        :rtype: PomodoroConfig
        """
        pass

    @property
    @abstractmethod
    def data(self) -> PomodoroData:
        """
        :reference:`data` from :class:`PomodoroTimer`.

        Return the current data of the Pomodoro timer.

        :return: The current Pomodoro timer data.
        :rtype: PomodoroData
        """
        pass

    def idle(self) -> None:
        """Set the timer to IDLE state."""
        pass

    def study(self) -> None:
        """Start a study session."""
        pass

    def pause(self) -> None:
        """Pause the current session."""
        pass

    def resume(self) -> None:
        """Resume a paused session."""
        pass

    def take_break(self) -> None:
        """Start a break session."""
        pass

    def end_of_study(self) -> None:
        """Mark the study session as complete."""
        pass

    def update(self) -> None:
        """Update the internal timer state."""
        pass
