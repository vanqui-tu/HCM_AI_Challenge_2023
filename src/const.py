import torch
MODEL = "ViT-B/32"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

METADATA_PATH = "../data/metadata/"
KEYFRAME_PATH = "../data/keyframes/"
FEATURE_PATH = "../data/features/"
MAP_KEYFRAMES = "../data/map-keyframes/"
VIDEOS_PATH = "../data/videos/"
SCRIPT_PATH = "../data/scripts/"
OBJECT_PATH = "../data/objects/"

WORKSPACE = "./vectordb"
LEN_OF_KEYFRAME_NAME = 4