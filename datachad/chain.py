from langchain.chains import ConversationalRetrievalChain

# from datachad.database import get_vector_store
from datachad.chains.deeplake import get_deeplake_vector_store
from datachad.chains.faiss import get_faiss_vector_store
from datachad.chains.pgvector import get_pavector_vector_store
from datachad.logging import logger
from datachad.models import get_model


def get_deeplake_chain(
    data_source: str, options: dict, credentials: dict
) -> ConversationalRetrievalChain:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    # create the langchain that will be called to generate responses
    vector_store = get_deeplake_vector_store(data_source, options, credentials)
    logger.debug("vector_store:%r" %(vector_store))
    retriever = vector_store.as_retriever()
    logger.debug("retriever:%r" %(retriever))
    # Search params "fetch_k" and "k" define how many documents are pulled from the hub
    # and selected after the document matching to build the context
    # that is fed to the model together with the user prompt
    search_kwargs = {
        "maximal_marginal_relevance": options["maximal_marginal_relevance"],
        "distance_metric": options["distance_metric"],
        "fetch_k": options["fetch_k"],
        "k": options["k"],
    }
    logger.debug("search_kwargs:%r" %(search_kwargs))
    retriever.search_kwargs.update(search_kwargs)
    logger.debug("1 search_kwargs:%r" %(search_kwargs))
    model = get_model(options, credentials)
    logger.debug("model:%r" %(model))
    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
        # we limit the maximum number of used tokens
        # to prevent running into the models context window limit of 4096
        max_tokens_limit=options["max_tokens"],
    )
    logger.info(f"Chain for data source {data_source} and settings {options} build!")
    return chain


def get_faiss_chain(
    data_source: str, options: dict, credentials: dict
) -> ConversationalRetrievalChain:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    # create the langchain that will be called to generate responses
    vector_store = get_faiss_vector_store(data_source, options, credentials)
    logger.debug("vector_store:%r" %(vector_store))
    retriever = vector_store.as_retriever()
    logger.debug("retriever:%r" %(retriever))
    # Search params "fetch_k" and "k" define how many documents are pulled from the hub
    # and selected after the document matching to build the context
    # that is fed to the model together with the user prompt
    search_kwargs = {
        # "maximal_marginal_relevance": options["maximal_marginal_relevance"],
        # "distance_metric": options["distance_metric"],
        "fetch_k": options["fetch_k"],
        "k": options["k"],
    }
    logger.debug("search_kwargs:%r" %(search_kwargs))
    retriever.search_kwargs.update(search_kwargs)
    logger.debug("1 search_kwargs:%r" %(search_kwargs))
    model = get_model(options, credentials)
    logger.debug("model:%r" %(model))
    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
        # we limit the maximum number of used tokens
        # to prevent running into the models context window limit of 4096
        max_tokens_limit=options["max_tokens"],
    )
    logger.info(f"Chain for data source {data_source} and settings {options} build!")
    return chain


def get_pgvector_chain(
    data_source: str, options: dict, credentials: dict
) -> ConversationalRetrievalChain:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    # create the langchain that will be called to generate responses
    vector_store = get_pavector_vector_store(data_source, options, credentials)
    logger.debug("vector_store:%r" %(vector_store))
    retriever = vector_store.as_retriever()
    logger.debug("retriever:%r" %(retriever))
    # Search params "fetch_k" and "k" define how many documents are pulled from the hub
    # and selected after the document matching to build the context
    # that is fed to the model together with the user prompt
    search_kwargs = {
        "maximal_marginal_relevance": options["maximal_marginal_relevance"],
        "distance_metric": options["distance_metric"],
        "fetch_k": options["fetch_k"],
        "k": options["k"],
    }
    try:
        logger.debug("search_kwargs:%r" %(search_kwargs))
        retriever.search_kwargs.update(search_kwargs)
        logger.debug("1 search_kwargs:%r" %(search_kwargs))
    except Exception as e:
        logger.error(e)
    model = get_model(options, credentials)
    logger.debug("model:%r" %(model))
    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
        # we limit the maximum number of used tokens
        # to prevent running into the models context window limit of 4096
        max_tokens_limit=options["max_tokens"],
    )
    logger.info(f"Chain for data source {data_source} and settings {options} build!")
    return chain

def get_chain(
    data_source: str, options: dict, credentials: dict
) -> ConversationalRetrievalChain:
    logger.debug("data_source:%r, options:%r, credentials:%r" %(data_source, options, credentials))
    # return get_deeplake_chain(data_source, options, credentials)
    # return get_faiss_chain(data_source, options, credentials)
    return get_pgvector_chain(data_source, options, credentials)
