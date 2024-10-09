import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/apiService';
import { Button } from '../components/button';

const RegisterAdminPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { authTokens } = useContext(AuthContext);
  const navigate = useNavigate();

  // Function to handle the admin registration
  const handleAdminRegister = async () => {
    if (loading) return;

    setLoading(true);
    setError('');
    setMessage('');

    // Basic validation
    if (!username || !password) {
      setError('Username and password are required.');
      setLoading(false);
      return;
    }

    try {
      await api.post(
        'register-admin/',
        { username, password },
        {
          headers: {
            Authorization: `Bearer ${authTokens?.access}`,
          },
        }
      );
      setMessage('Admin user registered successfully!');
      setUsername('');
      setPassword('');

      // Redirect to admin dashboard after successful registration
      setTimeout(() => {
        navigate('/admin-dashboard');
      }, 2000);

    } catch (error) {
      console.error('Error registering admin user:', error);
      setError('Failed to register admin user. Please check your credentials or try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center py-8 px-4" role="main">
      <h1 className="text-3xl font-bold mb-4" role="heading" aria-level="1">
        Register Admin User
      </h1>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="mb-4 p-2 border rounded w-full max-w-md"
        aria-label="Username"
        aria-required="true"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="mb-4 p-2 border rounded w-full max-w-md"
        aria-label="Password"
        aria-required="true"
      />

      {error && (
        <div className="mb-4 text-red-600" role="alert">
          {error}
        </div>
      )}

      {message && (
        <div className="mb-4 text-green-600" role="status">
          {message}
        </div>
      )}

      <Button
        label={loading ? 'Registering...' : 'Register Admin'}
        onClick={handleAdminRegister}
        disabled={loading}
      />
    </main>
  );
};

export default RegisterAdminPage;
