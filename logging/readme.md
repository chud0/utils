# Модуль logging для Python.
  В Python есть отличная встроенная библиотека - logging. Часто ее противопоставляют print-ам, однако на мой взгляд это гораздо более весомый инструмент. Разобравшись с некотрыми приемами в работе, хочу поделиться с сообществом наиболее, на мой взгляд, интересными вещами. Данная статья основана на [официальной](https://docs.python.org/3/library/logging.html) [документации](https://docs.python.org/3/howto/logging.html), и по сути является частичным вольным переводом.

## Когда использовать logging
Для самого простого использования, модуль предоставляет функции debug(), info(), warning(), error() и critical(). Название функций соответствует названию уровней или серьезности логируемых событий. Рекомендации по использованию стандартных уровней сведены в таблицу (в порядке возрастания серьезности).

Уровень сообщений | Когда использовать
--- | ---
CRITICAL | Критическая ошибка, выполнение программы невозможно
ERROR | Из-за серьезной ошибки программа не смогла выполнить какую-либо функцию
WARNING | Индикация того что произошло что-то неожиданное или указывающее на проблемы в ближайшем будущем, программа все еще работает так как ожидается
INFO | Подтверждения, когда программа работает так ожидается
DEBUG | Вывод детальной информации при поиске проблем в программе

Уровень логирования по умолчанию - `WARNING`, это означает что сообщения этого уровня или выше будут обработаны, ниже - отброшены.

## Simple example. (или В Бой!)
Самый простой пример использования модуля выглядит так:
```
import logging

logging.warning("Warning message")
logging.info("Info message")
```
если запустить скрипт с этим кодом, то в консоли будет выведено:
```
WARNING:root:Warning message
```
 что мы видим: `WARNING` это индикация уровня события, `root` - имя логгера, `Warning message` сообщение. Пока не обращайте внимание на имя логгера, это будет объяснено позже. Строка `logging.info("Info message")` была проигнорирована т.к. уровень `INFO` ниже уровня `WARNING` (который был установлен по умолчанию).

## Немного теории.
Модуль logging имеет модульный подход и предлагает несколько категорий компонентов: логгеры (loggers), обработчики (handlers), фильтры (filters) и объекты форматирования (formatters).
* [logger](https://docs.python.org/3/library/logging.html#logger-objects) содержит интерфейс для логирования. Это основной объект, именно он создает записи в лог.
* [handler](https://docs.python.org/3/library/logging.html#handler-objects) обработчик, который направляет созданные логгером записи в пункт назначения. Например вывод в консоль, запись в файл, отправка письма и т.д.
* [filter](https://docs.python.org/3/library/logging.html#filter-objects) позволяет получить больший контроль над фильтрацией записей чем стандартные уровни логирования.
> Базовый класс реализует только одно поведение: выстраивание иерархии логгеров при помощи имени логгера и точки. Например инициализирован логгер с именем `A.B`, тогда записи логгеров с именами `A.B.C`, `A.B.C.D`, `A.B.D` будут обработаны, а логгеров с именами `A.BB` или `B.B.C` отброшены.

* [formatter](https://docs.python.org/3/library/logging.html#formatter-objects) является шаблоном для форматирования записи. Возможные атрибуты для заполнения шаблона [здесь](https://docs.python.org/3/library/logging.html#logrecord-attributes)

## Способы конфигурации модуля.
### [basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig)
Это базовый, простой способ. Рассмотрим его, на примере чтобы погрузится удивительнйый мир логирования (смайлик):
```
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='example.log',
    filemode='w',
    level=logging.DEBUG,
    )
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```
Рассмотрим параметры переданные в baseConfig: `format` - преобразует вывод логера по переданному шаблону, `filename` - сообщает логгеру что необходимо логи заносить в файл с переданным названием `example.log`, `filemod`: `w` - перезаписывать файл при каждом запуске файла, `a` - дописывать в конец файла и наконец `level` устанавливает уровень логирования `DEBUG`. В результате выполнения будет создан файл `filemod.log` в котором окажутся записи:
```
2018-05-13 23:41:47,769 - root - DEBUG - This message should go to the log file
2018-05-13 23:41:47,769 - root - INFO - So should this
2018-05-13 23:41:47,769 - root - WARNING - And this, too
```
дата и время возможно будут другими. Этот способ конфигурирования на сколько прост, настолько же не понятен и не гибок, предлагаю перейти к следующему способу.
### [getLogger](https://docs.python.org/3/library/logging.html#logger-objects)
Этот способ открывает весь набор инструментов библиотеки. Для использования необходимо создать логгер, создать и добавить обработчики, фильтры и шаблон форматирования. Да, у одного логгера может быть несколько обработчиков. И снова пример:
```
import logging

# создание логгера с именем "main" (может быть любым)
logger = logging.getLogger('main')
# установка уровня логирования
logger.setLevel(logging.DEBUG)

# создание обработчика с логированием в консоль
cons_handler = logging.StreamHandler()
# установка уровня логирования конкретно этого обработчика
cons_handler.setLevel(logging.DEBUG)

# создание обработчика с логированием в файл "2_example.log"
file_handler = logging.FileHandler("3_example.log", mode="a")
file_handler.setLevel(logging.WARNING)

# создание шаблона отображения
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# связвание обработчиков с шаблоном форматирования
cons_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# добавление обработчиков логгеру
logger.addHandler(cons_handler)
logger.addHandler(file_handler)

# использование логгера
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```
По коду должно быть все понятно из комментариев, в результате выполнения получим в консоль:
```
2018-05-15 22:40:07,974 - main - DEBUG - debug message
2018-05-15 22:40:07,974 - main - INFO - info message
2018-05-15 22:40:07,974 - main - WARNING - warn message
2018-05-15 22:40:07,975 - main - ERROR - error message
2018-05-15 22:40:07,975 - main - CRITICAL - critical message
```
и файл с именем `3_example.log` с содержимым:
```
2018-05-15 22:40:07,974 - main - WARNING - warn message
2018-05-15 22:40:07,975 - main - ERROR - error message
2018-05-15 22:40:07,975 - main - CRITICAL - critical message
```
Хочу пояснить следующие моменты:
* Первым делом получаем логгер - экземпляр класса Logger с именем `main`. Причем действует правило: одно имя - один экземпляр. Это означает что при первом вызове метода логгер создается, а при последующих передается уже созданный экземпляр логгера. На практике это означает что достаточно вызвать и настроить логгер в одном месте (модуле), выполнить этот код (импортировать модуль), во всех последующих местах вызывать настроеный логгер и... просто логировать.
* Далее получаем обработчики. Полный список с описанием [здесь](https://docs.python.org/3/library/logging.handlers.html) их много и они разные: вывод в консоль, запись в файл (возможно с ротацией логов), отправка через сокет, http, UDP, отправка письмом, чтение/запись в очередь и т.д. Далее в приимерах будут те что пользовался я сам.
* Нужно четко понимать что у логгера может быть множество обработчиков, каждый обработчик может иметь свой шаблон сообщения, уровень логирования и фильтрацию. Поэтому в консоль попали все сообщения логгера, а в файл с уровнем `WARNING` и выше.
* И наконец получаем шаблоны сообщений. Параметры для шаблонов [здесь](https://docs.python.org/3/library/logging.html?highlight=logging%20formatter#logrecord-attributes), основные параметры далее в примерах примерах.
> Оптимизация. Процесс подстановки аргументов в шаблон ленивый, и произойдет только если запись действительно будет обрабатываться, поэтому в функцию логирования нужно передавать шаблон строки с аргументами, например `logger.debug("received params %s", a)`. Если же передавать заранее сформированную строку, то ресурсы  системы будут потрачены независимо от того будет запись занесена в лог или нет.

> Оптимизация. Вычисление аргуменов для логирования может быть долгим. Для того чтобы не терять время можно воспользоваться методом `isEnabledFor` логгера, который принимает уровень логирования, проверяет будет ли производится запись и возвращает ответ в `True` или `False`. Например:
```
if logger.isEnabledFor(logging.DEBUG):
    logger.debug('Message with %s', expensive_func())
```

### [dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)
Мой любимый способ. Сразу к примеру:
```
import logging
import logging.config

DEBUG = True

LOGGING_CONF = {
    "disable_existing_loggers": True,
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "brief": {
            "format": "%(levelname)-8s %(asctime)s %(name)-16s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "other_cons": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "brief",
        },
    },
    "loggers": {
        "main": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "slave": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["other_cons"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONF)

logger = logging.getLogger("main")
logger.info("loggers %s configured", ", ".join(LOGGING_CONF["loggers"]))
```
Итак почему мне нравится этот способ: есть полный контроль над логгерами как в предыдущем способе, но вся настройка происходит в одном месте и выглядит более наглядно. К тому же объект конфигурации это просто словарь который позволяет использовать всю мощь языка Python, и упростить контроль в процессе разработки (а по моему это очень много).

В примере, переменная DEBUG как раз для такого контроля, эта переменная может импортироваться из настроек проекта и определять поведение целевых логгеров. Это может помочь выводить проект в production - не придется ходить по модулям и править все `DEBUG = True` на `False`.

В словаре-конфигурации, первая строка отключает объявленные ранее логгеры (может применяться например для отключения логгеров сторонних библиотек), вторая указывается только для обратной совместимости (в будущем этот параметр появится) и может быть только `1`. Дальше думаю все понятно: создаются шаблоны, обработчики и объявляются логгеры, к обработчикам добавляются шаблоны, к логгерам обработчики.

Дальше с помощью метода `dictConfig` обрабатывается словарь-конфигурация, затем берется свежесозданный логгер `main` и выводится список имен описанных логгеров. Вывод может быть таким:
```
INFO     2018-05-20 22:43:12 [4_dictConfig.py:45] loggers main, slave configured
```

### [fileConfig](https://docs.python.org/3/library/logging.config.html#configuration-file-format)
Загружает конфигурацию из файла, файл должен быть в формате библиотеки [configparser](https://docs.python.org/3/library/configparser.html). Мехнизм описания конфигурации в файле очень похож на словарь dictConfig -а. Сама конфигурация чуть более многословна, так же предоставляет полный контроль над логгерами.
> По умолчанию disable_existing_loggers = True
> Вместо непосредственно файла может принимать экземпляр класса RawConfigParser, что позволяет хранить конфигурацию проекта в одном файле.

```
import logging
import logging.config

logging.config.fileConfig("5_logging.conf")

logger = logging.getLogger("simpleExample")

logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")
```
```
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
```
и вывод будет:
```
2018-05-20 23:31:29,215 - simpleExample - DEBUG - debug message
2018-05-20 23:31:29,216 - simpleExample - INFO - info message
2018-05-20 23:31:29,216 - simpleExample - WARNING - warn message
2018-05-20 23:31:29,216 - simpleExample - ERROR - error message
2018-05-20 23:31:29,217 - simpleExample - CRITICAL - critical message
```
Код думаю понятен, переходим к седующему способу конфигурации.

### [listen](https://docs.python.org/3/library/logging.config.html#logging.config.listen)
Поднимает сокет, который слушает и загружает конфигурацию. Наверное применяется в больших, распределенных проектах. Я это не использовал поэтому без примеров.

## Некоторые варианты использования
### Наследование
Как я уже упоминал, в логгерах, через имена, реализовано наследование. Рассмотрим пример:
```
import sys
import logging

# этот ужас из-за первой цифры в названии файла
log_dict_conf = __import__("4_dictConfig")
slave = __import__("6_inh_slave")

logger = logging.getLogger("slave." + __name__)
logger.debug("logger with name: %s created", logger.name)


def simple_func(a, b, c):
    s = slave.sum(a, b)
    m = slave.mult(s, c)
    logger.debug("received params %s, %s, %s; return %s", a, b, c, m)
    return m


if __name__ == "__main__":
    args = sys.argv[1:4]
    if len(args) == 3:
        logger.debug("received params from sys.argv")
        args = list(map(int, args))
    else:
        args = [4, 5, 6]
        logger.debug("load default params")
    logger.info("received params %s, %s, %s", *args)
    logger.info(simple_func(*args))
```

```
import logging
logger = logging.getLogger("slave." + __name__)
logger.debug("logger with name: %s created", logger.name)


def sum(a, b):
    s = a + b
    logger.debug("received params %s, %s; sum %s", a, b, s)
    return s


def mult(a, b):
    m = a * b
    logger.debug("received params %s, %s; multiply %s", a, b, m)
    return m
```
выполнив `python 6_inh_main.py 1 2 3` в консоли получим:
```
INFO     2018-05-24 00:54:14 [4_dictConfig.py:45] loggers main, slave configured
DEBUG    2018-05-24 00:54:14,411 slave.6_inh_slave logger with name: slave.6_inh_slave created
DEBUG    2018-05-24 00:54:14,412 slave.__main__   logger with name: slave.__main__ created
DEBUG    2018-05-24 00:54:14,412 slave.__main__   received params from sys.argv
INFO     2018-05-24 00:54:14,412 slave.__main__   received params 1, 2, 3
DEBUG    2018-05-24 00:54:14,412 slave.6_inh_slave received params 1, 2; sum 3
DEBUG    2018-05-24 00:54:14,412 slave.6_inh_slave received params 3, 3; multiply 9
DEBUG    2018-05-24 00:54:14,412 slave.__main__   received params 1, 2, 3; return 9
INFO     2018-05-24 00:54:14,412 slave.__main__   9
```
Пройдем по порядку. Для начала имортируем модуль `4_dictConfig` в котором инициализируем логгеры, это он в первой строке сообщает какие логгеры были настроены. Мне нравится подход, при котром логгеры инициализируюися в одном модуле, и затем получаются getLogger -ом по необходимости.

Затем имортируется модуль `6_inh_slave`, и в нем, при вызове getLogger -а к имени инициализированного логгера `slave` через точку добавлен `__name__` (вернет имя модуля если модуль импортируется), что определяет логгер-потомок `slave` -а с именем slave.6_inh_slave. Логгер-потомок наследует поведение логгера-родителя, однако теперь понятно из логгера какого модуля была сделана запись. Можно в наследовании подставлять имя пакета, название функционального блока или класса, здесь как душе угодно. 
