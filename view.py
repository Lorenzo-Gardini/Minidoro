import tkinter as tk
from enum import Enum
from pomodoro_model import PomodoroStates

class PomodoroCommands(Enum):
    STUDY = 1
    PAUSE = 2
    RESUME = 3
    BREAK = 4

class PomodoroView:
    def __init__(self, play_action, break_action):
        self._root = tk.Tk()
        self._root.title("Pomodoro Timer")
        self._root.geometry("300x200")

        self._timer = tk.Label(self._root, height=2, width=40)
        self._state = tk.Label(self._root, height=2, width=40)
        self._total_time_remaning = tk.Label(self._root, height=2, width=40)
        self._play_button = tk.Button(self._root, width=15)
        self._play_button.config(command=lambda: play_action(PomodoroCommands[self._play_button.cget('text').upper()]))
        break_button = tk.Button(self._root, text="Break", width=15, command=break_action)

        self._play_button.pack(pady=10)
        break_button.pack(pady=10)
        self._state.pack()
        self._timer.pack()
        self._total_time_remaning.pack()
        self.change_timer_label(0)

    def show(self):
        self._root.mainloop()

    def _change_play_button(self, text):
        self._play_button.config(text=text)

    def change_state_label(self, state):
        self._state.config(text=state.name.replace('_', ' ').capitalize())
        if state == PomodoroStates.PAUSE:
            self._change_play_button('Resume')
        elif state == PomodoroStates.STUDYING:
            self._change_play_button('Pause')
        else:
            self._change_play_button('Study')


    def change_timer_label(self, seconds):
        self._timer.config(text=PomodoroView._seconds_to_hms_text(seconds))

    def chage_total_time_remaning_label(self, seconds):
        self._total_time_remaning.config(text=f'Total study time:\n{PomodoroView._seconds_to_hms_text(seconds)}')

    def close(self):
        self._root.quit()
        self._root.destroy()

    @staticmethod
    def _seconds_to_hms_text(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"