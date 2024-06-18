// DiscordLoginButton.js


import React, { useContext } from 'react';
import { AuthContext } from '../components/AuthContext'; // AuthContext 가져오기

const DiscordLoginButton = () => {
    const { isLoggedIn, logout } = useContext(AuthContext); // 로그인 상태와 로그아웃 함수 가져오기

    const CLIENT_ID = '1219148050354802749';
    const REDIRECT_URI = 'http://127.0.0.1:3000/auth/';
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










// import React, { useState, useEffect } from 'react';

// const DiscordLoginButton = () => {
//     const [isLoggedIn, setIsLoggedIn] = useState(false);
//     const [username, setUsername] = useState(null);

//     useEffect(() => {
//         // 페이지 로드 시 로컬 스토리지에서 로그인 상태를 확인
//         const storedUsername = localStorage.getItem('username');
//         if (storedUsername) {
//             setUsername(storedUsername);
//             setIsLoggedIn(true);
//         }
//     }, []);

//     const CLIENT_ID = '1219148050354802749';
//     const REDIRECT_URI = 'http://127.0.0.1:3000/auth/';
//     const SCOPE = 'identify email';

//     const discordLogin = () => {
//         window.location.href = `https://discord.com/api/oauth2/authorize?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=code&scope=${SCOPE}`;
//     };

//     const handleLogout = () => {
//         setUsername(null);
//         setIsLoggedIn(false);
//         localStorage.removeItem('username');
//     };

//     return (
//         <div>
//             {isLoggedIn ? (
//                 <div>
//                     <p>Welcome, {username}!</p>
//                     <button onClick={handleLogout}>Logout</button>
//                 </div>
//             ) : (
//                 <button onClick={discordLogin}>Discord Login</button>
//             )}
//         </div>
//     );
// };

// export default DiscordLoginButton;





