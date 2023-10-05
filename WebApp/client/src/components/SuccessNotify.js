import Toast from 'react-bootstrap/Toast';
import { useState } from 'react';

function SuccessNotify({success = true}) {
  const [showA, setShowA] = useState(true);
  const toggleShowA = () => setShowA(!showA);

  return (
    <Toast show={showA} onClose={toggleShowA}  bg={success? "success":"danger"} className="d-inline-block m-1">
    <Toast.Header >
      <img
        src="holder.js/20x20?text=%20"
        className="rounded me-2"
       
        alt=""
      />
      <h2 className="me-auto text-black"> Session ID Status</h2>
    </Toast.Header>
    <Toast.Body><h3>{success?"Successful!":"Failed!"}</h3></Toast.Body>
  </Toast>
  );
}

export default SuccessNotify;