[![GitHub version](https://badge.fury.io/gh/Lorenzo-Gardini%2FMinidoro.svg)](https://github.com/Lorenzo-Gardini/Minidoro)
[![python versions](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# Minidoro

Simple Pomodoro timer with a minimalistic design. The code implements patter MVC and is well engineered. 

The project is managed using `uv`.

For any bug, features or improvements, please open an issue or a pull request.

If you want to run the app, change default settings in `configurations.config.yaml` file and run the `main.py`.

## Parameters
Parameters are:
```yaml
stop_on_timeout: false # if true, stops the timer once study_time is reached
stop_on_end: true # if true, stops the timer once total_study_time is reached
total_study_time: 240 # total time in minutes
study_time: 30 # time in minutes of one study session
short_break_time: 5 # time in minutes of one short break
long_break_time: 10 # time in minutes of one long break
long_break_interval: 4 # number of study sessions before a long break
```



