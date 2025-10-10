import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div>
      <h1>Welcome to the Influencer Platform</h1>
      <nav>
        <Link to="/login" style={{ marginRight: '10px' }}>Login</Link>
        <Link to="/register">Register</Link>
      </nav>
    </div>
  );
}

export default Home;