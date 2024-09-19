import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Card, Button } from 'react-bootstrap';

const ArticleDetail = () => {
    const { id } = useParams();
    const [article, setArticle] = useState(null);

    useEffect(() => {
        axios.get(`http://localhost:8000/api/articles/${id}/`)
            .then(response => {
                setArticle(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the article!", error);
            });
    }, [id]);

    if (!article) return <div>Loading...</div>;

    return (
        <Card>
            <Card.Img variant="top" src={article.image} />
            <Card.Body>
                <Card.Title>{article.title}</Card.Title>
                <Card.Text>{article.content}</Card.Text>
                <Button variant="primary">Like ❤️ ({article.like_count})</Button>
            </Card.Body>
        </Card>
    );
};

export default ArticleDetail;