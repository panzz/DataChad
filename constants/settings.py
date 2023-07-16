
import os
# import logging
from utils.log import logger

# LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logging.basicConfig(format=LOG_FORMAT)


# 本地模型存放的位置
DIR = os.path.dirname(os.path.dirname(__file__))
# DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print (f'DIR: {DIR}')
# MODEL_DIR = "model/"
MODEL_DIR = os.path.join(os.path.dirname(DIR), "common_models/")
print (f'MODEL_DIR: {MODEL_DIR}')

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
}

# Embedding model name
EMBEDDING_MODEL = "text2vec"

logger.info(f"""
loading model config:
dir: {os.path.dirname(os.path.dirname(__file__))},
MODEL_DIR: {MODEL_DIR},
embedding_model_dict: {embedding_model_dict},
EMBEDDING_MODEL: {EMBEDDING_MODEL}
""")

# 是否开启跨域，默认为False，如果需要开启，请设置为True
# is open cross domain
OPEN_CROSS_DOMAIN = False

# Bing 搜索必备变量
# 使用 Bing 搜索需要使用 Bing Subscription Key
# 具体申请方式请见 https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/quickstarts/rest/python
BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
BING_SUBSCRIPTION_KEY = ""

# 
CHATGLM_ENTER_POINT = "http://10.96.81.106:8000"