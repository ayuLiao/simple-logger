'''
日志模块
'''
import logging
import logging.handlers
from logging import *

from log4mongo.handlers import MongoHandler

from configs import *
from webhook_robot import BaseMsgBot

msg_bot = BaseMsgBot()

LOG_FILENAME = 'main.log'
LOG_LEVEL = ERROR


class MyLogger(Logger):

    def __init__(self, name, level=NOTSET):
        super(MyLogger, self).__init__(name=name, level=level)

    def _log(
            self,
            level,
            msg,
            args,
            exc_info=None,
            extra=None,
            stack_info=False,
            robot=False
    ) -> None:
        """

        :param level:
        :param msg:
        :param args:
        :param exc_info:
        :param extra:
        :param stack_info:
        :param robot: 是否要通过飞书机器人将日志发送到飞书上
        :return:
        """
        super(MyLogger, self)._log(level, msg, args, exc_info, extra, stack_info)
        if robot or level >= LOG_LEVEL:
            msg_bot.send_base_msg(msg)

    def __reduce__(self):
        return getLogger, ()


logger = MyLogger('bestpitcher_log', WARNING)


def set_logger(mongodb=False):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                  '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if mongodb:
        # log output to mongodb
        mon_handler = MongoHandler(host=mongodb_config['host'],
                                   port=int(mongodb_config['port']),
                                   database_name=mongodb_config['database_name'],
                                   # username=mongodb_config['user'],
                                   # password=mongodb_config['password'],
                                   # authentication_db=db_name
                                   )
        mon_handler.setLevel(logging.INFO)
        logger.addHandler(mon_handler)
    else:
        # log output to file
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
        logger.addHandler(file_handler)


set_logger(mongodb=True)
