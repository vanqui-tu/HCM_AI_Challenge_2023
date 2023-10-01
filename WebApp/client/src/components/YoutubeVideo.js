import classNames from 'classnames/bind';
import styles from '../styles/YoutubeVideo.module.css'
import React, { Component, useState, useEffect } from 'react';
import YouTube from 'react-youtube';

const cx = classNames.bind(styles);
class YouTubePlayer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            currentTime: 0,
        };

        // YouTube video options
        this.opts = {
            height: '480',
            width: '720',
            playerVars: {
                // Add your YouTube API key here if not using environment variables
                // key: 'YOUR_API_KEY',
                // Other player options
                key: 'AIzaSyD2YYWQNQhpPRUdz7FoxLWGVP1wjJ2DXjQ'
            },
        };

        // Video ID and starting time
        this.videoId = props.videoId
        this.start = props.start;
        // Video name and st fps
        this.name = props.name
        this.fps = props.fps;
    }

    // Event handler for when the YouTube player is ready
    onReady(event) {
        // Get a reference to the YouTube player
        this.setState({ player: event.target });

        // Start the video at the specific time (e.g., 23.3 seconds)
        event.target.seekTo(this.start);

        // Start tracking the time periodically
        this.trackTime();
    }

    // Event handler for tracking current time
    onPlay() {
        // Use the YouTube Player API to get the current time
        const currentTime = this.state.player.getCurrentTime();

        // Update the currentTime state with the current time of the video
        this.setState({ currentTime });
    }

    // Periodically update the current time while the video is playing
    trackTime() {
        this.intervalId = setInterval(() => {
            this.onPlay();
        }, 100); // Update every 0.1 second
    }

    // Clear the interval when the component unmounts
    componentWillUnmount() {
        clearInterval(this.intervalId);
    }

    render() {
        return (

            <div className={cx('video-details-container')}>
                <div className={cx('video-container')}>
                    <YouTube
                        videoId={this.videoId}
                        opts={this.opts}
                        onReady={(e) => this.onReady(e)}
                        onPlay={(e) => this.onPlay(e)} // Set the onPlay event handler for tracking time
                    />
                </div>
                <div className={cx('video-details')}>
                    <div className={cx('video-name')}>{(this.name)}</div>
                    <div className={cx('video-time')}>Current time: <span>{Number(this.state.currentTime).toFixed(2)}s</span></div>
                    <div className={cx('video-time')}>Current frame: <span>{Number(Number(this.state.currentTime) * this.fps).toFixed()}</span></div>
                </div>
            </div>
        );
    }
}

export default YouTubePlayer;
