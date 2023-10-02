import classNames from 'classnames/bind';
import React, { useState, useEffect } from 'react';
import styles from '../styles/Index.module.css'
import io from 'socket.io-client';
// import Papa from "papaparse";
const cx = classNames.bind(styles);

// import img_0007 from '';

const Index = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [keyframes, setDetailKeyframes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [allObjects, setAllObjects] = useState(false);
    const [detailObjects, setDetailObjects] = useState([]);
    const [filterObjects, setFilterObjects] = useState([])
    const [checkedIds, setCheckedIds] = useState([]);
    const [minScore, setMinScore] = useState(40);

    // TODO: Khởi tạo các tài nguyên mặc định cho UI
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
                setFilterObjects(data.objects)
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
                setLoading(false);
            });
    }, []);

    // TODO: Tạo 1 connect qua giao thức socket
    useEffect(() => {
        const socket = io('http://localhost:5000');
        socket.on('connect', () => {
            console.log("Connected to server");
        });

        return () => {
            socket.disconnect();
        };
    }, []);

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

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        console.log('Form submitted with searchQuery:', searchQuery);
        try {
            const socket = io('http://localhost:5000');
            socket.emit('search', { searchQuery });

            socket.on('search_result', (data) => {
                setDetailKeyframes(data.data)
                setLoading(false);
            });

            socket.on('search_error', (error) => {
                console.error('Server error:', error);
                setLoading(false);
            });

        } catch (error) {
            console.error('Error:', error);
        }
    };


    useEffect(() => {

    }, [filterObjects, setFilterObjects])

    return (
        <div className={cx("container")}>
            <div className={cx("sidebar")}>
                <label className={cx("checkbox")} for="allObjects">
                    <input
                        id="allObjects"
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
                <div className={cx('object-container')}>
                    <input type="text" placeholder='Search object...' onChange={(event) => {
                        console.log(event.target.value)

                        setFilterObjects(detailObjects.filter((value) => {
                            return value[0].toString().includes(event.target.value) || value[1].toString().includes(event.target.value);
                        }))
                    }} />
                    <ul className={cx("detail-objects")}>

                        {filterObjects.map((item, idx) => (
                            <li key={item.id} className={cx("detail-object")}>
                                <input
                                    type="checkbox"
                                    checked={checkedIds.includes(item[0])}
                                    name={idx}
                                    id={idx}
                                    onChange={() => handleCheckboxChange(item[0])}
                                />
                                <label for={idx}>
                                    <div>{item[0]}</div>
                                    <div>{item[1]}</div>
                                </label>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            {loading ? (<p>Is Loading</p>) : (
                <div className={cx("main-box")}>
                    <form className={cx("search-box")} onSubmit={handleFormSubmit}>
                        <input type="text" name="search" placeholder="Search..." className={cx("search-input")} value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
                        <a className={cx("search-icon")} onClick={handleFormSubmit}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                            </svg>
                        </a>
                    </form>

                    <div className={cx("keyframe-grid")}>
                        {keyframes.map((keyframe, idx) => (
                            <div className={cx("keyframe-container")} key={idx}>
                                <div className={cx("image-box")}>
                                    <img src={`http://127.0.0.1:5000/static/${keyframe['v']}/${keyframe["i"]}.jpg`} alt="My Image" />
                                    <div className={cx("bounding-boxes")}>
                                        {allObjects ? (
                                            <div className={cx("bounding-boxes")}>
                                                {keyframe["o"].map((box, boxIndex) => {

                                                    let score = minScore / 100
                                                    if (box["s"] >= score) {

                                                        if (checkedIds.length == 0 || checkedIds.includes(box["i"])) {
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
                                                                ></div>
                                                            )
                                                        }
                                                    }
                                                })}
                                            </div>
                                        ) : (<div></div>)}
                                    </div>
                                </div>
                                <div className={cx("keyframe-info")}>
                                    <span>Video: {keyframe["v"]}</span>
                                    <span>Keyframe: {keyframe["f"]}</span>
                                    <span>Time: {keyframe["t"]}s</span>
                                </div>
                                <a href={`/videos?videoId=${keyframe["l"]}&frameIdx=${keyframe["f"]}&start=${keyframe["t"]}&fps=${keyframe['fps'] === undefined ? 25 : keyframe["fps"]}&name=${keyframe["v"]}`} target="_blank">Xem chi tiết</a>
                            </div>
                        ))}
                    </div >
                </div>
            )}
        </div>
    );
}

export default Index