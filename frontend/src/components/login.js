import React, { useState } from 'react';
import { Form, Button, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = ({ setIsLoggedIn }) => {
    const navigate = useNavigate();

    // 상태 관리 (폼 데이터)
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    // 입력 필드 변경 핸들러
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    // 로그인 제출 핸들러
    const handleSubmit = (e) => {
        e.preventDefault();
        
        // API에 로그인 데이터 전송
        axios.post('http://127.0.0.1:8000/api/accounts/login/', formData)
            .then(response => {
                if (response.status === 200) {
                    // 로그인 성공 시 서버에서 받은 토큰을 저장
                    localStorage.setItem('authToken', response.data.token);

                    // 로그인 상태를 업데이트 (네비게이션 바에 반영)
                    setIsLoggedIn(true);

                    // 로그인 성공 시 원하는 페이지로 이동
                    navigate('/articles');
                }
            })
            .catch(error => {
                console.error('Login failed:', error);
            });
    };

    return (
        <Container className="mt-5">
            <h2 className="mb-4 text-center">로그인</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="Enter your username"
                        required
                    />
                </Form.Group>

                <Form.Group controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Enter your password"
                        required
                    />
                </Form.Group>

                {/* 버튼들 */}
                <div className="d-flex justify-content-between mt-4">
                    <Button variant="secondary" onClick={() => navigate(-1)}>취소</Button>
                    <Button variant="primary" type="submit">로그인</Button>
                </div>
            </Form>
        </Container>
    );
};

export default Login;