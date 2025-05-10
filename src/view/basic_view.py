import tkinter as tk
from typing import Callable

from src.model.pomodoro_model import PomodoroState
from src.view.view import PomodoroView
from src.view.view import PomodoroCommand

class BasicView(PomodoroView):
    """
    A basic implementation of the Pomodoro timer view using Tkinter.

    This class extends :class:`PomodoroView` and provides a graphical user
    interface (GUI) to interact with the Pomodoro timer. The view includes
    buttons for controlling the timer and displaying the state, time remaining,
    and total study time.
    """
    def __init__(self, play_action: Callable[[PomodoroCommand], None], break_action: Callable[[], None]) -> None:
        """
        Initializes the BasicView with the given actions for play and break.

        :param play_action: The function to be called when the play button is clicked.
                             It will receive a :class:`PomodoroCommand` value indicating the action.
        :type play_action: Callable[[PomodoroCommand], None]
        :param break_action: The function to be called when the break button is clicked.
        :type break_action: Callable[[], None]
        """
        self._root = tk.Tk()
        self._root.title("Minidoro")
        self._root.geometry("300x200")

        self._timer = tk.Label(self._root, height=2, width=40)
        self._state = tk.Label(self._root, height=2, width=40)
        self._total_time_remaning = tk.Label(self._root, height=2, width=40)
        self._play_button = tk.Button(self._root, width=15)
        self._play_button.config(command=lambda: play_action(PomodoroCommand[self._play_button.cget('text').upper()]))
        break_button = tk.Button(self._root, text="Break", width=15, command=break_action)

        self._play_button.pack(pady=10)
        break_button.pack(pady=10)
        self._state.pack()
        self._timer.pack()
        self._total_time_remaning.pack()
        self.change_timer_label(0)

    def show(self) -> None:
        """
        :reference:`show` from :class:`PomodoroView`.
        """
        self._root.mainloop()

    def change_state_label(self, state) -> None:
        """
        :reference:`change_state_label` from :class:`PomodoroView`.
        """
        self._state.config(text=state.name.replace('_', ' ').capitalize())
        if state == PomodoroState.PAUSE:
            self._change_play_button('Resume')
        elif state == PomodoroState.STUDYING:
            self._change_play_button('Pause')
        else:
            self._change_play_button('Study')

    def chage_total_time_remaning_label(self, seconds) -> None:
        """
        :reference:`chage_total_time_remaning_label` from :class:`PomodoroView`.
        """
        self._total_time_remaning.config(text=f'Total study time:\n{BasicView._seconds_to_hms_text(seconds)}')

    def change_timer_label(self, seconds) -> None:
        """
        :reference:`change_timer_label` from :class:`PomodoroView`.
        """
        self._timer.config(text=BasicView._seconds_to_hms_text(seconds))

    def close(self) -> None:
        """
        Close the Tkinter window and destroy the application.

        This method stops the Tkinter main loop and closes the window.
        """
        self._root.quit()
        self._root.destroy()

    @staticmethod
    def _seconds_to_hms_text(seconds: int) -> str:
        """ Converts seconds to a string in HH:MM:SS or MM:SS format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    def _change_play_button(self, text) -> None:
        """ Change the text of the play button."""
        self._play_button.config(text=text)