from logger import logger

def test_logger():
    logger.info('[info] 这条日志只会记录在MongoDB中')
    # exc_info 获得报错时的调用链
    logger.error('[error] 这条日志会发送到WebHook机器人上', exc_info=True)
    logger.warning('[warning] 这条日志也会发送到WebHook', robot=True)


if __name__ == '__main__':
    test_logger()