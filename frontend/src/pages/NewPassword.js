import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../styles/Newpass.css'

function NewPasswordPage() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { email } = location.state?location.state:{email: ''};

  useEffect(() => {
    if (!location.state || !location.state.hasOwnProperty('email')) {
      navigate('/forgotpassword');
    }
  }, [location, navigate]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    fetch('http://localhost:8000/userapp/api/user/changepwd/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, new_password: password })
    })
      .then(response => response.json())
      .then(data => {
        if (data.msg === 'Success') {
          navigate('/');
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
            <label class="titleB">New Password</label>
            <br/>
            <input class="emailbox" type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
            <br/>
            <br/>
            <label class="titleB">Re-Enter New Password</label>
            <br/>
            <input class="emailbox" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}/>
            <br/>
            <button class="submit" onClick={handleSubmit}>SUBMIT</button>
            <br/>
            {error && <p class="forgotperror">{error} !</p>}
        </div>
    </body>
  );
}

export { NewPasswordPage };
