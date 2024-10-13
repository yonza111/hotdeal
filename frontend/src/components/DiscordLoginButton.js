// components/DiscordLoginButton.js


import React, { useContext } from 'react';
import { AuthContext } from '../components/AuthContext'; // AuthContext 가져오기

const DiscordLoginButton = () => {
    const { isLoggedIn, logout } = useContext(AuthContext); // 로그인 상태와 로그아웃 함수 가져오기

    const CLIENT_ID = '1219148050354802749';
    // const REDIRECT_URI = 'http://127.0.0.1:3000/auth/';
    const REDIRECT_URI = 'http://localhost/auth/';
    const SCOPE = 'identify email';

    const discordLogin = () => {
        window.location.href = `https://discord.com/api/oauth2/authorize?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=code&scope=${SCOPE}`;
    };

    return (
        <div>
            {isLoggedIn ? (
                <div>
                
                <button onClick={logout}>Logout</button>
                </div>
            ) : (
                <button onClick={discordLogin}>Discord Login</button>
            )}
        </div>
    );
};

export default DiscordLoginButton;







