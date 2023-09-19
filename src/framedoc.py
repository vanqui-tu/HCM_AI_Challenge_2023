from typing import Any
from const import *
import numpy as np
from docarray import DocList, BaseDoc
from docarray.typing import NdArray
import clip
from transformers import AutoTokenizer, AutoModel, RobertaConfig
import faiss
from utils import (
    separate_paragraphs,
    get_all_scripts,
    check_script,
    get_all_feats,
    create_html_script,
)
import json as js
import pandas as pd
import os
from IPython.display import display, HTML

print("Set up...")
print("Get all script...")
list_script, documents = get_all_scripts()
print("Finished!")

print("Initalize Tokenizer and BERT model")
# Khởi tạo tokenizer và mô hình BERT
model_name = "vinai/phobert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
configuration = RobertaConfig()
model = AutoModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device}.")
model.to(device)
print("Finished!")

# WITH BERT
TRAIN = False
print("Set up Bert and faiss")
if TRAIN:
    print("<--Train-->")
    document_embeddings = []
    name_parents = []
    for i, doc in enumerate(documents):
        child_scripts = separate_paragraphs(doc)
        for i_child, part in enumerate(child_scripts):
            inputs = tokenizer(part, return_tensors="pt", padding=True, truncation=True)
            inputs = {key: value.to(device) for key, value in inputs.items()}  # Chuyển dữ liệu lên GPU
            with torch.no_grad():
                outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)  # Sử dụng trung bình của các embeddings từ BERT
            document_embeddings.append(embeddings)
            name_parents.append(list_script[i])
            
    np_document_embeddings = np.vstack([x.cpu().numpy() for x in document_embeddings])
    np.save("./../data/np_document_embeddings.npy", np_document_embeddings)
    with open("./../data/name_parents.json", 'w', encoding='utf-8') as json_file:
                js.dump(name_parents, json_file, ensure_ascii=False)
else:
    np_document_embeddings = np.load("./../data/np_document_embeddings.npy")
    with open("./../data/name_parents.json", 'r', encoding='utf-8') as json_file:
        name_parents = js.load(json_file)

d = np_document_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np_document_embeddings)
print("Finished!")


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
    fps = 0
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


class FrameDocs:
    doc_list = []

    def __init__(self, doc_list) -> None:
        self.doc_list = doc_list.copy()

    def __call__(self):
        return self.doc_list.copy()

    """_summary_
    Get length
    """
    def __len__(self) -> int:
        return len(self.doc_list)
    
    """_summary_
        Filtering using objects and keywords
    """
    def contains(
        self, objects = None, keywords = None, search_mode=0
    ):
        keywords = [kw.lower() for kw in keywords]
        doc_list = self.doc_list.copy()
        
        # Filter by keyword in scripts
        if keywords:
            if search_mode == 0:
                # search with BERT
                search_str = " ".join(keywords)
                search_inputs = tokenizer(
                    search_str, return_tensors="pt", padding=True, truncation=True
                )
                search_inputs = {
                    key: value.to(device) for key, value in search_inputs.items()
                }  # Chuyển dữ liệu lên GPU
                with torch.no_grad():
                    search_outputs = model(**search_inputs)
                search_embedding = search_outputs.last_hidden_state.mean(dim=1)
                search = search_embedding.cpu().numpy()
                top_videos = []
                D, I = index.search(search, 100)  # search
                for i in I[0]:
                    top_videos.append(name_parents[i][:-4])
                top_videos = list(set(top_videos))
                for i in range(len(doc_list) - 1, -1, -1):
                    if doc_list[i].video_name not in top_videos:
                        doc_list.pop(i)
            else:
                for i in range(len(doc_list) - 1, -1, -1):
                    transcript_path = SCRIPT_PATH + doc_list[i].video_name + ".txt"
                    try:
                        with open(transcript_path, "r") as file:
                            content = file.read()
                            if not check_script(content, keywords):
                                doc_list.pop(i)
                    except FileNotFoundError:
                        pass
         # Filter by objects
        if objects:
            pass

        return FrameDocs(doc_list=doc_list)

    def predict(
        self, csv_name, objects = None, keywords = None, mode=0
    ):
        max_lines = 100
        keywords = [kw.lower() for kw in keywords]
        self = self.contains(objects=objects, keywords=keywords, search_mode=mode)
        with open(csv_name, "w") as f:
            for i in range(min(max_lines, len(self))):
                row_text = (
                    f"{self.doc_list[i].video_name}, {self.doc_list[i].actual_idx}\n"
                )
                f.write(row_text)

    def visualize(self):
        img_docs = [
            {
                "link": doc.metadata["watch_url"].split("v=")[-1],
                "path": doc.image_path,
                "video": doc.video_name,
                "frame": doc.actual_idx,
                "s": str(int(doc.actual_time) // 60)
                + "'"
                + str(round(doc.actual_time - 60 * (int(doc.actual_time) // 60), 1)),
            }
            for doc in self.doc_list
        ]

        display(HTML(create_html_script(img_docs)))


def get_all_docs(npy_files) -> FrameDocs:
    doc_list = []
    for feat_npy in npy_files:
        video_name = feat_npy[feat_npy.find("L") :].split(".")[0]
        feats_arr = np.load(os.path.join(feat_npy))
        # Load metadata
        metadata = {}
        with open(os.path.join(METADATA_PATH, video_name + ".json")) as meta_f:
            metadata = js.load(meta_f)
            map_kf = pd.read_csv(
                os.path.join(MAP_KEYFRAMES, video_name + ".csv"),
                usecols=["pts_time", "fps", "frame_idx"],
            )
            metadata = {key: metadata[key] for key in ["publish_date", "watch_url"]}
            for frame_idx, feat in enumerate(feats_arr):
                image_path = os.path.join(
                    KEYFRAME_PATH, video_name, f"{frame_idx + 1:04d}.jpg"
                )
                actual_idx = map_kf["frame_idx"][frame_idx]
                doc_list.append(
                    FrameDoc(
                        embedding=feat,
                        video_name=video_name,
                        image_path=image_path,
                        keyframe_id=frame_idx + 1,
                        actual_idx=actual_idx,
                        actual_time=map_kf["pts_time"][frame_idx],
                        fps=map_kf["fps"][frame_idx],
                        metadata=metadata,
                    )
                )

    return FrameDocs(doc_list)
