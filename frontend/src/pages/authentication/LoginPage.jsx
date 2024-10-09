import React, { useState } from 'react';
import axios from '../../services/auth';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/login/', { email, password });
            console.log(response.data); // Handle token storage
            setMessage('Login successful. Please proceed with two-factor authentication if enabled.');
        } catch (error) {
            setMessage('Login failed. Please try again.');
            console.error(error);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                <h1 className="text-2xl font-semibold text-gray-700 mb-6">Login</h1>
                <form onSubmit={handleLogin}>
                    <input
                        type="email"
                        className="w-full p-3 border rounded-lg mb-4"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        className="w-full p-3 border rounded-lg mb-6"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button
                        type="submit"
                        className="w-full p-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                    >
                        Login
                    </button>
                </form>
                {message && <p className="mt-4 text-red-600">{message}</p>}
            </div>
        </div>
    );
};

export default LoginPage;
