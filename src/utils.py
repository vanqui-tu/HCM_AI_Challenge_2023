import os
import numpy as np

def create_html_script(images):
    styles = """
        <style>
            .image-list {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                grid-gap: 10px;
                max-height: 900px;
                overflow-y: scroll;
            }

            .image-item {
                position: relative;
            }

            .image-item img {
                max-width: 100%;
                height: auto;
                cursor: pointer;
            }

            .image-item a {
                display: none;
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.7);
                text-align: center;
                justify-content: center;
                align-items: center;
                text-decoration: none;
                color: white;
            }

            .image-item:hover a {
                display: flex;
            }
        </style>
    """

    script_js = """
        <script>
            function openLink(url) {
                window.open(url, '_blank');
            }
        </script>
    """

    div_childs = ""

    for image in images:
        link = f"http://www.watchframebyframe.com/watch/yt/{image['link']}"
        div_child = f"""
            <div class="image-item">
                <img src="{image['path']}" alt="Ảnh 1">
                <figcaption>{image['video']} - {image['frame']} - {image['s']}</figcaption>            
                <a href={link} target="_blank">Xem chi tiết</a>
            </div>
        """
        div_childs += div_child
    
    html_script = f"""
        {styles}
       <div class="image-list">
            {div_childs}
        </div>
        {script_js}
    """

    return html_script

def remove_stopwords(doc, stopwords):
    words = doc.split()

    # Lọc bỏ các stopwords
    filtered_words = [word for word in words if word not in stopwords]

    # Kết hợp các từ lại thành một đoạn văn
    filtered_doc = ' '.join(filtered_words)

    return filtered_doc

def get_all_scripts():
    # Get list stopword
    with open("./stopwords.txt", 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()

    path = "../data/scripts"
    list_script = os.listdir(path)
    all_scripts = []
    list_file = []
    for script in list_script:
        if not ".txt" in script:
             continue
        list_file.append(script)
        script_path = os.path.join(path, script)
        with open(script_path, 'r') as file:
                content = file.read()
                all_scripts.append(remove_stopwords(content, stopwords))
    
    return list_file, all_scripts

if __name__ == "__main__":
    get_all_scripts()