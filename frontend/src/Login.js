import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './styles/login.css'; // Make sure this path is correct

function Login() {
  // State for form fields
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  // State for loading and error messages
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Start loading
    setError('');     // Clear previous errors

    try {
      // API endpoint should ideally be in an environment variable
      const response = await axios.post('http://127.0.0.1:8000/auth/login/', formData);

      // Store tokens in localStorage
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);

      // Navigate to the dashboard on successful login
      navigate('/dashboard');

    } catch (err) {
      // Set a user-friendly error message
      if (err.response && err.response.status === 401) {
        setError('Invalid username or password. Please try again.');
      } else {
        setError('An unexpected error occurred. Please try again later.');
      }
      console.error('Login error:', err.response || err);
    } finally {
      setLoading(false); // Stop loading, regardless of outcome
    }
  };

  return (
    // This JSX structure now matches your CSS perfectly
    <div id="login-container">
      <div className="login-header">
        {/* You can place a logo image here */}
        {/* <img src="/path/to/logo.png" alt="Company Logo" className="logo" /> */}
        <h2>Welcome Back!</h2>
        <p className="subtitle">Please enter your details to sign in.</p>
      </div>

      <form id="login-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="username-input">Username</label>
          <input
            type="text"
            id="username-input" // ID for the label to connect to
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="e.g., john.doe"
            required
            disabled={loading} // Disable input when loading
          />
        </div>

        <div className="input-group">
          <label htmlFor="password-input">Password</label>
          <input
            type="password"
            id="password-input" // ID for the label to connect to
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Your password"
            required
            disabled={loading} // Disable input when loading
          />
        </div>

        {/* Display error message here instead of an alert */}
        {error && <p className="error-message">{error}</p>}

        <button type="submit" id="submit-button" disabled={loading}>
          {loading ? 'Signing In...' : 'Sign In'}
        </button>
      </form>
    </div>
  );
}

export default Login;