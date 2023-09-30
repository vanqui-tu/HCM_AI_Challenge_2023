import classNames from 'classnames/bind';
import React, { useState, useEffect } from 'react';
import styles from '../styles/Index.module.css'
import Sidebar from '../components/Sidebar'
const cx = classNames.bind(styles);

// import img_0007 from '';

const Index = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [keyframes, setDetailKeyframes] = useState([]);
    const [loading, setLoading] = useState(true);

    // Load the JSON data (images) from your file
    useEffect(() => {
        // Define the API endpoint you want to call
        const apiUrl = 'http://127.0.0.1:5000/example'; // Replace with your API endpoint

        // Make the API request
        fetch(apiUrl)
            .then((response) => response.json())
            .then((data) => {
                // Assuming the API response contains an array of image URLs
                setDetailKeyframes(data.data)
                console.log(data.data)
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
    // const keyframeRows = groupKeyframesIntoRows(keyframes);

    return (
        <div className={cx("container")}>
            {loading ? (<p>Is Loading</p>) : (
                <div>
                    <div className={cx("search-box")}>
                        <input type="text" name="search" placeholder="Search..." className={cx("search-input")} />
                        <a className={cx("search-icon")}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                            </svg>
                        </a>
                    </div>
                    <div className={cx("keyframe-grid")}>
                        {keyframes.map((keyframe, idx) => (
                            <div className={cx("keyframe-container")} key={idx}>
                                <div className={cx("image-box")}>
                                    <img src={'/0001.jpg'} alt="My Image" />
                                    <div className={cx("bounding-boxes")}>
                                        {keyframe["o"].map((box, boxIndex) => {
                                            let width = 400;
                                            let height = 224;
                                            // Image: 400 x 224
                                            let ymin = box["b"][0] * height;
                                            let xmin = box["b"][1] * width;
                                            let ymax = box["b"][2] * height;
                                            let xmax = box["b"][3] * width;

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
                                        })}
                                    </div>
                                </div>
                                <div className={cx("keyframe-info")}>
                                    <span>Keyframe: {keyframe["f"]}</span>
                                    <span>Time: {keyframe["t"]}s</span>
                                </div>
                                <a href={`/videos/${keyframe["l"]}?idx=${123123}&t=${keyframe["t"]}`} target="_blank">Xem chi tiết</a>
                            </div>
                        ))}
                    </div >

                    {/* <div className={cx("keyframe-grid")}>
                        {keyframeRows.map((row, rowIndex) => (
                            <div className={cx("keyframe-row")} key={rowIndex}>
                                {row.map((keyframe, index) => (
                                    <div className={cx("keyframe-cell")} key={index}>
                                        <div className={cx("image-box")}>
                                            <img src={'/0001.jpg'} alt="My Image" />
                                            <div className={cx("bounding-boxes")}>
                                                {keyframe["o"].map((box, boxIndex) => {
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
                                                })}
                                            </div>
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
                    </div> */}
                </div>
            )}
        </div>
    );
}

export default Index