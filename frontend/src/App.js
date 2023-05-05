import logo from './logo.svg';
import './App.css';
import { LoginPage } from './pages/Login.js'
import { Dashboard } from './pages/Dashboard.js'
import { SignupPage } from './pages/Signup';
import { ForgotPasswordPage } from './pages/ForgotPassword';
import { OtpPage } from './pages/VerifyOtp';
import { NewPasswordPage } from './pages/NewPassword';
import { QRCodePage } from './pages/AddProduct';
import { ReportPage } from './pages/Report';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"

function App() {
  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/forgotpassword" element={<ForgotPasswordPage/>} />
          <Route path="/otp" element={<OtpPage/>} />
          <Route path="/newpassword" element={<NewPasswordPage/>} />
          <Route path="/addproduct" element={<QRCodePage/>} />
          <Route path="/report" element={<ReportPage/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
