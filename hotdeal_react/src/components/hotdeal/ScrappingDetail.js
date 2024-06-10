import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom'; // useParams import 추가

const ScrappingDetail = () => {
  const { id } = useParams(); // URL에서 id 가져오기
  const [scrapping, setScrapping] = useState(null);

  useEffect(() => {
    const fetchScrappingDetail = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/hotdeal/api/scrappinglist/${id}/`); // URL에서 가져온 id 사용
        setScrapping(response.data);
      } catch (error) {
        console.error('Error fetching scrapping detail:', error);
      }
    };

    fetchScrappingDetail();
  }, [id]); // id를 의존성 배열에 추가

  return (
    <div>
      {scrapping ? (
        <div>
          <h2>{scrapping.title}</h2>
          <p>가격: {scrapping.price}</p>
          <p>카테고리: {scrapping.category}</p>
          <p>쇼핑몰: {scrapping.shop}</p>
          <p>배송비: {scrapping.delivery_fee}</p>
          <p>등록시간: {scrapping.register_time}</p>
          <p>링크: <a href={scrapping.url} target="_blank" rel="noopener noreferrer">{scrapping.url}</a></p>
          {/* Add more fields as needed */}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default ScrappingDetail;
