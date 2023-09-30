import React, { useState } from 'react';
import classNames from 'classnames/bind';
import styles from './Sidebar.module.scss';

// import config from './config';

const cx = classNames.bind(styles);

function Sidebar() {
    // Initialize state for the checkboxes
    const [checkbox1, setCheckbox1] = useState(false);
    const [checkbox2, setCheckbox2] = useState(false);
    const [checkbox3, setCheckbox3] = useState(false);

    // Handle checkbox state changes
    const handleCheckboxChange = (checkboxNumber) => {
        switch (checkboxNumber) {
            case 1:
                setCheckbox1(!checkbox1);
                break;
            case 2:
                setCheckbox2(!checkbox2);
                break;
            case 3:
                setCheckbox3(!checkbox3);
                break;
            default:
                break;
        }
    };

    return (
        <div className="sidebar">
            <div className={cx("container")}>
                <label className={cx("checkbox")}>
                    <input
                        type="checkbox"
                        checked={checkbox1}
                        onChange={() => handleCheckboxChange(1)}
                    />
                    Checkbox 1
                </label>
                <label className={cx("checkbox")}>
                    <input
                        type="checkbox"
                        checked={checkbox2}
                        onChange={() => handleCheckboxChange(2)}
                    />
                    Checkbox 2
                </label>
                <label className={cx("checkbox")}>
                    <input
                        type="checkbox"
                        checked={checkbox3}
                        onChange={() => handleCheckboxChange(3)}
                    />
                    Checkbox 3
                </label>
            </div>
        </div>
    );
}

export default Sidebar;
