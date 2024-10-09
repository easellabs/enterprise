import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const TwoFactor = () => {
    const navigate = useNavigate();
    const [otp, setOtp] = useState('');
    const [errors, setErrors] = useState('');

    const handleChange = (e) => {
        setOtp(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors('');

        try {
            const response = await axios.post('/api/auth/verify-2fa/', { otp });
            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            navigate('/dashboard');
        } catch (err) {
            setErrors('Invalid OTP.');
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white p-8 border border-gray-300 rounded-lg shadow-md">
            <h1 className="text-2xl font-bold mb-4">Two-Factor Authentication</h1>
            {errors && <div className="text-red-600 mb-4">{errors}</div>}
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="otp" className="block text-sm font-medium text-gray-700">Enter OTP</label>
                    <input
                        type="text"
                        name="otp"
                        id="otp"
                        value={otp}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
                >
                    Verify OTP
                </button>
            </form>
        </div>
    );
};

export default TwoFactor;
