import CToast from 'react-bootstrap/Toast';
import React, { useState } from 'react';
import classNames from 'classnames/bind';
import styles from '../styles/Notification.module.css';
const cx = classNames.bind(styles);

function SuccessNotify({ success = true, title = "Session ID Status", text = null, autohide = true }) {
  const [showA, setShowA] = useState(true);
  const toggleShowA = () => setShowA(!showA);

  return (
    <div className={cx('notify-container')}>
      <CToast placement="center" animation={true} autohide={autohide} show={showA} onClose={toggleShowA} bg={success ? "success" : "danger"} className="d-inline-block m-1">
        <CToast.Header>
          <h2 className="fw-bold me-auto text-black">{title}</h2>

        </CToast.Header>
        <CToast.Body><h3>{text === null ? success ? "Successful!" : "Failed!" : text}</h3></CToast.Body>
      </CToast>
    </div>
  );
}

export default SuccessNotify;