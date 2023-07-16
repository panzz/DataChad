from pathlib import Path
import os

DEBUG = True

PAGE_ICON = "🤖"
APP_NAME = "DataChad"
MODEL = "gpt-3.5-turbo"
PROJECT_URL = "https://github.com/gustavz/DataChad"

K = 6
FETCH_K = 30
CHUNK_SIZE = 512
CHUNK_OVERLAP = 128
TEMPERATURE = 0.7
MAX_TOKENS = 3357
MODEL_N_CTX = 1000
DISTANCE_METRIC = "cos"
MAXIMAL_MARGINAL_RELEVANCE = True

ENABLE_ADVANCED_OPTIONS = True
ENABLE_LOCAL_MODE = True
# ENABLE_LOCAL_MODE = False


# 本地模型存放的位置
DIR = os.path.dirname(os.path.dirname(__file__))
print (f'DIR: {DIR}')
# MODEL_DIR = "model/"
MODEL_DIR = os.path.join(os.path.dirname(DIR), "common_models/")
print (f'MODEL_DIR: {MODEL_DIR}')

# MODEL_PATH = Path.cwd() / "models"
MODEL_PATH = os.path.join(os.path.dirname(DIR), "common_models")
print (f'MODEL_PATH: {MODEL_PATH}')
GPT4ALL_BINARY = "ggml-gpt4all-j-v1.3-groovy.bin"
print (f'GPT4ALL_BINARY: {str(MODEL_PATH + "/" + GPT4ALL_BINARY)}')


DATA_PATH = Path.cwd() / "data"
# DEFAULT_DATA_SOURCE = "https://gitee.com/gitee-community/bullshit-codes.git"
# DEFAULT_DATA_SOURCE = "https://github.com/gustavz/DataChad.git"
# DEFAULT_DATA_SOURCE = "https://developerforum.lenovo.com/s3/dev-forum-prod/assets/107bb029-c4ea-4b51-9343-b56fc740cfd2.pdf"
DEFAULT_DATA_SOURCE = "/Users/panzz/Vobs/_dev/_chatbot/chatgpt-longchain-datachad/data/test"

MODE_HELP = """
Choose between `OpenAI` which uses the openai library to make API calls, or `Local` which runs all operations (Embedding, Vector Stor and LLM) locally.\n
To enable `Local` mode (disabled for the demo) set `ENABLE_LOCAL_MODE` to `True` in `datachad/constants.py` before deploying the app.\n
Furthermore you need to have the model binaries downloaded and stored inside `./models/`\n
"""

LOCAL_MODE_DISABLED_HELP = """
This is a demo hosted with limited resources. Local Mode is not enabled.\n
To use Local Mode deploy the app on your machine of choice with `ENABLE_LOCAL_MODE` set to `True`.
"""

AUTHENTICATION_HELP = f"""
Your credentials are only stored in your session state.\n
The keys are neither exposed nor made visible or stored permanently in any way.\n
Feel free to check out [the code base]({PROJECT_URL}) to validate how things work.
"""

USAGE_HELP = f"""
These are the accumulated OpenAI API usage metrics.\n
The app uses `gpt-3.5-turbo` for chat and `text-embedding-ada-002` for embeddings.\n
Learn more about OpenAI's pricing [here](https://openai.com/pricing#language-models)
"""

OPENAI_HELP = """
You can sign-up for OpenAI's API [here](https://openai.com/blog/openai-api).\n
Once you are logged in, you find the API keys [here](https://platform.openai.com/account/api-keys)
"""

ACTIVELOOP_HELP = """
You can create an ActiveLoops account (including 500GB of free database storage) [here](https://www.activeloop.ai/).\n
Once you are logged in, you find the API token [here](https://app.activeloop.ai/profile/gustavz/apitoken).\n
The organisation name is your username, or you can create new organisations [here](https://app.activeloop.ai/organization/new/create)
"""

UPLOAD_HELP = """
You can upload a single or multiple files. With each upload, all files in the batch are embedded into a single vector store.\n
**Important**: If you upload new files after you already have uploaded files, a new vector store that includes all previously uploaded files is created.
This means for each combination of uploaded files, a new vector store is created.\n
To treat your new upload independently, you need to remove the previous uploads by clicking the `X`, right next to the uploaded file name.\n
**!!! All uploaded files are removed permanently from the app after the vector stores are created !!!**
"""
