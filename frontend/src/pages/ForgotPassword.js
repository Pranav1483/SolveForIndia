import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Forgotpass.css';

function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const otp = Math.floor(Math.random() * 900000) + 100000;
  const navigate = useNavigate();

  const handleEmailSubmit = (event) => {
    event.preventDefault();
    fetch('https://blockchain-qrdk.onrender.com/userapp/api/user/sendotp/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, otp: otp.toString() })
    })
      .then(response => response.json())
      .then(data => {
        if (data.msg === 'Successful'){
          navigate('/otp', { state: { email: email, otp: otp.toString() } });
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
            <label class="titleB">Email</label>
            <br/>
            <input class="emailbox" type="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
            <br/>
            <button class="submit" onClick={handleEmailSubmit}>SUBMIT</button>
            <br/>
            {error && <p class="forgotperror">{error} !</p>}
        </div>
    </body>
  );
}

export { ForgotPasswordPage };
