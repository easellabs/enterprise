import React, { useEffect, useState, useContext } from 'react';
import api from '../services/apiService';
import { AuthContext } from '../context/AuthContext';

const UserDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const { authTokens } = useContext(AuthContext);

  useEffect(() => {
    if (authTokens) {
      const fetchData = async () => {
        try {
          const response = await api.get('user-dashboard/', {
            headers: {
              Authorization: `Bearer ${authTokens.access}`
            }
          });
          setDashboardData(response.data);
        } catch (error) {
          console.error('Error fetching user dashboard data:', error);
        }
      };
      
      fetchData();
    }
  }, [authTokens]);

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-4">User Dashboard</h1>
      {dashboardData ? (
        <div>
          <p>Welcome, {dashboardData.user.username}!</p>
          <p>Email: {dashboardData.user.email}</p>
          <p>Role: {dashboardData.user.role}</p>
        </div>
      ) : (
        <p>Loading user dashboard...</p>
      )}
    </div>
  );
};

export default UserDashboard;
