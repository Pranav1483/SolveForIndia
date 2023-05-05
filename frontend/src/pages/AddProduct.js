import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import jsQR from 'jsqr';
import '../styles/Addproduct.css'

function QRCodePage() {
  const [image, setImage] = useState(null);
  const [error, setError] = useState('');
  const [dataURL, setDataURL] = useState(false);
  const [qrCodeData, setQRCodeData] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = location.state?location.state:{user: {username: ''}}
  useEffect( () => {
    if (user.username === ''){
        navigate('/dashboard');
    }
  })

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch('http://localhost:8000/userapp/api/user/addpdt/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user.username, hash: qrCodeData })
    })
      .then(response => response.json())
      .then(data => {
        if (data.msg === 'Product Added Successfully'){
          navigate('/dashboard');
        } else {
          setError(data.msg);
        }
      })
      .catch(error => {
        console.log(error);
        setError('Something went wrong. Please try again.');
      });
  }

  const handleLogout = () => {
    localStorage.setItem('isLoggedIn', 'false');
    navigate('/');
  }

  const handleAddProduct = () => {
    navigate('/addproduct', { state: {user: user}});
  }

  const handleAddReport = () => {
    navigate('/report', { state: {user: user}});
  }

  const handleDashboard = () => {
    navigate('/dashboard');
  }

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      const image = new Image();
      image.src = event.target.result;
      image.onload = () => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = image.width;
        canvas.height = image.height;
        context.drawImage(image, 0, 0, image.width, image.height);
        setDataURL(canvas.toDataURL());
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        if (code) {
          setQRCodeData(code.data);
        } else {
          setQRCodeData('No QR code found.');
        }
      };
    };
    reader.readAsDataURL(file);
  };

  return (
    <body>
      <div class="sidebox">
              <div class="userimage"></div>
              <label class="username">@{user.username}</label>
              <div class="innerbox">
                  <div class="idimg"></div>
                  <label class="idlabel">Name:</label>
                  <label class="idlabel">{user.first_name} {user.last_name}</label>
                  <br/>
                  <label class="idlabel">Email:</label>
                  <label class="idlabel">{user.email}</label>
                  <br/>
                  <label class="idlabel">Mobile:</label>
                  <label class="idlabel">{user.mobile}</label>
              </div>
              <button class="btn" onClick={handleDashboard}>DASHBOARD</button>
              <br/>
              <button class="btn" onClick={handleAddProduct}>ADD PRODUCT</button>
              <br/>
              <button class="btn" onClick={handleAddReport}>REPORT</button>
              <br/>
              <button class="btn" onClick={handleLogout}>LOGOUT</button>
          </div>
      <div class="addpdtbox">
        <label class="addpdttitle">Upload QR Code</label>
        <br/>
        <div class="addpdtinnerbox" style={{backgroundImage: `url(${dataURL})`}}></div>
        <input class="addpdtinput" type="file" accept="image/*" onChange={handleImageUpload} />
        <br />
        <button type="submit" class="addpdtsubmit" onClick={handleSubmit}>Submit</button>
        {error && <p class="addpdterror">{ error } !</p>}
      </div>
      </body>
  );
}

export { QRCodePage };
