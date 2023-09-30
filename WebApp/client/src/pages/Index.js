import classNames from 'classnames/bind';
import React, { useState, useEffect } from 'react';
import styles from '../styles/Index.module.css'
import Sidebar from '../components/Sidebar'
const cx = classNames.bind(styles);

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
        <div className={cx('main')}>
            <Sidebar />
            <div className={cx('content')}>
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
                                {keyframeRows.map((row, rowIndex) => (
                                    <div className={cx("keyframe-row")} key={rowIndex}>
                                        {row.map((keyframe, index) => (
                                            <div className={cx("keyframe-cell")} key={index}>
                                                <div>
                                                    <img src="https://i.ytimg.com/vi/HNsRpkryGXA/hqdefault.jpg?sqp=-oaymwEXCJADEOABSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDT_1e4WaAw3ZFe1c31UF2n23_5Kw"></img>
                                                    <div className={cx("bounding-boxes")}>
                                                        {keyframe.objects.map((box, boxIndex) => {
                                                            // Image: 400 x 224
                                                            let ymin = box["box"][0] * 224;
                                                            let xmin = box["box"][1] * 400;
                                                            let ymax = box["box"][2] * 224;
                                                            let xmax = box["box"][3] * 400;

                                                            return (
                                                                <div
                                                                    className={cx("bounding-box")}
                                                                    key={boxIndex}
                                                                    style={{
                                                                        left: ymin + 'px',
                                                                        top: xmin + 'px',
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
                                                    <span>Keyframe: {keyframe["frame"]}</span>
                                                    <span>Time: {keyframe["time"]}s</span>
                                                </div>
                                                <a href="fb.com" target="_blank">Xem chi tiết</a>
                                            </div>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Index