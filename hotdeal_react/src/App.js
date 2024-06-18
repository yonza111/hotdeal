// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Main from './components/Main';
import ScrappingList from './components/hotdeal/ScrappingList';
import ScrappingDetail from './components/hotdeal/ScrappingDetail';
import KeywordList from './components/keyword_manager/KeywordList';
import FilteredAScrappingList from './components/keyword_manager/FilteredAScrappingList';
import KeywordCreate from './components/keyword_manager/KeywordCreate';
import KeywordDelete from './components/keyword_manager/KeywordDelete';
import DiscordMessageActiveUpdate from './components/keyword_manager/DiscordMessageActiveUpdate';
import DiscordLoginButton from './components/DiscordLoginButton';
import Auth from './components/Auth';
import { AuthProvider, AuthContext } from './components/AuthContext'; // AuthProvider 및 AuthContext 가져오기
import PrivateRoute from './components/PrivateRoute'; // PrivateRoute 가져오기
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'; // react-toastify 스타일

function App() {
  return (
    <AuthProvider> {/* AuthProvider로 앱을 감쌉니다 */}
            <Router>
                <div>
                <ToastContainer /> {/* ToastContainer 추가 */}
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
                            <li>
                                <AuthContext.Consumer>
                                    {({ isLoggedIn, user, logout }) => (
                                        isLoggedIn ? (
                                            <div>
                                                <span>{user.username}님</span>
                                                <button onClick={logout}>Logout</button>
                                            </div>
                                            
                                        ) : (
                                            <DiscordLoginButton />
                                        )
                                    )}
                                </AuthContext.Consumer>
                            </li>
                        </ul>
                    </nav>
        
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/scrappinglist" element={<ScrappingList />} />
          <Route path="/scrappingdetail/:id" element={<ScrappingDetail />} />
          <Route path="/auth/" element={<Auth />} />
          {/* Private routes */}
          <Route element={<PrivateRoute />}>
            <Route path="/keywordlist" element={<KeywordList />} />
            <Route path="/filteredascrappinglist/:keyword" element={<FilteredAScrappingList />} />
            <Route path="/keywordcreate" element={<KeywordCreate />} />
            <Route path="/keyworddelete" element={<KeywordDelete />} />
            <Route path="/discordmessageactiveupdate/:id" element={<DiscordMessageActiveUpdate />} />
          </Route>
        </Routes>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;
