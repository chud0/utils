import logging

# создание логгера с именем "main" (может быть любым)
logger = logging.getLogger('main')
# установка уровня логирования
logger.setLevel(logging.DEBUG)

# создание обработчика с логированием в консоль
ch = logging.StreamHandler()
# установка уровня логирования конкретно этого обработчика
ch.setLevel(logging.DEBUG)
# создание обработчика с логированием в файл "2_example.log"
file_handler = logging.FileHandler("3_example.log", mode="a")
file_handler.setLevel(logging.WARNING)

# создание шаблона
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# связвание обработчиков с шаблоном форматирования
ch.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(file_handler)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
