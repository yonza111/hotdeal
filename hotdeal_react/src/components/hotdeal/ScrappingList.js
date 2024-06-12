// components/hotdeal/ScrappingList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Pagination from "./Pagination";

// 카테고리 배열 추가
const categories = ['먹거리', 'SW/게임', 'PC제품', '가전제품', '생활용품', '의류', '세일정보', '화장품', '모바일/상품권', '패키지/이용권', '기타', '해외핫딜'];

const ScrappingListView = () => {
  const [scrappings, setScrappings] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(''); // 선택된 카테고리 상태 추가
  const [searchTerm, setSearchTerm] = useState(''); // 검색어 상태 추가

  useEffect(() => {
    const fetchScrappings = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/hotdeal/api/scrappinglist/');
        console.log('Data:', response.data); // 데이터 확인
        setScrappings(response.data);
      } catch (error) {
        console.error('Error fetching scrappinglist:', error);
      }
    };

    fetchScrappings();
  }, []);

  // 카테고리 버튼 클릭 시 호출되는 함수
  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  // 선택된 카테고리와 검색어에 따라 항목을 필터링
  const filteredScrappings = scrappings.filter(scrapping => {
    const matchesCategory = selectedCategory ? scrapping.category === selectedCategory : true;
    const matchesSearchTerm = scrapping.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                              scrapping.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                              scrapping.shop.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearchTerm;
  });

  return (
    <div>
      <h1>Scrapping List</h1>
      <div>
        {categories.map(category => (
          <button key={category} onClick={() => handleCategoryClick(category)}>
            {category}
          </button>
        ))}
        {/* 전체 보기 버튼 추가 */}
        <button onClick={() => handleCategoryClick('')}>전체 보기</button>
      </div>
      {/* 검색 입력 필드 추가 */}
      <input 
        type="text" 
        placeholder="검색어를 입력하세요" 
        value={searchTerm} 
        onChange={(e) => setSearchTerm(e.target.value)} 
      />
      <ul>
        {filteredScrappings.map(scrapping => (
          <li key={scrapping.id}>
            <div><Link to={`/scrappingdetail/${scrapping.id}`}>{scrapping.title}</Link></div>
            <div>가격: {scrapping.price}</div>
            <div>카테고리: {scrapping.category}</div>
            <div>쇼핑몰: {scrapping.shop}</div>
            <div>배송비: {scrapping.delivery_fee}</div>
            <div>등록시간: {scrapping.register_time}</div>
            {/* Add more fields as needed */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ScrappingListView;
