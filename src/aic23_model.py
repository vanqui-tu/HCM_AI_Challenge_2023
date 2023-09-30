from utils import clean_dbs, get_all_feats
from vector_database import TextEmbedding, VectorDB
from framedoc import FrameDoc, FrameDocs, get_all_docs
from docarray import DocList
from const import *

print("Loading model...")
clean_dbs()
all_feat_files = get_all_feats(feat=FEATURE_PATH)
print(all_feat_files)
doc_list = get_all_docs(all_feat_files)
print("Done...")


class AIC23_Model:
    
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
        print("Index root database...")
        self.root = VectorDB(
            space=space,
            max_elements=max_elements,
            ef_construction=ef_construction,
            ef=ef,
            M=M,
            allow_replace_deleted=allow_replace_deleted,
            num_threads=num_threads,
            method=method,
            workspace=ROOT_DB
        )
        
        self.root.index(doc_list)
        print("Done")
            
    def search(self, query_text: str, audio_texts=[],topk=1000) -> FrameDocs:
        return self.root.search(query_text=query_text, topk=topk).contains(keywords=audio_texts)

    def search_and_visualize(self, query_text: str, audio_texts=None,topk=1000) -> FrameDocs:
        frameDocs = self.search(query_text=query_text, audio_texts=audio_texts, topk=topk)
        frameDocs.visualize()
        return frameDocs
    
model = AIC23_Model()
print("Loading model: Done!")