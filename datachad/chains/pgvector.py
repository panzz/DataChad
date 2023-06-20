# import deeplake
import os
from langchain.vectorstores import DeepLake, VectorStore, FAISS

from datachad.constants import DATA_PATH
from datachad.io import clean_string_for_storing
from datachad.loader import load_data_source, split_docs
from datachad.logging import logger
from datachad.models import MODES, get_embeddings


def get_faiss_dataset_path(data_source: str, options: dict, credentials: dict) -> str:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    dataset_name = clean_string_for_storing(data_source)
    # we need to differntiate between differently chunked datasets
    dataset_name += f"-{options['chunk_size']}-{options['chunk_overlap']}-{options['model'].embedding}"
    logger.debug("dataset_name:%r" %(dataset_name))
    # if options["mode"] == MODES.LOCAL:
    #     dataset_path = str(DATA_PATH / dataset_name)
    # else:
    #     dataset_path = f"hub://{credentials['activeloop_org_name']}/{dataset_name}"
    dataset_path = str(DATA_PATH / dataset_name)
    logger.debug("dataset_path:%r" %(dataset_path))
    return dataset_path

def load_vector_store(vs_path, embeddings):
    return FAISS.load_local(vs_path, embeddings)

def get_faiss_vector_store(data_source: str, options: dict, credentials: dict) -> VectorStore:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    # either load existing vector store or upload a new one to the hub
    embeddings = get_embeddings(options, credentials)
    logger.debug("embeddings:%r" %(embeddings))
    dataset_path = get_faiss_dataset_path(data_source, options, credentials)
    logger.debug("dataset_path:%r" %(dataset_path))
    docs = load_data_source(data_source)
    logger.debug("docs:%r, options:%r" %(len(docs), options))
    if os.path.isdir(dataset_path) and os.path.isfile(dataset_path+"/index.faiss"):
        vector_store = load_vector_store(dataset_path, embeddings)
        vector_store.add_documents(docs)
        logger.debug("add_documents vector_store:%r" %(vector_store))
        vector_store.save_local(dataset_path)
    else:
        vector_store = FAISS.from_documents(docs, embeddings)  ##docs 为Document列表
        logger.debug("from_documents vector_store:%r" %(vector_store))
    
    # if deeplake.exists(dataset_path, token=credentials["activeloop_token"]):
    #     logger.info(f"Dataset '{dataset_path}' exists -> loading")
    #     vector_store = DeepLake(
    #         dataset_path=dataset_path,
    #         read_only=True,
    #         embedding_function=embeddings,
    #         token=credentials["activeloop_token"],
    #     )
    #     vector_store = load_vector_store(vs_path, self.embeddings)
    # else:
    #     logger.info(f"Dataset '{dataset_path}' does not exist -> uploading")
    #     docs = load_data_source(data_source)
    #     logger.debug("docs:%r, options:%r" %(len(docs), options))
    #     docs = split_docs(docs, options)
    #     logger.debug("docs:%r" %(len(docs)))
    #     # vector_store = DeepLake.from_documents(
    #     #     docs,
    #     #     embeddings,
    #     #     dataset_path=dataset_path,
    #     #     token=credentials["activeloop_token"],
    #     # )
    #     vector_store = FAISS.from_documents(docs, embeddings) 
    #     logger.debug("vector_store:%r" %(vector_store))
    logger.info(f"Vector Store {dataset_path} loaded!")
    return vector_store
