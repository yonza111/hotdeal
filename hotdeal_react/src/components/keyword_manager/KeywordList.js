// src/components/keyword_manager/KeywordList.js
import React from 'react';
import { Link } from 'react-router-dom';

const KeywordList = () => {
  return (
    <div>
      <h1>Keyword List</h1>
      <p> 내가 등록한 키워드들 현재 상태 나와야 함.</p>
      <ul>
        <li><Link to="/filteredallscrappinglist">Filtered All Scrapping List</Link></li>
        <li><Link to="/keywordcreate">Create Keyword</Link></li>
        <li><Link to="/keyworddelete">Delete Keyword</Link></li>
      </ul>
      {/* Keyword List 컴포넌트 내용 */}
    </div>
  );
};

export default KeywordList;
