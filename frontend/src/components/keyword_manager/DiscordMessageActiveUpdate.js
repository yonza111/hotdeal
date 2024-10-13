// src/components/keyword_manager/DiscordMessageActiveUpdate.js
import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../AuthContext'; // AuthContext 가져오기

const DiscordMessageActiveUpdate = () => {
    const { user } = useContext(AuthContext);
    const [discordMessageActive, setDiscordMessageActive] = useState(false);
    const token = user ? user.token : null;

    useEffect(() => {
        const fetchDiscordMessageActiveStatus = () => {
            // axios.get(`http://127.0.0.1:8000/keyword_manager/api/active/${user.id}/`, {
            axios.get(`/api/keyword_manager/api/active/${user.id}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                setDiscordMessageActive(response.data.active);
            })
            .catch(error => {
                console.error('Error fetching Discord message active status:', error);
            });
        };

        if (user) {
            fetchDiscordMessageActiveStatus();
        }
    }, [user, token]); // user와 token을 의존성 배열에 추가

    const handleToggleActive = () => {
        const newActiveStatus = !discordMessageActive;
        // axios.put(`http://127.0.0.1:8000/keyword_manager/api/active/${user.id}/`, { active: newActiveStatus }, {
        axios.put(`/api/keyword_manager/api/active/${user.id}/`, { active: newActiveStatus }, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            setDiscordMessageActive(newActiveStatus);
            console.log('Discord message active status updated successfully.');
        })
        .catch(error => {
            console.error('Error updating Discord message active status:', error);
        });
    };

    return (
        <div>
            {discordMessageActive ? (
                <p>
                    Discord Message Active: Yes
                    <button onClick={handleToggleActive}>Deactivate</button>
                </p>
            ) : (
                <p>
                    Discord Message Active: No
                    <button onClick={handleToggleActive}>Activate</button>
                </p>
            )}
        </div>
    );
};

export default DiscordMessageActiveUpdate;
