import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css'


function Dashboard(props) {
    const [obj, setObj] = useState(false);
    const history = useNavigate();

    const handleLogout = () => {
      localStorage.setItem('isLoggedIn', 'false');
      history('/');
    }

    const handleAddProduct = () => {
      history('/addproduct', { state: {user: obj}});
    }

    const handleAddReport = () => {
      history('/report', { state: {user: obj}});
    }

    const handleDashboard = () => {
      history('/dashboard');
    }

    useEffect(() => {
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        if ((isLoggedIn == 'false') || (!isLoggedIn)) {
          history({
            pathname: '/'
          });
        }
        fetch('https://blockchain-qrdk.onrender.com/userapp/api/user/' + localStorage.getItem('isLoggedIn'))
          .then(response => response.json())
          .then(data => {
            setObj(data);
          })
          .catch(error => {
            localStorage.setItem('isLoggedIn', 'false');
            history({
              pathname: '/'
            });
          });
      }, [history]);
      if(obj.msg == 'No User Found'){
        localStorage.setItem('isLoggedIn', 'false');
        history({
          pathname: '/'
        });
      }
      if (!obj) {
        return <div class="loader"></div>;
      }
      const products = Object.values(obj.products);
      return (
        <body>
          <div class="sidebox">
              <div class="userimage"></div>
              <label class="username">@{obj.username}</label>
              <div class="innerbox">
                  <div class="idimg"></div>
                  <label class="idlabel">Name:</label>
                  <label class="idlabel">{obj.first_name} {obj.last_name}</label>
                  <br/>
                  <label class="idlabel">Email:</label>
                  <label class="idlabel">{obj.email}</label>
                  <br/>
                  <label class="idlabel">Mobile:</label>
                  <label class="idlabel">{obj.mobile}</label>
              </div>
              <button class="btn" onClick={handleDashboard}>DASHBOARD</button>
              <br/>
              <button class="btn" onClick={handleAddProduct}>ADD PRODUCT</button>
              <br/>
              <button class="btn" onClick={handleAddReport}>REPORT</button>
              <br/>
              <button class="btn" onClick={handleLogout}>LOGOUT</button>
          </div>
          <div class="main">
              <table rules="none">
                  <thead>
                      <tr class="headerrow">
                          <th style={{borderTopLeftRadius: '20px', borderRight: '0px'}}>ITEM</th>
                          <th style={{borderLeft: '0px', borderRight: '0px'}}>SIZE</th>
                          <th style={{borderLeft: '0px', borderRight: '0px'}}>COLOUR</th>
                          <th style={{borderTopRightRadius: '20px', borderLeft: '0px'}}>MANUFACTURED</th>
                      </tr>
                  </thead>
                  <tbody>
                    {products.map((product, index) => (
                      <tr key={index}>
                        <td>{product.product_details.Item}</td>
                        <td>{product.product_details.Size}</td>
                        <td>{product.product_details.Colour}</td>
                        <td>{product.timestamp}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                      <td class="footrow" style={{borderBottomLeftRadius: '20px', borderRight: '0px'}}></td>
                      <td class="footrow" style={{borderLeft: '0px', borderRight: '0px'}}></td>
                      <td class="footrow" style={{borderLeft: '0px', borderRight: '0px'}}></td>
                      <td class="footrow" style={{borderBottomRightRadius: '20px', borderLeft: '0px'}}></td>
                  </tfoot>
              </table>
          </div>
        </body>
      )
}


export { Dashboard };