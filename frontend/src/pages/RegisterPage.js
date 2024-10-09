import React, { useState } from 'react';
import { registerUser } from '../services/apiService';
import { Button } from '../components/button';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    try {
      const response = await registerUser(username, password);
      setMessage('User registered successfully! Please login.');
    } catch (error) {
      setMessage('Error registering user: ' + error.message);
    }
  };

  return (
    <div className="flex flex-col items-center py-8">
      <h1 className="text-3xl font-bold mb-4">Register</h1>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="mb-4 p-2 border rounded"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="mb-4 p-2 border rounded"
      />
      <Button label="Register" onClick={handleRegister} />
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
};

export default RegisterPage;
