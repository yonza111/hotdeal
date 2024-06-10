import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Pagination from "./Pagination";

const ScrappingListView = () => {
  const [scrappings, setScrappings] = useState([]);

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

  return (
    <div>
      <h1>Scrapping List</h1>
      <ul>
        {scrappings.map(scrapping => (
          <li key={scrapping.id}>
            <Link to={`/scrappingdetail/${scrapping.id}`}> 
            <div>{scrapping.title}</div></Link>
            <div>가격: {scrapping.price}</div>
            <div>카테고리: {scrapping.category}</div>
            <div>쇼핑몰: {scrapping.shop}</div>
            <div>배송비: {scrapping.delivery_fee}</div>
            <div>등록시간: {scrapping.register_time}</div>
            {/* Add more fields as needed */}
            
          </li>
        ))}
      </ul>
      {/* Add links for Category List and Scrapping Search */}
      <ul>
        <li><Link to="/categorylist">Category List</Link></li>
        <li><Link to="/scrappingsearch">Scrapping Search</Link></li>
      </ul>
    </div>
  );
};


export default ScrappingListView;



