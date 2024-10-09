import React, { useState } from 'react';
import axios from '../../services/auth';

const TwoFAPage = () => {
    const [otp, setOtp] = useState('');
    const [message, setMessage] = useState('');

    const handleVerifyOtp = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/verify-2fa/', { otp });
            console.log(response.data); // Store JWT securely
            setMessage('Two-Factor Authentication successful.');
        } catch (error) {
            setMessage('Invalid OTP. Please try again.');
            console.error(error);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                <h1 className="text-2xl font-semibold text-gray-700 mb-6">Two-Factor Authentication</h1>
                <form onSubmit={handleVerifyOtp}>
                    <input
                        type="text"
                        className="w-full p-3 border rounded-lg mb-6"
                        placeholder="Enter OTP"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        required
                    />
                    <button
                        type="submit"
                        className="w-full p-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                    >
                        Verify OTP
                    </button>
                </form>
                {message && <p className="mt-4 text-red-600">{message}</p>}
            </div>
        </div>
    );
};

export default TwoFAPage;
