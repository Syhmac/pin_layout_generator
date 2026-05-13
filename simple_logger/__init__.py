from datetime import datetime
import os


class LOG:
    """
    Object for logging messages to a file. Can be used to log debug, info, warn, error and critical messages.
    """
    __file = str # Path to the current log file
    __filepath = str # Path to the directory where the log files are stored
    __level = 0 # Log level. Higher values mean less massages. Can be changes by self.set_level()

    def __init__(self, level: int = 1, filename: str = 'latest.log', filepath: str = 'logs/') -> None:
        """
        Initialize the logger. Run when the class is created.

        If run with level higher than 4, will reset to 0.

        :param level: Log level, 1 (info) by default. Expected values: 0-4
        :param filename: Path to the log file. 'latest.log' by default.
        :param filepath: Path to the directory where the log files are stored. 'logs/' by default.
        Should be ending with /
        :return: None
        """
        if level not in range(0, 5):
            level = 0
        self.__check_directory(filepath)
        self.__filepath = filepath
        self.__file = filepath + filename
        self.__level = level
        with open(self.__file, 'w') as f:
            f.write(self.__get_full_time() + '\n')
            f.close()
        self.debug('Logger initialized')

    @staticmethod
    def __check_directory(path: str) -> None:
        """
        Private method to check if the specified directory exists. If not, creates it.
        :param path: directory path
        :return: None
        """
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def __get_full_time() -> str:
        """
        Private method to get the current time in the format 'YYYY-MM-DD HH:MM:SS.MS'
        :return: string - current time
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    @staticmethod
    def __get_short_time() -> str:
        """
        Private method to get the current time in the format 'HH:MM:SS.MS'
        :return: string - current time
        """
        return datetime.now().strftime('%H:%M:%S.%f')

    def debug(self, message: str) -> None:
        """
        Logs a debug message to the file. Only logs if the level is 0.
        :param message: log message
        :return: None
        """
        if self.__level == 0:
            with open(self.__file, 'a') as f:
                f.write(f'[{self.__get_short_time()}] [DEBUG]:\t{message}\n')
                f.close()

    def info(self, message: str) -> None:
        """
        Logs an info message to the file. Only logs if the level 1 or lower.
        :param message: log message
        :return: None
        """
        if self.__level <= 1:
            with open(self.__file, 'a') as f:
                f.write(f'[{self.__get_short_time()}] [INFO]:\t{message}\n')
                f.close()

    def warn(self, message: str) -> None:
        """
        Logs a warning message to the file. Only logs if the level is 2 or lower.
        :param message: log message
        :return: None
        """
        if self.__level <= 2:
            with open(self.__file, 'a') as f:
                f.write(f'[{self.__get_short_time()}] [WARN]:\t{message}\n')
                f.close()

    def error(self, message: str) -> None:
        """
        Logs an error message to the file. Only logs if the level is 3 or lower.
        :param message: log message
        :return: None
        """
        if self.__level <= 3:
            with open(self.__file, 'a') as f:
                f.write(f'[{self.__get_short_time()}] [ERROR]:\t{message}\n')
                f.close()

    def critical(self, message: str) -> None:
        """
        Logs a critical message to the file. Only logs if the level is 4 or lower.
        :param message: log message
        :return: None
        """
        if self.__level <= 4:
            with open(self.__file, 'a') as f:
                f.write(f'[{self.__get_short_time()}] [CRITICAL]:\t{message}\n')
                f.close()

    def set_level(self, level: int = 1) -> None:
        """
        Changes the log level. If the level is higher than 4, sets it to 0.
        :param level: Log level, 1 (info) by default. Expected values: 0-4
        :return: None
        """
        if level not in range(0, 5):
            level = 0
        self.__level = level
        self.debug(f'Logger level set to {level}')

    def save(self, filename: str = "time") -> None:
        """
        Saves a copy of the current log file in the location specified on the logger initialization.
        :param filename: Name of the file with or without extension. 'time' by default. Set to 'time' to save as the timestamp.
        :return: None
        """
        if filename == 'time':
            file = self.__filepath + datetime.now().strftime('%Y-%m-%d-%H_%M_%S') + '.log'
        else:
            file = self.__filepath + filename

        try:
            with open(file, 'w') as f:
                with open(self.__file, 'r') as r:
                    self.debug('Saving log file')
                    f.write(r.read())
                    r.close()
                f.close()
        except Exception as e:
            self.error(f'Error while saving the log file: {e}')