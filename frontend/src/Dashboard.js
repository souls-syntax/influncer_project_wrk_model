import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/Dashboard.css'; 
import { Link, useNavigate } from 'react-router-dom'; // Card ko clickable banane ke liye

// Aapke project ke CSS ke hisaab se styles import karein
// import './Dashboard.css'; 

function Dashboard() {
  // State variables data manage karne ke liye
  const [influencers, setInfluencers] = useState([]);
  const [searchTerm, setSearchTerm] = useState(''); // Category ya naam se search ke liye
  const [minSubs, setMinSubs] = useState(0); // Minimum subscribers ke liye
  const [location, setLocation] = useState(''); // Location se search ke liye
  const [isLoading, setIsLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  const navigate = useNavigate();
  // Yeh useEffect tab chalega jab bhi koi filter (searchTerm, minSubs, location) badlega
  useEffect(() => {
    const fetchInfluencers = async () => {
      setIsLoading(true); // Data fetch shuru hone par loading = true
      setError(null); // Purana error saaf karein

      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          // Agar token nahi hai, toh aage na badhein
          setError("User not authenticated.");
          setIsLoading(false);
          return;
        }

        // --- YAHAN API CALL KA SAHI LOGIC HAI ---
        // Sahi parameters ke saath API URL banayein
        const params = new URLSearchParams();
        if (searchTerm) params.append('search_term', searchTerm);
        if (minSubs > 0) params.append('min_subs', minSubs);
        if (location) params.append('location', location);
        
        const response = await axios.get(`http://127.0.0.1:8000/api/influencers/?${params.toString()}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        setInfluencers(response.data);

      } catch (err) {
        setError("Data fetch karne mein dikkat aa rahi hai. Baad mein try karein.");
        console.error("Error fetching influencers:", err);
      } finally {
        setIsLoading(false); // Data fetch hone ke baad loading = false
      }
    };

    fetchInfluencers();
  }, [searchTerm, minSubs, location]);
  const handleLogout = () => {
    // 1. Browser ki local storage se login tokens ko hatayein.
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');

    // 2. User ko login page par wapas bhej dein.
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <div className="header">
        <h1>Influencer Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>
      
      {/* --- FILTER SECTION --- */}
      <div className="filters-container">
        <input 
          type="text" 
          placeholder="Search by Name or Category..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <input 
          type="number" 
          placeholder="Min Subscribers"
          onChange={(e) => setMinSubs(Number(e.target.value))}
        />
        <input 
          type="text" 
          placeholder="Location..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </div>

      {/* --- DATA DISPLAY SECTION --- */}
      {isLoading ? (
        <p>Loading influencers...</p>
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : (
        <div className="influencers-grid">
          {influencers.length > 0 ? influencers.map(influencer => (
            // --- CARD PAR CLICK KA LOGIC ---
            // Har card ko <Link> se wrap kiya gaya hai
            <Link key={influencer.id} to={`/influencer/${influencer.id}`} className="card-link">
              <div className="influencer-card">
                <img src={influencer.photo_url} alt={influencer.name} />
                <h3>{influencer.name}</h3>
                <p>{influencer.subscribers.toLocaleString()} Subscribers</p>
                <p className="category-tag">{influencer.category}</p>
              </div>
            </Link>
          )) : (
            <p>No influencers found for the selected filters.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default Dashboard;