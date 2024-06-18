// PrivateRoute.js
import React, { useContext, useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../components/AuthContext';
import { toast } from 'react-toastify';

const PrivateRoute = () => {
    const { isLoggedIn } = useContext(AuthContext);
    const [initialLoad, setInitialLoad] = useState(true);

    useEffect(() => {
        if (!initialLoad && !isLoggedIn) {
            toast.error("로그인해야 가능합니다");
        }
        if (initialLoad && isLoggedIn !== null) {
            setInitialLoad(false);
        }
    }, [isLoggedIn, initialLoad]);

    if (isLoggedIn === null) {
        return <p>Loading...</p>;  // 로딩 중일 때 보여줄 UI
    }

    return isLoggedIn ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
