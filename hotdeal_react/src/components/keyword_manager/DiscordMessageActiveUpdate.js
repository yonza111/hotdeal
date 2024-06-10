// src/components/keyword_manager/DiscordMessageActiveUpdate.js
import React from 'react';
import { useParams } from 'react-router-dom';

const DiscordMessageActiveUpdate = () => {
  const { id } = useParams();
  return (
    <div>
      <h1>Update Discord Message for {id}</h1>
      {/* Discord Message Active Update 컴포넌트 내용 */}
    </div>
  );
};

export default DiscordMessageActiveUpdate;
