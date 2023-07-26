import os
import json
import requests
from typing import Dict, List, Optional, Tuple, Union, Any

# import torch
# from fastchat.conversation import (compute_skip_echo_len, get_default_conv_template)
# from fastchat.serve.inference import load_model as load_fastchat_model
from langchain.llms.base import LLM
from langchain.callbacks.manager import (
    CallbackManagerForLLMRun,
)
# from langchain.llms.utils import enforce_stop_tokens
# from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer

from utils.log import logger

# from config import *

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class AnswerResult:
    """
    消息实体
    """
    # {'question': 'Hi', 'chat_history': [], 'answer': 'Hello! How can I assist you today?'}
    question: str
    chat_history: List[List[str]] = []
    answer: str
    # llm_output: Optional[dict] = None

class ChatLLM(LLM):
    """Wrapper around LLM Model"""
     # define class variable here, Class variables are common across instantiated objects.
    api_base_url: str = "http://10.96.81.106:8000"
    """API base Url"""
    max_token: int = 10000
    temperature: float = 0.95
    """What sampling temperature to use."""
    top_p = 0.7
    history = []
    model_type: str = "chatglm"
    model_name: str = "ChatGLM-6B",
    tokenizer: object = None
    model: object = None
    streaming: bool = False
    """Penalizes repeated tokens."""


    def __init__(self, model_name, temperature, verbose):
        logger.debug(f"model_name:{model_name}, temperature:{temperature}, verbose:{verbose}")
        super().__init__()
        # define lcoal variable here, can be use by self.* after constructor

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling FastChat API."""
        normal_params = {
            "model": self.model_name,
            "prompt": '',
            "history": [],
            "max_length": self.max_token,
            "top_p": self.top_p,
            "temperature": self.temperature
        }
        return {**normal_params}

    @property
    def _llm_type(self) -> str:
        return self.model_type

    @property
    def _api_base_url(self) -> str:
        return self.api_base_url

    def set_api_key(self, api_key: str):
        pass

    def set_api_base_url(self, api_base_url: str):
        self.api_base_url = api_base_url

    def call_model_name(self, model_name):
        self.model_name = model_name


    def _stream(self, prompt: str, history: List[List[str]] = []):
        """Call FastChat with streaming flag and return the resulting generator.

        BETA: this is a beta feature while we figure out the right abstraction.
        Once that happens, this interface could change.

        Args:
            prompt: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            A generator representing the stream of tokens from OpenAI.

        Example:
            .. code-block:: python

                generator = fastChat.stream("Tell me a joke.")
                for token in generator:
                    yield token
        """
        logger.debug(f"prompt:{prompt}, history:{history}")
        params = self._default_params
        # for chatGLM
        params["prompt"] = prompt
        params["history"] = history
        logger.debug(f'params:{params}')

        headers = {"Content-Type": "application/json"}
        logger.debug(f"api_base_url:{self.api_base_url}")
        response = requests.post(
            self.api_base_url,
            headers=headers,
            json=params,
            stream=False,
        )
        logger.debug(f"response:{response.json()}")
        data = response.json() #json.loads(response.decode("utf-8"))
        return data

    def generatorAnswer(self, prompt: str,
                        history: List[List[str]] = [],
                        streaming: bool = False):

        print(f"generatorAnswer> prompt:{prompt},history:{history}, streaming:{streaming}")
        generator = self._stream(prompt, history)
        print(f"generatorAnswer> generator:{generator}")
        # generator:{'response': 'Hi, how can I assist you today?', 'history': [["Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n我是文字\n\n我是文字\n\n我是文字\n\n我是文字\n\n我是文字\n\n我是文字\n\nQuestion: Hi\nHelpful Answer:", 'Hi, how can I assist you today?']], 'status': 200, 'time': '2023-07-16 19:07:54'}
        history += [[prompt, generator["response"]]]
        # question: str
        # chat_history: List[List[str]] = []
        # answer: str
        answer_result = AnswerResult()
        print(f"generatorAnswer> answer_result:{answer_result}")
        answer_result.question = prompt
        answer_result.chat_history = history
        print(f"generatorAnswer> history:{answer_result.chat_history}")
        # answer_result.llm_output = {"answer": generator["response"]}
        answer_result.answer = generator["response"]
        # print(f"generatorAnswer> llm_output:{answer_result.llm_output}")
        print(f"generatorAnswer> answer_result 1:{answer_result}")
        yield answer_result

    def _call(self, 
              prompt: str, 
              stop: Optional[List[str]] = None, 
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any,
    ) -> str:
        print(f"_call> prompt:{prompt}, Optional:{Optional}, run_manager:{run_manager}")
        res = self.generatorAnswer(prompt=prompt, history=self.history, streaming=False)
        print(f"_call> res:{json.dumps(res.__dict__, ensure_ascii=False, indent=4)}")
        # {'question': 'Hi', 'chat_history': [], 'answer': 'Hello! How can I assist you today?'}
        return json.dumps(res.__dict__, ensure_ascii=False, indent=4)


    def load_llm(self,
                   llm_device="cpu",
                   num_gpus='auto',
                   device_map: Optional[Dict[str, int]] = None,
                   **kwargs):
        pass
        # if 'chatglm' in self.model_name_or_path.lower():
        #     self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path,
        #                                                trust_remote_code=True, cache_dir=os.path.join(MODEL_CACHE_PATH, self.model_name_or_path))                            
        #     if torch.cuda.is_available() and llm_device.lower().startswith("cuda"):

        #         num_gpus = torch.cuda.device_count()
        #         if num_gpus < 2 and device_map is None:
        #             self.model = (AutoModel.from_pretrained(
        #                 self.model_name_or_path, trust_remote_code=True, cache_dir=os.path.join(MODEL_CACHE_PATH, self.model_name_or_path), 
        #                 **kwargs).half().cuda())
        #         else:
        #             from accelerate import dispatch_model

        #             model = AutoModel.from_pretrained(self.model_name_or_path,
        #                                             trust_remote_code=True, cache_dir=os.path.join(MODEL_CACHE_PATH, self.model_name_or_path),
        #                                             **kwargs).half()

        #             if device_map is None:
        #                 device_map = auto_configure_device_map(num_gpus)

        #             self.model = dispatch_model(model, device_map=device_map)
        #     else:
        #         self.model = (AutoModel.from_pretrained(
        #             self.model_name_or_path,
        #             trust_remote_code=True, cache_dir=os.path.join(MODEL_CACHE_PATH, self.model_name_or_path)).float().to(llm_device))
        #     self.model = self.model.eval()

        # else:     
        #     self.model, self.tokenizer = load_fastchat_model(
        #         model_path = self.model_name_or_path,
        #         device = llm_device,
        #         num_gpus = num_gpus
        #     ) 
            