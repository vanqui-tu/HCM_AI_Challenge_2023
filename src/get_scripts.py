import os
import json
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi

METADATA_PATH = "../data/metadata"
NO_SCRIPT_PATH = "../data/scripts/no_scripts.txt"

get_times = True

if __name__ == "__main__":
    metadata_list = os.listdir(METADATA_PATH)
    no_script_list = ''
    for idx, file in enumerate(tqdm(metadata_list)):
        if ".json" not in file:
            continue
        file_path = os.path.join(METADATA_PATH, file)
        with open(file_path, encoding="utf-8", errors='ignore') as f:
            file_data = json.load(f)
        f.close()
        
        id_video = file_data['watch_url'].split('=')[1]
        try:
            script = YouTubeTranscriptApi.get_transcript(id_video, languages=['vi'])
        except:
            script = None

        if script == None:
            file = file.replace('.json', '')
            no_script_list = no_script_list + '\n' + file if no_script_list != '' else file
            continue
        
        text_path = file_path.replace('metadata', 'scripts')

        if get_times:
            with open(text_path, 'w', encoding='utf-8') as json_file:
                for line in script:
                    line['text'] = line['text'].lower()
                json.dump(script, json_file, ensure_ascii=False)

            # with open(text_path, 'r', encoding='utf-8') as json_file:
            #     extracted_data = json.load(json_file)
        else:
            text = ''
            for line in script:
                text = text + ' ' + line['text']
            text = text.strip()

            text_path = text_path.replace('json', 'txt')
            with open(text_path, 'w', encoding="utf-8", errors='ignore') as f:
                f.write(text.lower())
            f.close()
        with open(NO_SCRIPT_PATH, 'w', encoding="utf-8", errors='ignore') as f:
            f.write(no_script_list)
        f.close()

