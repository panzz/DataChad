# import deeplake
import os
from langchain.vectorstores import VectorStore
from langchain.vectorstores.pgvector import PGVector, DistanceStrategy

from datachad.constants import DATA_PATH
from datachad.io import clean_string_for_storing
from datachad.loader import load_data_source, split_docs
from utils.log import logger
from datachad.models import MODES, get_embeddings


def get_dataset_path(data_source: str, options: dict, credentials: dict) -> str:
    logger.debug(f"data_source: {data_source}, options:{options}")
    dataset_name = clean_string_for_storing(data_source)
    logger.debug(f"dataset_name: {dataset_name}")
    # we need to differntiate between differently chunked datasets
    dataset_name += f"-{options['chunk_size']}-{options['chunk_overlap']}-{options['model'].embedding}"
    logger.debug(f"dataset_name: {dataset_name}")
    logger.debug(f"options['mode']: {options['mode']}")
    if options["mode"] == MODES.LOCAL:
        dataset_path = str(DATA_PATH / dataset_name)
    else:
        # dataset_path = f"hub://{credentials['activeloop_org_name']}/{dataset_name}"
        try:
            dataset_path = PGVector.connection_string_from_db_params(
                driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
                host=os.environ.get("PGVECTOR_HOST", "10.122.81.156"),
                port=int(os.environ.get("PGVECTOR_PORT", "5432")),
                database=os.environ.get("PGVECTOR_DATABASE", "pgvector"),
                user=os.environ.get("PGVECTOR_USER", "a_appconnect"),
                password=os.environ.get("PGVECTOR_PASSWORD", "A_AppConnect"),
            )
            logger.debug(f"dataset_path: {dataset_path}")
        except Exception as e:
            logger.error(f"ERROR: {e}")
    return dataset_path, dataset_name


def get_pavector_vector_store(data_source: str, options: dict, credentials: dict) -> VectorStore:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    # either load existing vector store or upload a new one to the hub
    embeddings = get_embeddings(options, credentials)
    logger.debug("embeddings:%r" %(embeddings))
    dataset_path, dataset_name = get_dataset_path(data_source, options, credentials)
    logger.debug("dataset_path:%r, dataset_name:%r" %(dataset_path, dataset_name))
    try:
        store = PGVector(
            connection_string=dataset_path,
            embedding_function=embeddings,
            collection_name=dataset_name,
            distance_strategy=DistanceStrategy.COSINE,
        )
        logger.debug("store:%r" %(store))
        retriever = store.as_retriever()
        # if retriever:
        #     logger.info(f"Dataset '{dataset_path}' exists -> loading")
        #     vector_store = PGVector.from_existing_index(
        #         embedding=embeddings,
        #         collection_name=dataset_name,
        #         distance_strategy=DistanceStrategy.EUCLIDEAN,
        #         pre_delete_collection=False,
        #         connection_string=dataset_path,
        #     )
        # else:
        logger.info(f"Dataset '{dataset_path}' does not exist -> uploading")
        docs = load_data_source(data_source)
        logger.debug("docs:%r, options:%r" %(len(docs), options))
        docs = split_docs(docs, options)
        logger.debug(f"docs:{docs}, dataset_path:{dataset_path}, dataset_name:{dataset_name}, embeddings:{embeddings}")
        vector_store = PGVector.from_documents(
            documents=docs,
            embedding=embeddings,
            connection_string=dataset_path,
            collection_name=dataset_name,
        )
        logger.debug("vector_store:%r" %(vector_store))
    except Exception as e:
        logger.error(f"ERROR: {e}")
    # logger.info(f"{file} 未能成功加载")
    logger.debug("vector_store:%r" %(vector_store))
    logger.info(f"Vector Store {dataset_path} loaded!")
    return vector_store
