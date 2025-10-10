import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import Campaigns from './Campaigns';
import InfluencerProfile from './InfluencerProfile'; // Yeh import bilkul sahi hai

// Aapka PrivateRoute function bilkul sahi hai
function PrivateRoute({ children }) {
  const token = localStorage.getItem('accessToken');
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <Router>
      <div className="App">
        {/* Humne <header> ko Routes se bahar nikal diya hai taaki
            agar aap future mein Navbar banayein, toh woh har page par dikhe. */}
        
        <Routes>
          {/* ============== PUBLIC ROUTES ============== */}
          {/* Yeh routes koi bhi dekh sakta hai */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* ============== PRIVATE ROUTES ============== */}
          {/* Humne in routes ko PrivateRoute se protect kar diya hai */}
          <Route 
            path="/dashboard" 
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/campaigns" 
            element={
              <PrivateRoute>
                <Campaigns />
              </PrivateRoute>
            } 
          />
          
          {/* --- YAHAN NAYA ROUTE JODA GAYA HAI --- */}
          {/* Yeh niyam batata hai ki /influencer/:ID waale URL par kya dikhana hai */}
          <Route 
            path="/influencer/:influencerId" 
            element={
              <PrivateRoute>
                <InfluencerProfile />
              </PrivateRoute>
            } 
          />

          {/* Fallback Route: Agar koi galat URL daala jaaye, toh use dashboard par bhej do */}
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;