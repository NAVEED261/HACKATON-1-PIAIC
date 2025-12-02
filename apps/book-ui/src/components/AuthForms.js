import React, { useState, useEffect } from 'react';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000';

function AuthForms() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [learningPreferences, setLearningPreferences] = useState('');
  const [hardwareSoftwareBackground, setHardwareSoftwareBackground] = useState('');
  const [message, setMessage] = useState('');
  const [activeForm, setActiveForm] = useState('signup'); // 'signup', 'signin', 'profile'

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsLoggedIn(true);
      fetchProfile(token);
    }
  }, []);

  const fetchProfile = async (token) => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUsername(data.username);
        setEmail(data.email);
        setLearningPreferences(data.learning_preferences || '');
        setHardwareSoftwareBackground(data.hardware_software_background || '');
        setMessage('');
      } else {
        localStorage.removeItem('access_token');
        setIsLoggedIn(false);
        setMessage('Session expired or invalid. Please sign in again.');
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
      localStorage.removeItem('access_token');
      setIsLoggedIn(false);
      setMessage('Failed to fetch profile. Please try again.');
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, learning_preferences: learningPreferences, hardware_software_background: hardwareSoftwareBackground }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(`Signup successful for ${data.username}! Please sign in.`);
        setActiveForm('signin');
      } else {
        setMessage(data.detail || 'Signup failed.');
      }
    } catch (error) {
      console.error('Error during signup:', error);
      setMessage('An error occurred during signup.');
    }
  };

  const handleSignin = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }).toString(),
      });
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        setIsLoggedIn(true);
        fetchProfile(data.access_token);
        setActiveForm('profile');
        setMessage('Sign in successful!');
      } else {
        setMessage(data.detail || 'Sign in failed.');
      }
    } catch (error) {
      console.error('Error during signin:', error);
      setMessage('An error occurred during signin.');
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setMessage('');
    const token = localStorage.getItem('access_token');
    if (!token) {
      setMessage('Not authenticated.');
      return;
    }

    const updateData = {
      email,
      learning_preferences: learningPreferences,
      hardware_software_background: hardwareSoftwareBackground,
    };
    // Only include password in update if it's provided (i.e., user wants to change it)
    if (password) {
      updateData.password = password;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/user/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(updateData),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage('Profile updated successfully!');
        // Refresh profile data in case username/email was updated (though not allowed in this UI)
        fetchProfile(token);
      } else {
        setMessage(data.detail || 'Profile update failed.');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      setMessage('An error occurred during profile update.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsLoggedIn(false);
    setUsername('');
    setEmail('');
    setPassword('');
    setLearningPreferences('');
    setHardwareSoftwareBackground('');
    setMessage('Logged out successfully.');
    setActiveForm('signin');
  };

  return (
    <div style={{
      maxWidth: '500px',
      margin: '50px auto',
      padding: '20px',
      border: '1px solid #ddd',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      backgroundColor: '#fff'
    }}>
      {message && <p style={{ color: 'red' }}>{message}</p>}

      {!isLoggedIn && (
        <div style={{ marginBottom: '20px' }}>
          <button onClick={() => setActiveForm('signup')} style={{ marginRight: '10px' }}>Signup</button>
          <button onClick={() => setActiveForm('signin')}>Sign In</button>
        </div>
      )}

      {isLoggedIn && (
        <div style={{ marginBottom: '20px' }}>
          <button onClick={() => setActiveForm('profile')} style={{ marginRight: '10px' }}>Profile</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}

      {activeForm === 'signup' && !isLoggedIn && (
        <form onSubmit={handleSignup}>
          <h2>Signup</h2>
          <div>
            <label>Username:</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div>
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <div>
            <label>Learning Preferences (optional):</label>
            <textarea value={learningPreferences} onChange={(e) => setLearningPreferences(e.target.value)} rows="3"></textarea>
          </div>
          <div>
            <label>Hardware/Software Background (optional):</label>
            <textarea value={hardwareSoftwareBackground} onChange={(e) => setHardwareSoftwareBackground(e.target.value)} rows="3"></textarea>
          </div>
          <button type="submit">Signup</button>
        </form>
      )}

      {activeForm === 'signin' && !isLoggedIn && (
        <form onSubmit={handleSignin}>
          <h2>Sign In</h2>
          <div>
            <label>Username:</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit">Sign In</button>
        </form>
      )}

      {activeForm === 'profile' && isLoggedIn && (
        <form onSubmit={handleUpdateProfile}>
          <h2>User Profile</h2>
          <div>
            <label>Username:</label>
            <input type="text" value={username} disabled />
          </div>
          <div>
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label>Change Password (leave blank if not changing):</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div>
            <label>Learning Preferences:</label>
            <textarea value={learningPreferences} onChange={(e) => setLearningPreferences(e.target.value)} rows="3"></textarea>
          </div>
          <div>
            <label>Hardware/Software Background:</label>
            <textarea value={hardwareSoftwareBackground} onChange={(e) => setHardwareSoftwareBackground(e.target.value)} rows="3"></textarea>
          </div>
          <button type="submit">Update Profile</button>
        </form>
      )}
    </div>
  );
}

export default AuthForms;
