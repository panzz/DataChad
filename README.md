# DataChad 🤖

This is an app that let's you ask questions about any data source by leveraging [embeddings](https://platform.openai.com/docs/guides/embeddings), [vector databases](https://www.activeloop.ai/), [large language models](https://platform.openai.com/docs/models/gpt-3-5) and last but not least [langchains](https://github.com/hwchase17/langchain)

## How does it work?

1. Upload any `file(s)` or enter any `path` or `url`
2. The data source is detected and loaded into text documents
3. The text documents are embedded using openai embeddings
4. The embeddings are stored as a vector dataset to activeloop's database hub
5. A langchain is created consisting of a LLM model (`gpt-3.5-turbo` by default) and the vector store as retriever
6. When asking questions to the app, the chain embeds the input prompt and does a similarity search of in the vector store and uses the best results as context for the LLM to generate an appropriate response
7. Finally the chat history is cached locally to enable a [ChatGPT](https://chat.openai.com/) like Q&A conversation

## Good to know
- The app only runs on `py>=3.10`!
- As default context this git repository is taken so you can directly start asking question about its functionality without chosing an own data source.
- To run locally or deploy somewhere, execute `cp .env.template .env` and set credentials in the newly created `.env` file. Other options are manually setting of system environment variables, or storing them into `.streamlit/secrets.toml` when hosted via streamlit.
- If you have credentials set like explained above, you can just hit `submit` in the authentication without reentering your credentials in the app.
- To enable `Local Mode` (disabled for the demo) set `ENABLE_LOCAL_MODE` to `True` in `datachad/constants.py`. You need to have the model binaries downloaded and stored inside `./models/`
- Currently supported `Local Mode` OSS model is [GPT4all](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin). To add more models update `datachad/models.py`
- If you are running `Local Mode` all your data stays locally on your machine. No API calls are made. Same with the embeddings database which stores its data to `./data/`
- Your data won't load? Feel free to open an Issue or PR and contribute!
- Yes, Chad in `DataChad` refers to the well-known [meme](https://www.google.com/search?q=chad+meme)

## How does it look like?

<img src="./datachad.png" width="100%"/>

## TODO LIST
If you like to contribute, feel free to grab any task
- [x] Refactor utils, especially the loaders
- [x] Add option to choose model and embeddings
- [x] Enable fully local / private mode
- [x] Add option to upload multiple files to a single dataset
- [x] Decouple datachad modules from streamlit
- [ ] Support streaming responses
- [ ] Add Image caption and Audio transcription support



#DataChad🤖

这是一款应用程序，可让您通过利用 [embeddings](https://platform.openai.com/docs/guides/embeddings)、[向量数据库](https://www.activeloop.ai) 询问有关任何数据源的问题 /)、[大型语言模型](https://platform.openai.com/docs/models/gpt-3-5) 最后但并非最不重要的 [langchains](https://github.com/hwchase17/langchain)

## 它如何运作？

1. 上传任何“文件”或输入任何“路径”或“网址”
2. 检测数据源并加载到文本文档中
3. 使用openai embeddings嵌入文本文档
4. 嵌入作为向量数据集存储到activeloop的数据库中心
5. 创建一个由LLM模型（默认为`gpt-3.5-turbo`）和作为检索器的向量存储组成的langchain
6. 当向应用程序提问时，链嵌入输入提示并在向量存储中进行相似性搜索，并使用最佳结果作为 LLM 的上下文以生成适当的响应
7. 最后将聊天记录缓存到本地，实现[ChatGPT](https://chat.openai.com/) 类Q&A对话

## 好消息
- 该应用程序只能在 `py>=3.10` 上运行！
- 作为默认上下文，此 git 存储库被采用，因此您可以直接开始询问有关其功能的问题，而无需选择自己的数据源。
- 要在本地运行或部署在某处，请执行 `cp .env.template .env` 并在新创建的 `.env` 文件中设置凭据。 其他选项是手动设置系统环境变量，或者在通过 streamlit 托管时将它们存储到 .streamlit/secrets.toml 中。
- 如果您按照上述说明设置了凭据，则只需在身份验证中点击“提交”即可，而无需在应用程序中重新输入您的凭据。
- 要启用“本地模式”（在演示中禁用），请在“datachad/constants.py”中将“ENABLE_LOCAL_MODE”设置为“True”。 您需要下载模型二进制文件并将其存储在 ./models/ 中
- 当前支持的“本地模式”OSS 模型是 [GPT4all](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin)。 要添加更多模型，请更新 `datachad/models.py`
- 如果您正在运行“本地模式”，您的所有数据都将保留在本地机器上。 不进行任何 API 调用。 与将数据存储到 ./data/ 的嵌入数据库相同
- 您的数据无法加载？ 随意打开 Issue 或 PR 并做出贡献！
- 是的，`DataChad` 中的 Chad 指的是众所周知的 [meme](https://www.google.com/search?q=chad+meme)

## 它看起来如何？

<img src="./datachad.png" width="100%"/>

## 待办事项列表
如果你喜欢贡献，随时抓住任何任务
- [x] 重构实用程序，尤其是加载程序
- [x] 添加选项以选择模型和嵌入
- [x] 启用完全本地/私人模式
- [x] 添加将多个文件上传到单个数据集的选项
- [x] 将 datachad 模块与 streamlit 分离
- [ ] 支持流式响应
- [ ] 添加图片说明和音频转录支持

https://www.activeloop.ai/resources/data-chad-an-ai-app-with-lang-chain-deep-lake-to-chat-with-any-data/

streamlit run app.py --server.port 8080

你好，列举出datachad的项目结构，并对源代码做简要说明