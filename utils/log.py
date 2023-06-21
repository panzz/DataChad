import logging
import os
# import sys
import yaml
import logging.config as log_config

LOGGING_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logging.yml")
# print('dfa> LOGGING_CONFIG_PATH:%r' %(LOGGING_CONFIG_PATH))
# print('dfa> __name__:%r' %(__name__))

with open(LOGGING_CONFIG_PATH, 'r', encoding="utf-8") as file_logging:
    # print('logging> file_logging:%r' %(file_logging))
    dict_conf = yaml.load(file_logging, Loader=yaml.FullLoader)
    # print('logging> dict_conf:%r' %(dict_conf))
    log_config.dictConfig(dict_conf)

logger = logging.getLogger(__name__)
log = logging.getLogger("log")


# logging.config.fileConfig('./../logging.conf')

# def configure_logger(debug: int = 0) -> None:
#     # boilerplate code to enable logging in the streamlit app console
#     log_level = logging.DEBUG if debug == 1 else logging.INFO
#     logger.setLevel(log_level)
#     # 创建一个流处理器handler并设置日志级别
#     stream_handler = logging.StreamHandler(stream=sys.stdout)
#     stream_handler.setLevel(log_level)
#     # 为日志器logger添加上面创建好的处理器 stream_handler
#     # formatter = logging.Formatter("%(message)s")
#     formatter = logging.Formatter("%(asctime)s %(module)s.%(funcName)s(%(levelno)s.%(lineno)d) %(message)s")
#     stream_handler.setFormatter(formatter)

#     logger.addHandler(stream_handler)
#     logger.propagate = False


# configure_logger(1 if DEBUG else 0)

# configure_logger()
