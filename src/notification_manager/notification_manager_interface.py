from abc import ABC, abstractmethod


class NotificationManager(ABC):

    @abstractmethod
    def time_to_break(self):
        """
        Notify the user that it's time to take a break.
        """
        pass

    @abstractmethod
    def time_to_study(self):
        """
        Notify the user that it's time to study.
        """
        pass

    @abstractmethod
    def study_is_over(self):
        """
        Notify the user that the study session is over.
        """
        pass