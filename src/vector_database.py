import os
from docarray import DocList, BaseDoc
from docarray.typing import NdArray
from typing import List
from vectordb import InMemoryExactNNVectorDB, HNSWVectorDB
import random
from const import *
from framedoc import TextEmbedding, FrameDoc, FrameDocs
          
class VectorDB:
    text_embedding = TextEmbedding()
    workspace = os.getcwd()
    method = "ANN"

    def __init__(self, method="ANN"):
        # Check if parent workspace exists
        if not os.path.isdir(WORKSPACE):
            os.mkdir(WORKSPACE, 0o666)
        # Create new workspae
        exits = [int(name.rsplit("_")[1]) for name in os.listdir(WORKSPACE)]
        while True:
            id = random.getrandbits(128)
            if id not in exits:
                self.workspace = os.path.join(
                    self.workspace, WORKSPACE, "DB_" + str(id)
                )
                break

        self.method = method
        #   Approximate Nearest Neighbour based on HNSW algorithm
        if method == "ANN":
            self.DB = HNSWVectorDB[FrameDoc](workspace=self.workspace)

        # Exhaustive search on the embeddings
        else:
            self.DB = InMemoryExactNNVectorDB[FrameDoc](workspace=self.workspace)

    def index(self, framedocs: FrameDocs):
        doc_list = framedocs()
        # Index database
        self.DB.index(inputs=DocList[FrameDoc](doc_list))

    def search(self, query_text: str, topk=100) -> FrameDocs:
        query_doc = FrameDoc(embedding=self.text_embedding(query_text))
        return FrameDocs(self.DB.search(inputs=DocList[FrameDoc]([query_doc]), limit=topk)[
            0
        ].matches)

    def delete(self, del_doc_list: List[FrameDoc]):
        self.DB.delete(docs=DocList[FrameDoc](del_doc_list))
        

if __name__ == "__main__":
    pass