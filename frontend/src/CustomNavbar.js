import React from 'react';
import { Navbar, Nav, Form, FormControl, Button } from 'react-bootstrap';

const CustomNavbar = () => {
    return (
        <Navbar bg="light" expand="lg">
        <Navbar.Brand href="#">KH 트렌드</Navbar.Brand>
        <Nav className="mr-auto">
            <Nav.Link href="#">최신글</Nav.Link>
            <Nav.Link href="#">인기글</Nav.Link>
        </Nav>
        <Form inline className="mx-auto">
            <FormControl type="text" placeholder="search" className="mr-sm-2" />
            <Button variant="outline-dark">🔍</Button>
        </Form>
        <div>
            <Button variant="dark" className="mr-2">Signup</Button>
            <Button variant="dark">Login</Button>
        </div>
        </Navbar>
    );
};

export default CustomNavbar;
