// components/Auth.js


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
            // axios.post('http://127.0.0.1:8000/discord/discord/callback/', { code })
            axios.post('/api/discord/callback/', { code }) // 변경된 URL
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








