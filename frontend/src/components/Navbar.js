import React from 'react';
import { Navbar, Nav, Form, FormControl, Button, NavbarOffcanvas } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const CustomNavbar = ({ isLoggedIn }) => {
    const navigate = useNavigate();

    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand onClick={() => navigate('/articles')}>TRESS</Navbar.Brand>
            <Nav className="mr-auto">
                <Nav.Link href="#">최신글</Nav.Link>
                <Nav.Link href="#">인기글</Nav.Link>
            </Nav>
            <Form inline className="mx-auto">
                <FormControl type="text" placeholder="search" className="mr-sm-2" />
                <Button variant="outline-dark">🔍</Button>
            </Form>
            <div>
                {isLoggedIn ? (
                    <Button variant="dark" onClick={() => navigate('/accounts/logout')}>Logout</Button>
                ) : (
                    <>
                        <Button variant="dark" className="mr-2" onClick={() => navigate('/accounts/signup')}>Signup</Button>
                        <Button variant="dark" onClick={() => navigate('/accounts/login')}>Login</Button>
                    </>
                )}
            </div>
        </Navbar>
    );
};

export default CustomNavbar;
