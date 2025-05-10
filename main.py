from src.controller.pomodoro_controller import PomodoroController
from src.controller.pomodoro_controller_impl import PomodoroControllerImpl

pomodoro_controller: PomodoroController = PomodoroControllerImpl('../configurations/config.yaml')
pomodoro_controller.start()