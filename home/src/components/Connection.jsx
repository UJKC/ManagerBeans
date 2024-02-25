import React, { useState, useEffect } from 'react';

const ConnectionStatus = () => {
  const [status, setStatus] = useState('');

  useEffect(() => {
    // Fetch connection status from Flask backend
    fetch('/auth/connection-status')
      .then(response => response.json())
      .then(data => setStatus(data.status))
      .catch(error => console.error('Error fetching connection status:', error));
  }, []);

  return (
    <div>
      <h2>Connection Status</h2>
      <p>Status: {status}</p>
    </div>
  );
};

export default ConnectionStatus;
