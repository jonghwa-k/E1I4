import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Button, Container, Row, Col } from 'react-bootstrap';

const Articles = () => {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        // API에서 데이터를 가져옴
        axios.get(`http://localhost:8000/api/articles/`)
            .then(response => {
                setArticles(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the articles!", error);
            });
    }, []);

    return (
        <Container>
            {/* 게시글 목록 */}
            <h2 className="my-4">NEWS</h2>
            <Row>
                {articles.map(article => (
                    <Col md={4} key={article.id} className="mb-4">
                        <Card>
                            <Card.Img variant="top" src={article.image_url || 'https://via.placeholder.com/150'} />
                            <Card.Body>
                                <Card.Title>{article.title}</Card.Title>
                                <Card.Text>{article.subtitle}</Card.Text>
                                <Button variant="primary" href={`/articles/${article.id}`}>Read More</Button>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default Articles;
