
from transformers import AutoTokenizer, AutoModel, RobertaConfig
import faiss
import re
from utils import  get_all_scripts
import torch
import numpy as np
from vector_database import FrameDoc
from utils import FrameDocToImage
import tqdm

SCRIPT_PATH = "../data/scripts/"
def check_script(file_content, keywords):
    for keyword in keywords:
        if (keyword not in file_content):
            return False
    return True

def filter_by_audio(result, keywords):
    for i in range(len(result) - 1, -1, -1):
        transcript_path = SCRIPT_PATH + result[i].video_name + ".txt"
        try:
            with open(transcript_path, 'r') as file:
                content = file.read()
                if (not check_script(content, keywords)):
                    result.pop(i)                 
        except FileNotFoundError:
            pass
    return result

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
model.to(device)
print("Finished!")

def separate_paragraphs(script, max_word=128):
    # Tách đoạn văn thành danh sách các từ
    words = re.findall(r'\b\w+\b', script)
    
    # Tính số lượng từ trong mỗi đoạn văn con
    n_child_script = len(words) // max_word
    
    # Tạo danh sách các đoạn văn con
    child_scripts = []
    for i in range(n_child_script):
        start = i * max_word
        end = (i + 1) * max_word
        if i == n_child_script - 1:
            # Trường hợp cuối cùng, lấy tất cả từ còn lại
            child_script = ' '.join(words[start:])
        else:
            child_script = ' '.join(words[start:end])
        child_scripts.append(child_script)
    
    return child_scripts


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
else:
    np_document_embeddings = np.load("./../data/np_document_embeddings.npy")

d = np_document_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np_document_embeddings)
print("Finished!")


def predict(keywords, results, csv_name, mode = 0):
    max_lines = 100
    top_videos = []
    keywords = [kw.lower() for kw in keywords]
    
    if mode == 0:
        search_str = " ".join(keywords)
        search_inputs = tokenizer(search_str, return_tensors="pt", padding=True, truncation=True)
        search_inputs = {key: value.to(device) for key, value in search_inputs.items()}  # Chuyển dữ liệu lên GPU
        with torch.no_grad():
            search_outputs = model(**search_inputs)
        search_embedding = search_outputs.last_hidden_state.mean(dim=1)
        search = search_embedding.cpu().numpy()
        
        # Lay 100 video
        k = 100
        D, I = index.search(search, k)  # search
        
        for i in I[0]:
            top_videos.append(name_parents[i][:-4])
        top_videos = list(set(top_videos))
        list_frame = FrameDocToImage(results)
        with open(csv_name, 'w') as f:
            for row in list_frame:
                video = row["video"]
                if max_lines == 0:
                    return
                elif len(csv_name) != 0 and video in top_videos:
                    row_text = f"{video}, {row['frame']}\n"
                    f.write(row_text)
                    max_lines -= 1
                elif len(csv_name) == 0:
                    row_text = f"{video}, {row['frame']}\n"
                    f.write(row_text)
                    max_lines -= 1
    else:
        results = filter_by_audio(result=results, keywords=keywords)
        with open(csv_name, 'w') as f:
            for row in results:
                if max_lines == 0:
                    return
                else:
                    row_text = f"{row.video_name}, {row.actual_idx}\n"
                    f.write(row_text)
                    max_lines -= 1

    

    