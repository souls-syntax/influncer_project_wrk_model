import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './styles/register.css'; // We will create this new CSS file

function Register() {
  // State for form fields
  const [formData, setFormData] = useState({
    username: '',
    email: '',
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
    setLoading(true);
    setError('');

    try {
      await axios.post('http://127.0.0.1:8000/auth/register/', formData);
      
      // On success, navigate to the login page with a success message
      navigate('/login', { state: { message: 'Registration successful! Please log in.' } });

    } catch (err) {
      // Handle specific backend errors gracefully
      if (err.response && err.response.data) {
        // Combine multiple error messages if the backend sends them
        const errorData = err.response.data;
        const errorMessages = Object.keys(errorData)
          .map(key => `${key}: ${errorData[key]}`)
          .join(' ');
        setError(errorMessages || 'Registration failed. Please check your details.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      console.error('Registration error:', err.response || err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="register-container">
      <div className="register-header">
        <h2>Create an Account</h2>
        <p className="subtitle">Get started with your new account.</p>
      </div>

      <form id="register-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="username-input">Username</label>
          <input
            type="text"
            id="username-input"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Choose a unique username"
            required
            disabled={loading}
          />
        </div>

        <div className="input-group">
          <label htmlFor="email-input">Email</label>
          <input
            type="email"
            id="email-input"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="e.g., yourname@example.com"
            required
            disabled={loading}
          />
        </div>

        <div className="input-group">
          <label htmlFor="password-input">Password</label>
          <input
            type="password"
            id="password-input"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Create a strong password"
            required
            disabled={loading}
          />
        </div>

        {error && <p className="error-message">{error}</p>}

        <button type="submit" id="submit-button" disabled={loading}>
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <p className="login-link">
        Already have an account? <Link to="/login">Sign In</Link>
      </p>
    </div>
  );
}

export default Register;