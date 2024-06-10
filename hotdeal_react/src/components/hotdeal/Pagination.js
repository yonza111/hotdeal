import React, { useState } from "react";
import Pagination from "react-js-pagination";

const Paging = ({ onChange }) => {
  const [page, setPage] = useState(1);

  const handlePageChange = (pageNumber) => {
    setPage(pageNumber);
    onChange(pageNumber); // 페이지 변경 이벤트 전달
  };

  return (
    <Pagination
      activePage={page}
      itemsCountPerPage={20}
      totalItemsCount={5000}
      pageRangeDisplayed={10}
      prevPageText={"‹"}
      nextPageText={"›"}
      onChange={handlePageChange} // 페이지 변경을 핸들링하는 함수
    />
  );
};

export default Paging;
