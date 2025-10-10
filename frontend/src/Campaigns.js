import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          navigate('/login');
          return;
        }
        // User ke saare campaigns fetch karne ke liye API call
        const response = await axios.get('http://127.0.0.1:8000/dashboard/campaigns/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setCampaigns(response.data);
      } catch (error) {
        console.error('Failed to fetch campaigns', error);
        if (error.response && error.response.status === 401) {
          navigate('/login');
        }
      }
    };
    fetchCampaigns();
  }, [navigate]);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>My Saved Lists</h2>
        <Link to="/dashboard">Back to Discovery</Link>
      </div>
      <hr />
      {campaigns.length === 0 ? (
        <p>You haven't saved any lists yet.</p>
      ) : (
        <div>
          {campaigns.map(campaign => (
            <div key={campaign.id} style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '15px', marginBottom: '15px' }}>
              <h3>{campaign.name}</h3>
              <p><strong>Date Created:</strong> {new Date(campaign.date_created).toLocaleDateString()}</p>
              <p><strong>Influencers Saved (IDs):</strong></p>
              <ul>
                {/* Influencer IDs ko split karke list mein dikhayein */}
                {campaign.influencer_ids.split(',').map(id => (
                  <li key={id}>{id}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Campaigns;