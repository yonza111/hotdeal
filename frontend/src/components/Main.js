//components/main.js
import React from 'react';
import { Link } from 'react-router-dom';

const Main = () => {
  return (
    <div>
      <h1>Main</h1>
      <ul>
        <li><Link to="/scrappinglist">Scrapping List</Link></li>
        <li><Link to="/keywordlist">Keyword List</Link></li>
      </ul>
    </div>
  );
};

export default Main;
