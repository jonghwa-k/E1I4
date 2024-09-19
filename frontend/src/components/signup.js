import React, { useState } from 'react';
import { Form, Button, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

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

    // 상태 관리 (에러 메시지)
    const [errors, setErrors] = useState([]);

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

    // API에 회원가입 데이터 전송
    axios.post('http://127.0.0.1:8000/api/accounts/signup/', formData)
        .then(response => {
            console.log(response.data);

            // 상태 코드로 성공 여부 판단
            if (response.status === 201 || response.status === 200) {
                // 회원가입 성공 시 로그인 페이지로 리다이렉트
                navigate('/accounts/login');
            }
        })
        .catch(error => {
            if (error.response && error.response.data) {
                // 서버에서 반환한 에러 메시지를 상태에 저장
                setErrors(error.response.data.message || ["서버와의 통신에 문제가 발생했습니다."]);
            } else {
                console.error('There was an error!', error);
                setErrors(["서버와의 통신에 문제가 발생했습니다."]);
            }
        });
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

                {/* 에러 메시지 표시 */}
                {errors.length > 0 && (
                    <div className="alert alert-danger mt-3">
                        {errors.map((error, index) => (
                            <p key={index}>{error}</p>
                        ))}
                    </div>
                )}

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