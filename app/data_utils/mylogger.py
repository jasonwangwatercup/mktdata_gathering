# -*- coding: utf-8 -*-
# for the sake of avoiding initiating several loggers at the same time.

import logging
import logging.handlers


class MLogger(object):
    __is_logger_inited = {}
    __logger = {}
    __formatter = {}

    @classmethod
    def __init(cls, level3, level2, level1, level0, loggerName, logfile1, logfile2):
        formatter = logging.Formatter(cls.__formatter[loggerName])
        cls.__logger[loggerName] = logging.getLogger(loggerName)
        cls.__logger[loggerName].setLevel(level0)

        fle = logging.handlers.RotatingFileHandler(logfile1, mode='a', maxBytes=10000000, backupCount=50, encoding='utf-8')
        fle.setLevel(level1)
        fle.setFormatter(formatter)

        fileerror = logging.handlers.RotatingFileHandler(logfile2, mode='a', maxBytes=10000000, backupCount=50, encoding='utf-8')
        fileerror.setLevel(level2)
        fileerror.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(level3)
        console.setFormatter(formatter)

        cls.__logger[loggerName].addHandler(fle)
        cls.__logger[loggerName].addHandler(fileerror)
        cls.__logger[loggerName].addHandler(console)

    @classmethod
    def init_logger(cls, loggerName, formatter, logfile1, logfile2, level3=logging.ERROR, level2=logging.WARNING, level1=logging.DEBUG, level0=logging.DEBUG):
        if loggerName not in cls.__is_logger_inited:
            cls.__is_logger_inited[loggerName] = False
        if cls.__is_logger_inited[loggerName] is False:
            cls.__formatter[loggerName] = formatter
            cls.__init(level3, level2, level1, level0, loggerName, logfile1, logfile2)
            cls.__is_logger_inited[loggerName] = True
            print "mLogger logger %s is initiated. id: %s." % (loggerName, id(cls.__logger[loggerName]))

            return cls.__logger[loggerName]
        else:
            print "mLogger logger %s already initiated. id: %s." % (loggerName, id(cls.__logger[loggerName]))
            return cls.__logger[loggerName]

    @classmethod
    def print_stat(cls, loggername):
        if (loggername in cls.__is_logger_inited) and cls.__is_logger_inited[loggername] is True:
            print "mLogger logger %s has beed initiated. id: %s." % (loggername, id(cls.__logger[loggername]))
        else:
            print "mLogger logger %s not initiated yet." % loggername
