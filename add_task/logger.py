import logging

class Logger:
    _instance = None

    def __new__(cls, log_file='log.log', level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.setup(log_file, level)
        return cls._instance

    def setup(self, log_file, level):
        self.logger = logging.getLogger("SingletonLogger")
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # Set UTF-8
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# Usage example
# logger = SingletonLogger('example.log').get_logger()
# logger.info('This is an info message')
