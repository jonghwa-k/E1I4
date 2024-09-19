import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CustomNavbar from './components/Navbar';  // 공통 내비게이션 바
import Articles from './components/ArticleList';
import ArticleDetail from './components/ArticleDetail';
import Signup from './components/signup';
import Login from './components/login';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // 로그인 상태 확인 및 API 호출
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      {/* 공통 내비게이션 바, 로그인 여부 및 로그아웃 핸들러 전달 */}
      <CustomNavbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} />

      {/* 메인 컨텐츠 영역 */}
      <div className="container mt-4">
        <Routes>
          <Route path="/articles" element={<Articles />} />
          <Route path="/articles/:id" element={<ArticleDetail />} />
          <Route path="/accounts/signup" element={<Signup />} />
          <Route path="/accounts/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
