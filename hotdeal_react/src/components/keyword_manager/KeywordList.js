// src/components/keyword_manager/KeywordList.js
import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../AuthContext';

const KeywordList = () => {
  const { isLoggedIn, user } = useContext(AuthContext);
  const [keywords, setKeywords] = useState([]);
  const [newKeyword, setNewKeyword] = useState('');

  useEffect(() => {
    if (isLoggedIn) {
      axios.get(`http://127.0.0.1:8000/keyword_manager/api/list/`, {
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      })
        .then(response => {
          setKeywords(response.data);
        })
        .catch(error => {
          console.error('Error fetching keywords:', error);
        });
    }
  }, [isLoggedIn, user.token]);


  const handleKeywordChange = (event) => {
    setNewKeyword(event.target.value);
  };

  const handleKeywordSubmit = (event) => {
    event.preventDefault();
    if (newKeyword.trim() === '') {
      return;
    }

    axios.post('http://127.0.0.1:8000/keyword_manager/api/add/', { text: newKeyword }, {
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
      .then(response => {
        setKeywords([...keywords, response.data]);
        console.log('Response from server:', response.data);
        setNewKeyword('');
      })
      .catch(error => {
        console.error('Error adding keyword:', error);
      });
  };

  const handleKeywordDelete = (id) => {
    axios.delete(`http://127.0.0.1:8000/keyword_manager/api/delete/${id}/`, {
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
      .then(() => {
        setKeywords(keywords.filter(keyword => keyword.id !== id));
      })
      .catch(error => {
        console.error('Error deleting keyword:', error);
      });
  };


  return (
    <div>
      <h1>Keyword List</h1>
      {isLoggedIn ? (
        <p>Logged in as: {user.username}</p>
      ) : (
        <p>Please log in to view keywords.</p>
      )}
      <h2>My Keywords</h2>
      <ul>
        {keywords.map(keyword => (
          <li key={keyword.id}>
          {keyword.text}  <button onClick={() => handleKeywordDelete(keyword.id)}>Delete</button>
          <Link to={`/filteredascrappinglist/${keyword.text}`}> 키워드 검색 결과</Link>
        </li>
        ))}
      </ul>
      

      {isLoggedIn && (
        <form onSubmit={handleKeywordSubmit}>
          <input
            type="text"
            value={newKeyword}
            onChange={handleKeywordChange}
            placeholder="Enter a new keyword"
          />
          <button type="submit">Add Keyword</button>
        </form>
      )}

    <li><Link to={`/discordmessageactiveupdate/${user.id}`}>discordmessage setting</Link></li>


    </div>
  );
};

export default KeywordList;
