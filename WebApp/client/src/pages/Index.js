import classNames from 'classnames/bind';
import React, { useState, useEffect } from 'react';
import styles from '../styles/Index.module.css'
import Papa from "papaparse";
const cx = classNames.bind(styles);

// import img_0007 from '';

const Index = () => {
    const [allObjects, setAllObjects] = useState(false);
    const [detailObjects, setDetailObjects] = useState([]);
    const [checkedIds, setCheckedIds] = useState([]);
    const [minScore, setMinScore] = useState(40);
    const handleCheckboxChange = (id) => {
        if (checkedIds.includes(id)) {
            // If the ID is already in the checkedIds array, remove it
            setCheckedIds(checkedIds.filter((checkedId) => checkedId !== id));
        } else {
            // If the ID is not in the checkedIds array, add it
            setCheckedIds([...checkedIds, id]);
        }
    };
    const handleRangeChange = (e) => {
        // Update the range values in the state
        if (e.target.value >= 40) {
            setMinScore(e.target.value);
        }
    };

    const [searchQuery, setSearchQuery] = useState('');
    const [keyframes, setDetailKeyframes] = useState([]);
    const [loading, setLoading] = useState(true);

    // Load the JSON data (images) from your file
    useEffect(() => {
        // Define the API endpoint you want to call
        const apiUrl = 'http://127.0.0.1:5000/initial'; // Replace with your API endpoint

        // Make the API request
        fetch(apiUrl)
            .then((response) => response.json())
            .then((data) => {
                // Assuming the API response contains an array of image URLs
                setDetailKeyframes(data.detail_keyframes)
                setDetailObjects(data.objects)
                console.log(data.objects)
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
                setLoading(false);
            });
    }, []);

    // Filter images based on the search query
    const groupKeyframesIntoRows = (keyframes) => {
        const rows = [];
        for (let i = 0; i < keyframes.length; i += 3) {
            rows.push(keyframes.slice(i, i + 3));
        }
        return rows;
    };

    // Group the filtered images into rows
    const keyframeRows = groupKeyframesIntoRows(keyframes);

    return (
        <div className={cx("container")}>
            <div className={cx("sidebar")}>
                <label className={cx("checkbox")}>
                    <input
                        type="checkbox"
                        checked={allObjects}
                        onChange={() => setAllObjects(!allObjects)}
                    />
                    Show all objects
                </label>
                <label className={cx("score-box")}>
                    <input
                        type="range"
                        name="min"
                        value={minScore}
                        min={0}
                        max={100}
                        onChange={handleRangeChange}
                    />
                    <p>
                        Score: {minScore / 100}
                    </p>
                </label>
                <ul className={cx("detail-objects")}>
                    {detailObjects.map((item) => (
                        <li key={item.id} className={cx("detail-object")}>
                            <input
                                type="checkbox"
                                checked={checkedIds.includes(item[0])}
                                onChange={() => handleCheckboxChange(item[0])}
                            />
                            <p>{item[0]}</p>
                            <p>{item[1]}</p>
                        </li>
                    ))}
                </ul>
            </div>
            {loading ? (<p>Is Loading</p>) : (
                <div className={cx("main-box")}>
                    <div className={cx("search-box")}>
                        <input type="text" name="search" placeholder="Search..." className={cx("search-input")} />
                        <a className={cx("search-icon")}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                            </svg>
                        </a>
                    </div>

                    <div className={cx("keyframe-grid")}>
                        {keyframeRows.map((row, rowIndex) => (
                            <div className={cx("keyframe-row")} key={rowIndex}>
                                {row.map((keyframe, index) => (
                                    <div className={cx("keyframe-cell")} key={index}>
                                        <div className={cx("image-box")}>
                                            <img src={`http://127.0.0.1:5000/static/${keyframe['v']}/${keyframe["i"]}.jpg`} alt="My Image" />
                                            {allObjects ? (
                                                <div className={cx("bounding-boxes")}>
                                                    {keyframe["o"].map((box, boxIndex) => {

                                                        let score = minScore / 100
                                                        if (box["s"] >= score) {

                                                            if (checkedIds.length == 0 || checkedIds.includes(box["i"])){
                                                                // Image: 400 x 224
                                                                let ymin = box["b"][0] * 224;
                                                                let xmin = box["b"][1] * 400;
                                                                let ymax = box["b"][2] * 224;
                                                                let xmax = box["b"][3] * 400;

                                                                return (
                                                                    <div
                                                                        className={cx("bounding-box")}
                                                                        key={boxIndex}
                                                                        style={{
                                                                            left: xmin + 'px',
                                                                            top: ymin + 'px',
                                                                            width: (xmax - xmin) + 'px',
                                                                            height: (ymax - ymin) + 'px',
                                                                        }}
                                                                    >{
                                                                            console.log(box["box"])
                                                                        }</div>
                                                                )
                                                            }
                                                        }
                                                    })}
                                                </div>
                                            ) : (<div></div>)}
                                        </div>
                                        <div className={cx("keyframe-cell-info")}>
                                            <span>Keyframe: {keyframe["f"]}</span>
                                            <span>Time: {keyframe["t"]}s</span>
                                        </div>
                                        <a href={`https://www.youtube.com/watch?v=${keyframe["l"]}`} target="_blank">Xem chi tiết</a>
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Index