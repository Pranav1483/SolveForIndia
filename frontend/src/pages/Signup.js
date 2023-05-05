import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Signup.css'

function SignupPage() {
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [mobile, setMobile] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    fetch('https://blockchain-qrdk.onrender.com/userapp/api/user/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username,
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
        mobile: mobile
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.msg === 'User Registered Successfully') {
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
    <div class="outer2">
      <label class="signupheading">SIGN UP</label>
      <br/><br/>
      <label class="signuplabel">Username</label>
      <br/>
      <input type="text" class="signuptext" value={username} onChange={(e) => setUsername(e.target.value)} />
      <br />
      <br/>
      <label class="signuplabel">First Name</label>
      <br/>
      <input type="text" class="signuptext" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
      <br />
      <br/>
      <label class="signuplabel">Last Name</label>
      <br/>
      <input type="text" class="signuptext" value={lastName} onChange={(e) => setLastName(e.target.value)} />
      <br />
      <br/>
      <label class="signuplabel">Email</label>
      <br/>
      <input type="email" class="signuptext" value={email} onChange={(e) => setEmail(e.target.value)} />
      <br />
      <br/>
      <label class="signuplabel">Password</label>
      <br/>
      <input type="password" class="signuptext" value={password} onChange={(e) => setPassword(e.target.value)} />
      <br />
      <br/>
      <label class="signuplabel">Confirm Password</label>
      <br/>
      <input type="password" class="signuptext" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
      <br />
      <br/>
      <label class="signuplabel">Mobile</label>
      <br/>
      <input type="text" class="signuptext" value={mobile} onChange={(e) => setMobile(e.target.value)} />
      <br />
      <br/>
      <button type="submit" class ="signupsubmit" onClick={handleSubmit}>Sign Up</button>
      {error && <p class="signuperror">{error} !</p>}
    </div>
  );
}

export { SignupPage };
