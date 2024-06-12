// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Main from './components/Main';
import ScrappingList from './components/hotdeal/ScrappingList';
import ScrappingDetail from './components/hotdeal/ScrappingDetail';
import KeywordList from './components/keyword_manager/KeywordList';
import FilteredAllScrappingList from './components/keyword_manager/FilteredAllScrappingList';
import FilteredAScrappingList from './components/keyword_manager/FilteredAScrappingList';
import KeywordCreate from './components/keyword_manager/KeywordCreate';
import KeywordDelete from './components/keyword_manager/KeywordDelete';
import DiscordMessageActiveUpdate from './components/keyword_manager/DiscordMessageActiveUpdate';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/scrappinglist">Scrapping List</Link>
            </li>
            <li>
              <Link to="/keywordlist">Keyword List</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/scrappinglist" element={<ScrappingList />} />
          <Route path="/scrappingdetail/:id" element={<ScrappingDetail />} />
          <Route path="/keywordlist" element={<KeywordList />} />
          <Route path="/filteredallscrappinglist" element={<FilteredAllScrappingList />} />
          <Route path="/filteredascrappinglist/:keyword" element={<FilteredAScrappingList />} />
          <Route path="/keywordcreate" element={<KeywordCreate />} />
          <Route path="/keyworddelete" element={<KeywordDelete />} />
          <Route path="/discordmessageactiveupdate/:id" element={<DiscordMessageActiveUpdate />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
