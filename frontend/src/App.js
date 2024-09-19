import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CustomNavbar from './components/Navbar';  // 공통 내비게이션 바
import Articles from './components/ArticleList';
import ArticleDetail from './components/ArticleDetail';
import Signup from './components/signup.js';

function App() {
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // 로그인 상태를 확인하는 useEffect
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('There was an error fetching the API message!', error);
      });

    // 로그인 여부를 확인하는 API 예시
    axios.get('/api/is-authenticated')  // 로그인 상태 확인 API 호출
      .then(response => {
        setIsLoggedIn(response.data.isAuthenticated);  // 로그인 여부 설정
      })
      .catch(error => {
        console.error('There was an error checking authentication!', error);
      });
  }, []);

  return (
    <Router>
      {/* 공통 내비게이션 바, 로그인 여부 전달 */}
      <CustomNavbar isLoggedIn={isLoggedIn} />

      {/* 메인 컨텐츠 영역 */}
      <div className="container mt-4">
        <Routes>
          <Route path="/articles" element={<Articles />} />
          <Route path="/articles/:id" element={<ArticleDetail />} />
          <Route path="/accounts/signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
