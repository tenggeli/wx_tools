# _*_ coding:UTF-8 _*_

import os

import logging
import logging.handlers


class MyLogger(object):
    '''
    classdocs
    '''

    def __init__(self):
        pass

    logger = None

    @staticmethod
    def getLogger():
        #         path='/Users/tony/work/workspace/bi.jobscheduler/log/myapp.log'
        #         path = '../log/myapp.log'
        #         path = '/Users/tony/github/bi.harrypotte/bi.harrypotte.harrypotte/jobscheduler/log/myapp.log'
        path = os.getcwd() + '/app/log/myapp.log'
        if MyLogger.logger is None:
            logging.basicConfig(level = logging.DEBUG,
                                format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt = '%m-%d %H:%M',
                                filename = path,
                                filemode = 'a+')
            logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s", "%D-%H:%M:%S")
            logging.handlers.TimedRotatingFileHandler(
                path, when='S', interval=1, backupCount=40)
            MyLogger.logger = logging
        return MyLogger.logger

    def initLog(self):
        logging.basicConfig(level=logging.INFO,
                            filename='./log/log.txt',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filemode='w',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        # use logging
        logging.info('this is a loggging info message')
        logging.debug('this is a loggging debug message')
        logging.warning('this is loggging a warning message')
        logging.error('this is an loggging error message')
        logging.critical('this is a loggging critical message')


if __name__ == '__main__':
    print ('test..')

    MyLogger.getLogger().info('This is info message')
    MyLogger.getLogger().info('This is info message...')

    try:
        print 'try...'
        r = 10 / int('a')
        print 'result:', r
    except ValueError, e:
        print 'ValueError:', e
        MyLogger.getLogger().error('error: {}'.format(e))
    except ZeroDivisionError, e:
        print 'ZeroDivisionError:', e
    finally:
        print 'finally...'

#     logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='myapp.log',
#                 filemode='w')
#
#     #################################################################################################
#     #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
#     console = logging.StreamHandler()
#     console.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
#     #################################################################################################
#
#     logging.debug('This is debug message')
#     logging.info('This is info message')
#     logging.warning('This is warning message')
# #     MyLogger.getLogger()
