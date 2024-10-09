// import React, { useState, useContext } from 'react';
// import { loginUser } from '../services/apiService';
// import Button from '../components/Button';
// import { AuthContext } from '../context/AuthContext';

// const LoginPage = () => {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const { setAuthTokens } = useContext(AuthContext);
//   const [message, setMessage] = useState('');

//   const handleLogin = async () => {
//     try {
//       const response = await loginUser(username, password);
//       setAuthTokens(response.data); // Save tokens in context
//       localStorage.setItem('authTokens', JSON.stringify(response.data)); // Persist tokens in localStorage
//       setMessage('Login successful!');
//     } catch (error) {
//       setMessage('Login error: ' + error.message);
//     }
//   };

//   return (
//     <div className="flex flex-col items-center py-8">
//       <h1 className="text-3xl font-bold mb-4">Login</h1>
//       <input
//         type="text"
//         placeholder="Username"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//         className="mb-4 p-2 border rounded"
//       />
//       <input
//         type="password"
//         placeholder="Password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//         className="mb-4 p-2 border rounded"
//       />
//       <Button label="Login" onClick={handleLogin} />
//       {message && <p className="mt-4">{message}</p>}
//     </div>
//   );
// };

// export default LoginPage;
