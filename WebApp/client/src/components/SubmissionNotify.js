import React from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function SubmissionNotify({ text }) {
    const notify = () => toast(text);
    notify();
    return (
        <ToastContainer
            position="top-right"
            autoClose={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss={false}
            draggable={false}
            theme="dark"
        />
    );
}

export default SubmissionNotify;