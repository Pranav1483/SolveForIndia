import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import '../styles/Report.css'

function ReportPage() {
    const [error, setError] = useState('');
    const [loc, setLoc] = useState('');
    const [report, setReport] = useState('');
    const location = useLocation();
    const navigate = useNavigate();
    const { user } = location.state?location.state:{user: {username: ''}}

    useEffect( () => {
        if(user.username === ''){
            navigate('/dashboard');
        }
    })

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch('http://localhost:8000/userapp/api/user/report/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user.username, location: loc, report: report})
        })
            .then(response => response.json())
            .then(data => {
                if (data.msg === 'Report Successful'){
                    navigate('/dashboard');
                }
                else {
                    setError(data.msg);
                }
            })
            .catch(error => {
                console.log(error);
                setError('Something went Wrong, Please Try Again !');
            })
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
            <div class="reportbox">
                <label class="reportheading">REPORT</label>
                <label class="reportlabel">Location:</label>
                <input style={{height:'20px'}} class="reportinput" type="text" value={loc} onChange={(e) => setLoc(e.target.value)} />
                <br />
                <label class="reportlabel">Report:</label>
                <textarea style={{height:'100px'}}class="reportinput" type="text" value={report} onChange={(e) => setReport(e.target.value)} />
                <br />
                <button class="reportsubmit" type="submit" onClick={handleSubmit}>Submit</button>
                <br/>
                { error && <p class="reporterror">{ error } !</p>}
            </div>
        </body>
    )
    
}

export { ReportPage };