import os
from docarray import DocList
from typing import List
from vectordb import InMemoryExactNNVectorDB, HNSWVectorDB
import random
from const import *
from framedoc import TextEmbedding, FrameDoc, FrameDocs
import multiprocessing


class VectorDB:
    text_embedding = TextEmbedding()
    workspace = os.getcwd()
    method = "ANN"

    def __init__(
        self,
        space="l2",
        max_elements=1024,
        ef_construction=200,
        ef=10,
        M=16,
        allow_replace_deleted=False,
        num_threads=-1,
        method="ANN",
        workspace = None
    ) -> None:
        """_summary_
        :param space: Specifies the similarity metric used for the space (options are "l2", "ip", or "cosine"). The default is "l2".
        :type space: str
        :param max_elements: Sets the initial capacity of the index, which can be increased dynamically. The default is 1024.
        :type max_elements: int
        :param ef_construction: This parameter controls the speed/accuracy trade-off during index construction. The default is 200.
        :type ef_construction: int
        :param ef:This parameter controls the query time/accuracy trade-off. The default is 10.
        :type ef: int
        :param M: This parameter defines the maximum number of outgoing connections in the graph. The default is 16.
        :type M: int
        :param allow_replace_deleted: If set to True, this allows replacement of deleted elements with newly added ones. The default is False.
        :type allow_replace_deleted: int
        :param num_threads: This sets the default number of threads to be used during index and search operations. The default is -1 (All).
        :type num_threads: int
        Returns:
            _type_: _description_
        """
        # Check if parent workspace exists
        if not os.path.isdir(WORKSPACE):
            os.mkdir(WORKSPACE, 0o666)
        if not workspace:
            # Create new workspace
            exits = [int(name.rsplit("_")[1]) for name in os.listdir(WORKSPACE)]
            while True:
                id = random.getrandbits(128)
                if id not in exits:
                    self.workspace = os.path.join(
                        self.workspace, WORKSPACE, "DB_" + str(id)
                    )
                    break
        else:
            self.workspace = os.path.join(
                        self.workspace, WORKSPACE, workspace
                    )
        self.method = method
        
        if num_threads <= 0:
            num_threads = multiprocessing.cpu_count()
            print(f"{num_threads} threads had found...")
            
        #   Approximate Nearest Neighbour based on HNSW algorithm
        if method == "ANN":
            self.DB = HNSWVectorDB[FrameDoc](
                space=space,
                max_elements=max_elements,
                ef_construction=ef_construction,
                ef=ef,
                M=M,
                allow_replace_deleted=allow_replace_deleted,
                num_threads=num_threads,
                workspace=self.workspace,)

        # Exhaustive search on the embeddings
        else:
            self.DB = InMemoryExactNNVectorDB[FrameDoc](
                space=space,
                max_elements=max_elements,
                ef_construction=ef_construction,
                ef=ef,
                M=M,
                allow_replace_deleted=allow_replace_deleted,
                num_threads=num_threads,
                workspace=self.workspace,
            )

    def index(self, framedocs: FrameDocs):
        doc_list = framedocs()
        # Index database
        self.DB.index(inputs=DocList[FrameDoc](doc_list))

    def search(self, query_text: str, topk=100) -> FrameDocs:
        query_doc = FrameDoc(embedding=self.text_embedding(query_text))
        return FrameDocs(
            self.DB.search(inputs=DocList[FrameDoc]([query_doc]), limit=topk)[0].matches
        )

    def delete(self, del_doc_list: List[FrameDoc]):
        self.DB.delete(docs=DocList[FrameDoc](del_doc_list))

if __name__ == "__main__":
    pass
