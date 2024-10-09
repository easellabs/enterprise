import React, { useState } from 'react';
import axios from '../../services/auth';

const RegisterPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/register/', { email, password });
            setMessage('Registration successful. You can now login.');
        } catch (error) {
            setMessage('Registration failed. Please try again.');
            console.error(error);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                <h1 className="text-2xl font-semibold text-gray-700 mb-6">Register</h1>
                <form onSubmit={handleRegister}>
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
                        Register
                    </button>
                </form>
                {message && <p className="mt-4 text-red-600">{message}</p>}
            </div>
        </div>
    );
};

export default RegisterPage;
