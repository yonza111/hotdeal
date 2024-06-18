// Auth.js


import React, { useEffect, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../components/AuthContext'; // AuthContext 가져오기

const Auth = () => {
    const navigate = useNavigate();
    const { login } = useContext(AuthContext); // login 함수 가져오기

    useEffect(() => {
        const currentUrl = window.location.href;
        const code = new URL(currentUrl).searchParams.get("code");

        if (code) {
            console.log('Extracted code:', code);
            // 추출한 코드를 서버로 보냅니다.
            axios.post('http://127.0.0.1:8000/discord/discord/callback/', { code })
                .then(response => {
                    console.log('Receiving code To django - Server response:', response.data);
                    const user = response.data.user;
                    const token = response.data.token;
                    const userWithToken = { ...user, token };
                    login(userWithToken); // 로그인 상태 업데이트
                    navigate('/');

                     // 사용자 객체를 콘솔에 출력
                     console.log('Logged in user:', userWithToken);
                })
                .catch(error => {
                    console.error('Receiving code To django - Error Receiving code to server:', error);
                });
        }
    }, [login, navigate]);

    return (
        <div>
            <p>Loading...</p>
        </div>
    );
};

export default Auth;











// import React, { useEffect, useState } from 'react';
// import { useNavigate } from 'react-router-dom'; // useNavigate 훅을 가져옵니다.
// import axios from 'axios';

// const Auth = () => {
//     const [username, setUsername] = useState(null);
//     const [isLoggedIn, setIsLoggedIn] = useState(false);
//     const navigate = useNavigate(); // useNavigate 훅을 초기화합니다.

//     useEffect(() => {
//         const currentUrl = window.location.href;
//         const code = new URL(currentUrl).searchParams.get("code");

//         // 페이지 로드 시 로컬 스토리지에서 로그인 상태를 확인
//         const storedUsername = localStorage.getItem('username');
//         if (storedUsername) {
//             setUsername(storedUsername);
//             setIsLoggedIn(true);
//             navigate('/'); // 이미 로그인된 상태라면 홈으로 리디렉션
//         }

//         if (code && !isLoggedIn) {
//             console.log('Extracted code:', code);

//             // 추출한 코드를 서버로 보냅니다.
//             axios.post('http://127.0.0.1:8000/discord/discord/callback/', { code })
//                 .then(response => {
//                     console.log('Receiving code To django - Server response:', response.data);
//                     setUsername(response.data.user);
//                     setIsLoggedIn(true);
//                     localStorage.setItem('username', response.data.user);
//                     navigate('/'); // 로그인 성공 후 홈으로 리디렉션
//                 })
//                 .catch(error => {
//                     console.error('Receiving code To django - Error Receiving code to server:', error);
//                 });
//         }
//     }, [isLoggedIn, navigate]);

//     return (
//         <div>
//             {isLoggedIn ? (
//                 <h1>Welcome, {username}!</h1>
//             ) : (
//                 <p>Loading...</p>
//             )}
//         </div>
//     );
// };

// export default Auth;




