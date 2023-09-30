import React from 'react'
import classNames from 'classnames/bind';
import styles from '../styles/VideoDetails.module.css'
const cx = classNames.bind(styles);

const VideoDetails = () => {
    return (
        <div className={cx('main')}>
            Video details
        </div>
    )
}

export default VideoDetails