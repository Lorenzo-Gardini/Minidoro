from enum import Enum
from src.model.pomodoro_model import PomodoroState

class PomodoroCommand(Enum):
    """
    Enumeration of commands for controlling a Pomodoro timer.

    This enum defines the set of commands that can be issued to the Pomodoro timer logic.

    Members
    -------
    STUDY : int
        Start a study session.
    PAUSE : int
        Pause the current timer.
    RESUME : int
        Resume a paused timer.
    BREAK : int
        Start a break session.
    """

    STUDY = 1
    """Start a study session."""

    PAUSE = 2
    """Pause the current timer."""

    RESUME = 3
    """Resume a paused timer."""

    BREAK = 4
    """Start a break session."""



class PomodoroView:
    """
    Interface for the Pomodoro timer view.

    This class defines the contract for any GUI or UI component that displays the state
    of a Pomodoro timer. It contains methods to update UI elements such as labels and timers,
    and to control the visibility of the view.

    Methods
    -------
    show() -> None
        Displays the view to the user.

    change_state_label(state: int) -> None
        Updates the label indicating the current state of the timer (e.g., work, break).

    change_timer_label(seconds: int) -> None
        Updates the main timer display with the remaining time in seconds.

    chage_total_time_remaning_label(seconds: int) -> None
        Updates the display showing total remaining Pomodoro session time in seconds.

    close() -> None
        Closes or hides the view.
    """

    def show(self) -> None:
        """
        Display the view to the user.
        """
        pass

    def change_state_label(self, state: PomodoroState) -> None:
        """
        Change the label to reflect the current Pomodoro state.

        :param state: Enumeration value indicating the current state of the Pomodoro timer.
        :type state: PomodoroState
        """
        pass

    def change_timer_label(self, seconds: int) -> None:
        """
        Update the timer label with the remaining time.

        :param seconds: The number of seconds remaining in the current Pomodoro session.
        :type seconds: int
        """
        pass

    def chage_total_time_remaning_label(self, seconds: int) -> None:
        """
        Update the total time remaining label.

        :param seconds: Total remaining time in seconds for the Pomodoro cycle.
        :type seconds: int
        """
        pass

    def close(self) -> None:
        """
        Close the view or remove it from display.
        """
        pass
