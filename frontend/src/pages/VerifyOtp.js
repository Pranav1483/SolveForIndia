import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/Otppage.css'

function OtpPage() {
  const [entered_otp, setEntered_otp] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { email, otp } = location.state?location.state:{email:'', otp:''};
  useEffect(() => {
    if (!location.state || !location.state.hasOwnProperty('email') || !location.state.hasOwnProperty('otp')) {
      navigate('/forgotpassword');
    }
  }, [location, navigate]);
  
  const handleSubmit = (event) => {
    event.preventDefault();
    fetch('http://localhost:8000/userapp/api/user/verifyotp/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ otp: otp, otp_from_user: entered_otp })
    })
      .then(response => response.json())
      .then(data => {
        if (data.msg === 'Success'){
          navigate('/newpassword', { state: { email: email } });
        } else {
          setError(data.msg);
        }
      })
      .catch(error => {
        console.log(error);
        setError('Something went wrong. Please try again.');
      });
  }

  return (
    <body>
        <div class="box1">
            <label class="titleA">RESET PASSWORD</label>
            <br/>
            <label class="titleB">OTP</label>
            <br/>
            <input class="emailbox" type="email" value={entered_otp} onChange={(e) => setEntered_otp(e.target.value)}/>
            <br/>
            <button class="submit" onClick={handleSubmit}>SUBMIT</button>
            <br/>
            {error && <p class="forgotperror">{error} !</p>}
        </div>
    </body>
  );
}

export { OtpPage };
