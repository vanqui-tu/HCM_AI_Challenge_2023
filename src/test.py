import os
import json
import csv
from tqdm import tqdm

def get_detail_frames():
    list_dataset = []
    list_folder = os.listdir("./../data/keyframes")
    for _, folder in enumerate(tqdm(list_folder)):
        if folder == ".gitkeep":
            continue

        # TODO: Read map_keyframe
        map_keyframe = []
        with open(f"./../data/map-keyframes/{folder}.csv", 'r', newline="") as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)

            for row in csv_reader:
                map_keyframe.append(row)
        file.close()

        folder_path = os.path.join("./../data/keyframes", folder)
        list_keyframes = os.listdir(folder_path)

        for idx, frame in enumerate(list_keyframes):
            frame_path = os.path.join(folder_path, frame)

            # TODO Get object of frame if confidence > 0.4
            obj_path = frame_path.replace("keyframes", "objects")
            obj_path = obj_path.replace("jpg", "json")
            with open(f"./../data/objects/{folder}/{frame[:-4]}.json", 'r') as file:
                objects_data = json.load(file)
            file.close()    
            detection_class_labels = objects_data["detection_class_labels"]
            detection_scores = objects_data["detection_scores"]
            detection_class_entities = objects_data["detection_class_entities"]
            detection_boxes = objects_data["detection_boxes"]
            objects_data.clear()
            objects = []
            for i, score in enumerate(detection_scores):
                if float(score) < 0.4:
                    continue
                objects.append({
                    "score": score,
                    "class_id": detection_class_labels[i],
                    "class_name": detection_class_entities[i],
                    "box": detection_boxes[i],
                })    

            obj_frame = {
                "file_path": frame_path,
                "frame_id": frame[:-4],
                "time": map_keyframe[idx][1],
                "frame": map_keyframe[idx][3],
                "objects": objects
            }
            list_dataset.append(obj_frame)
    
    with open("./test.json", "w") as json_file:
        json.dump(list_dataset, json_file)

if __name__ == "__main__":
    with open("./test.json", "r") as json_file:
        dataset_dict = json.load(json_file)

    print(dataset_dict[0])