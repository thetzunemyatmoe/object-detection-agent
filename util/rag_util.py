from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(text, chunk_size=200, overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    texts = text_splitter.split_text(text)
    return texts
