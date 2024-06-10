// src/components/keyword_manager/FilteredAScrappingList.js
import React from 'react';
import { useParams } from 'react-router-dom';

const FilteredAScrappingList = () => {
  const { keyword } = useParams();
  return (
    <div>
      <h1>Filtered A Scrapping List for {keyword}</h1>
      {/* Filtered A Scrapping List 컴포넌트 내용 */}
    </div>
  );
};

export default FilteredAScrappingList;
