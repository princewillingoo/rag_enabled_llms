import os
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader, HTMLTagReader


def create_and_persist_index(data, index_name):
    print("generating index...", index_name)
    index = VectorStoreIndex.from_documents(data, show_progress=True)
    index.storage_context.persist(persist_dir=index_name)
    return index


def load_existing_index(index_name):
    storage_context = StorageContext.from_defaults(persist_dir=index_name)
    return load_index_from_storage(storage_context)


def get_index(data, index_name):
    if not os.path.exists(index_name):
        return create_and_persist_index(data, index_name)
    else:
        return load_existing_index(index_name)


html_path = os.path.join("data", "Economy_of_China.html")
china_html = HTMLTagReader(tag="main").load_data(file=html_path)
china_index = get_index(china_html, "china")
china_engine = china_index.as_query_engine()

pdf_path = os.path.join("data", "Economy_of_Nigeria.pdf")
nigeria_pdf = PDFReader().load_data(file=pdf_path)
nigeria_index = get_index(nigeria_pdf, "nigeria")
nigeria_engine = nigeria_index.as_query_engine()
