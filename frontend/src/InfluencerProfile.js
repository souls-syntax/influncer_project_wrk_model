// src/InfluencerProfile.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

// Aap iske liye alag se CSS file bana sakte hain: src/styles/InfluencerProfile.css
// import './styles/InfluencerProfile.css';

function InfluencerProfile() {
  const [influencer, setInfluencer] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const { influencerId } = useParams(); // URL se ID nikalne ke liye

  useEffect(() => {
    const fetchInfluencerDetails = async () => {
      setIsLoading(true);
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          setError("Aap logged in nahi hain.");
          setIsLoading(false);
          return;
        }

        const response = await axios.get(`http://127.0.0.1:8000/api/influencers/${influencerId}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setInfluencer(response.data);
      } catch (err) {
        setError("Influencer ki details nahi mil pa rahi hain.");
        console.error("Error fetching influencer details:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInfluencerDetails();
  }, [influencerId]);

  if (isLoading) return <p>Loading profile...</p>;
  if (error) return <p className="error-message">{error}</p>;
  if (!influencer) return <p>No influencer found.</p>;

  return (
    <div className="profile-container">
      <Link to="/dashboard">← Back to Dashboard</Link>
      <div className="profile-header">
        <img src={influencer.photo_url} alt={influencer.name} />
        <div>
          <h1>{influencer.name}</h1>
          <p>{influencer.subscribers.toLocaleString()} Subscribers</p>
          <p>{influencer.category}</p>
        </div>
      </div>
      <div className="profile-details">
        <h2>About</h2>
        <p>{influencer.description || "No description available."}</p>
        <h2>AI Analysis</h2>
        <p><strong>Primary Niche:</strong> {influencer.ai_niche}</p>
        <p><strong>Brand Safety Score:</strong> {influencer.ai_safety_score}/10</p>
        <p><strong>Recommendation:</strong> {influencer.ai_recommendation}</p>
      </div>
    </div>
  );
}

export default InfluencerProfile;