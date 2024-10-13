// 로그인 상태에 따라 네비게이션 바의 항목을 동적으로 업데이트
// 로그인 상태를 전역적으로 관리하고, 이를 바탕으로 네비게이션 바를 조건부 렌더링
// Context API
// components/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(null);  // 초기 상태를 null로 설정
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
            setIsLoggedIn(true);
        } else {
            setIsLoggedIn(false);  // 사용자가 없는 경우 false로 설정
        }
    }, []);

    const login = (user) => {
        setUser(user);
        setIsLoggedIn(true);
        localStorage.setItem('user', JSON.stringify(user));
    };

    const logout = () => {
        setUser(null);
        setIsLoggedIn(false);
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};