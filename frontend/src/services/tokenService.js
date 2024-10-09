// tokenService.js
import CryptoJS from 'crypto-js';

const secretKey = process.env.REACT_APP_SECRET_KEY || 'default-secret-key';

// Encrypt and store tokens securely
export const setAuthTokens = (tokens) => {
  if (!tokens) return;
  const encryptedTokens = CryptoJS.AES.encrypt(JSON.stringify(tokens), secretKey).toString();
  sessionStorage.setItem('authTokens', encryptedTokens);
};

// Retrieve and decrypt tokens
export const getAuthTokens = () => {
  const encryptedTokens = sessionStorage.getItem('authTokens');
  if (!encryptedTokens) {
    return null;
  }
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedTokens, secretKey);
    return JSON.parse(bytes.toString(CryptoJS.enc.Utf8));
  } catch (e) {
    console.error('Failed to decrypt tokens:', e);
    return null;
  }
};
