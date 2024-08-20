import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { useParams, Link  } from 'react-router-dom';
import { AuthContext } from '../AuthContext';

const FilteredAScrappingList = () => {
  const { keyword } = useParams();
  const { user } = useContext(AuthContext);
  const [scrappingList, setScrappingList] = useState([]);

  useEffect(() => {
    if (user) {
      // axios.get(`http://127.0.0.1:8000/keyword_manager/api/filtered/${keyword}/`, {
      axios.get(`/api/keyword_manager/api/filtered/${keyword}/`, {
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      })
        .then(response => {
          setScrappingList(response.data);
        })
        .catch(error => {
          console.error('Error fetching scrapping list:', error);
        });
    }
  }, [keyword, user]);

  return (
    <div>
      <h1>Scrapping Results for: {keyword}</h1>
      <ul>
        {scrappingList.map(item => (
          <li key={item.id}>
            <Link to={`/scrappingdetail/${item.id}`}>{item.title}</Link>
            {console.log(item)}
            </li>
        ))}
      </ul>
    </div>
  );
};

export default FilteredAScrappingList;
