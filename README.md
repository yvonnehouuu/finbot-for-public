# Finbot

## main.py -> linebot
pull the questions to `chatbot.py`
</br></br>

## chatbot.py -> Groq Chatbot 
connect with `main.py`
</br></br>

## (Unfinished) ragchat.py -> Rag + Groq Chatbot
connect with the folder 'data'
* 卡在`upset` 函數回傳值為空
  ``` python
  vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        collection_metadata={"hnsw:space": "cosine"}  # 使用餘弦相似度
    )
  ```
  最底層為 :
  ``` python
  @abstractmethod
    def _upsert(
        self,
        collection_id: UUID,
        ids: IDs,
        embeddings: Embeddings,
        metadatas: Optional[Metadatas] = None,
        documents: Optional[Documents] = None,
        uris: Optional[URIs] = None,
    ) -> bool:
        """[Internal] Add or update entries in the a collection specified by UUID.
        If an entry with the same id already exists, it will be updated,
        otherwise it will be added.

        Args:
            collection_id: The collection to add the embeddings to
            ids: The ids to associate with the embeddings. Defaults to None.
            embeddings: The sequence of embeddings to add
            metadatas: The metadata to associate with the embeddings. Defaults to None.
            documents: The documents to associate with the embeddings. Defaults to None.
            uris: URIs of data sources for each embedding. Defaults to None.
        """
        pass
  ```
