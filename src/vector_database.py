import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import clip
import json as js
from docarray import DocList, BaseDoc
from docarray.typing import NdArray
from typing import List
import numpy as np
from vectordb import InMemoryExactNNVectorDB, HNSWVectorDB
from natsort import natsorted
import random
from const import *

class TextEmbedding:
    def __init__(self):
        self.device = DEVICE
        self.model, _ = clip.load(MODEL, device=self.device)

    def __call__(self, text: str) -> np.ndarray:
        text_inputs = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_feature = self.model.encode_text(text_inputs)[0]
        return text_feature.detach().cpu().numpy()
    
class FrameDoc(BaseDoc):
    embedding: NdArray[512]
    video_name = ""
    image_path = ""
    keyframe_id = 0
    actual_idx = 0
    actual_time = 0.0
    fps=0
    metadata = {}

    def __str__(self):
        return f"""
            Video name: {self.video_name}
            Image path: {self.image_path}
            Keyframe Id: {self.keyframe_id}
            Actual keyframe idx: {self.actual_idx}
            Time: {self.actual_time}
            FPS: {self.fps}
            Metadata: {self.metadata}
          """
          
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

    def index(self, doc_list: List[FrameDoc]):
        # Index database
        self.DB.index(inputs=DocList[FrameDoc](doc_list))

    def search(self, query_text: str, topk=100):
        query_doc = FrameDoc(embedding=self.text_embedding(query_text))
        return self.DB.search(inputs=DocList[FrameDoc]([query_doc]), limit=topk)[
            0
        ].matches

    def delete(self, del_doc_list: List[FrameDoc]):
        self.DB.delete(docs=DocList[FrameDoc](del_doc_list))
        

if __name__ == "__main__":
    pass