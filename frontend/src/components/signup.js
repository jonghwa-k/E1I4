import React, { useState } from 'react';
import { Form, Button, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
    const navigate = useNavigate();

    // 상태 관리 (폼 데이터)
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        name: '',
        nickname: '',
        email: '',
        bio: ''
    });

    // 입력 필드 변경 핸들러
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    // 회원가입 제출 핸들러
    const handleSubmit = (e) => {
        e.preventDefault();
        // 회원가입 로직을 여기에 추가 (백엔드 API 연동)
        console.log(formData);

        // 성공 시 로그인 페이지로 이동 (예시)
        navigate('/accounts/login');
    };

    return (
        <Container className="mt-5">
            <h2 className="mb-4 text-center">회원가입</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="ID를 입력하세요."
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
                        placeholder="비밀번호를 입력하세요."
                        required
                    />
                </Form.Group>

                <Form.Group controlId="name">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="이름을 입력하세요."
                        required
                    />
                </Form.Group>

                <Form.Group controlId="nickname">
                    <Form.Label>Nickname</Form.Label>
                    <Form.Control
                        type="text"
                        name="nickname"
                        value={formData.nickname}
                        onChange={handleChange}
                        placeholder="닉네임을 입력하세요."
                        required
                    />
                </Form.Group>

                <Form.Group controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="email을 입력하세요."
                        required
                    />
                </Form.Group>

                <Form.Group controlId="bio">
                    <Form.Label>Bio</Form.Label>
                    <Form.Control
                        as="textarea"
                        name="bio"
                        value={formData.bio}
                        onChange={handleChange}
                        placeholder="자신을 소개해보세요."
                    />
                </Form.Group>

                {/* 버튼들 */}
                <div className="d-flex justify-content-between mt-4">
                    <Button variant="secondary" onClick={() => navigate(-1)}>취소</Button>
                    <Button variant="primary" type="submit">가입완료</Button>
                </div>
            </Form>
        </Container>
    );
};

export default Signup;
