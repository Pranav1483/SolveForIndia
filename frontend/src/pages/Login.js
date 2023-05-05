import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Login.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if ((isLoggedIn != 'false') && (isLoggedIn))  {
      navigate({
        pathname: '/dashboard',
        state: { user: isLoggedIn }
      });
    }
  }, [navigate]);
  
  const handleSubmit = (event) => {
    event.preventDefault();
    fetch('https://blockchain-qrdk.onrender.com/userapp/api/user/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username, password: password })
    })
      .then(response => response.json())
      .then(data => {
    
        if (data.msg == 'Successful'){
          localStorage.setItem('isLoggedIn', data.username);
          navigate({
            pathname: '/dashboard',
            state: {user: data.username}
          });
        } else {
          setError(data.msg);
        }
      })
      .catch(error => {
        console.log(error);
        setError('Something went wrong. Please try again.');
      });
  }

  const handleSignUp = (event) => {
    event.preventDefault();
    navigate({
      pathname: '/signup'
    });
  }

  return (
    <body>
        <div class="box1">
            <label class="title1">LOGIN</label>
            <div class="box2">
                <label class="title2">Username</label>
                <input type="text" class="textbox" placeholder="&#xF007; User" value={username} onChange={(e) => setUsername(e.target.value)}/>
            </div>
            <br/>
            <div class="box2">
                <label class="title2">Password</label>
                <input type="password" class="textbox" placeholder="&#xF023; ****" value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>
            <a class="forgotpwd" href="/forgotpassword">Forgot Password</a>
            <div class="buttondiv">
                <button class="button1" onClick={handleSubmit}>LOGIN</button>
            </div>
            <div class="errordiv">
            {error && <p class="error">{error} !</p>}
            </div>
            <br/>
            <div class="buttondiv">
                <button class="button2" onClick={handleSignUp}>Sign Up</button>
            </div>
        </div>
    </body>
  );
}

export { LoginPage };
