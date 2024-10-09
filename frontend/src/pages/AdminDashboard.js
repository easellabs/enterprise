import React, { useEffect, useState, useContext } from 'react';
import api from '../services/apiService';
import { AuthContext } from '../context/AuthContext';

const AdminDashboard = () => {
  const [adminData, setAdminData] = useState(null);
  const { authTokens } = useContext(AuthContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('admin-dashboard/', {
          headers: {
            Authorization: `Bearer ${authTokens.access}`, // Include the access token
          },
        });
        setAdminData(response.data);
      } catch (error) {
        console.error('Error fetching admin dashboard data:', error);
      }
    };

    fetchData();
  }, [authTokens]);

  if (!adminData) {
    return <div>Loading admin dashboard...</div>;
  }

  return (
    <div>
      <h1>Welcome to the Admin Dashboard</h1>
      <p>Username: {adminData.admin_details.username}</p>
      <p>Role: {adminData.admin_details.role}</p>
      <p>Total Users: {adminData.admin_details.total_users}</p>
    </div>
  );
};

export default AdminDashboard;
