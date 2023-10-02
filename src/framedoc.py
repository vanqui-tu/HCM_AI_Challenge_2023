from const import *
import numpy as np
from docarray import DocList, BaseDoc
from docarray.typing import NdArray
import clip
from utils import (
    check_script,
    create_html_script,
    reformat_keyframe,
    reformat_object
)
import json as js
import pandas as pd
import os
from IPython.display import display, HTML
from tqdm import tqdm

reformat_keyframe()
reformat_object()

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
    object_labels = []
    link = ""
    id_frame=""

    def __str__(self):
        return f"""
            Video name: {self.video_name}
            Image path: {self.image_path}
            Keyframe Id: {self.id_frame}
            Actual keyframe idx: {self.actual_idx}
            Time: {self.actual_time}
            FPS: {self.fps}
            Metadata: {self.metadata}
            Object Labels: {self.object_labels}
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
        self, keywords = None
    ):
       
        doc_list = self.doc_list.copy()
        
        # Filter by keyword in scripts
        if keywords:
            keywords = [kw.lower() for kw in keywords]
            for i in range(len(doc_list) - 1, -1, -1):
                transcript_path = SCRIPT_PATH + doc_list[i].video_name + ".txt"
                try:
                    with open(transcript_path, "r") as file:
                        content = file.read()
                        if not check_script(content, keywords):
                            doc_list.pop(i)
                except FileNotFoundError:
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

    def to_json(self):
        json_frame = [
            {
                "l": doc.link,
                "v": doc.video_name,
                "i": doc.id_frame,
                "f": doc.actual_idx,
                "t": doc.actual_time,
                "o": doc.object_labels,
            }
            for doc in self.doc_list
        ]

        return json_frame

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
    for feat_npy in tqdm(iterable=npy_files, ascii=True, desc="Loading FrameDocs"):
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

def get_all_docs_v2() -> FrameDocs:
    doc_list = []
    with open("../data/detail_keyframes.json", "r") as json_file:
        detail_keyframes = js.load(json_file)
    json_file.close()
    start_video = "L01_V001"
    features_frames = np.load("../data/features/" + start_video + ".npy")
    for idx, keyframe in enumerate(tqdm(detail_keyframes)):
        if keyframe["v"] != start_video:
            start_video = keyframe["v"]
            features_frames = np.load("../data/features/" + start_video + ".npy")
        id_frame = keyframe["i"]
        print(id_frame)
        id =  int(keyframe["i"].lstrip('0'))
        doc_list.append(
            FrameDoc(
                embedding=features_frames[id - 1],
                link=keyframe["l"],
                video_name=keyframe["v"],
                id_frame=str(id_frame),
                actual_idx=keyframe["f"],
                actual_time=keyframe["t"],
                object_labels=keyframe["o"],
            )
        )
    detail_keyframes.clear()
    return FrameDocs(doc_list)
