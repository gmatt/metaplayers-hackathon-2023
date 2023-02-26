import 'bootstrap/dist/css/bootstrap.min.css';

import React from 'react';
import styles from "./App.module.css"
import {Alert, Button, Col, Container, Form, Navbar, Row, Spinner, Stack} from "react-bootstrap";
import * as Icon from 'react-bootstrap-icons';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL

interface Props {
}

class State {
    public query: string = "";
    public loading: boolean = false;
}

class App extends React.Component<Props, State> {
    state = new State();

    submit = async () => {
        await this.setState({...this.state, "loading": true});
        const res = await (await fetch(BACKEND_URL + "/question", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            }, body: JSON.stringify({
                query: this.state.query,
            })
        })).text();
        console.log(res)
        await this.setState({...this.state, "loading": false});
    }

    render() {
        return (
            <div className="App">
                <Row>
                    <Col sm={3} className={styles.nav}>
                        <Container>
                            <Stack gap={3}>
                                <div className="hr"/>
                                <Navbar.Brand href="#home" className="">
                                    <img
                                        alt=""
                                        src="/icon.png"
                                        width="30"
                                        height="30"
                                        className="d-inline-block align-top"
                                        style={{marginLeft: 15, borderRadius: 5}}
                                    />{' '}
                                    <span style={{
                                        color: "white",
                                        fontWeight: "bold",
                                        fontSize: 19,
                                        marginLeft: 5,
                                    }}>JoGPTár</span>
                                </Navbar.Brand>
                                <div className="hr"/>
                                <Button variant="dark">Menu</Button>
                                <Button variant="dark">Options</Button>
                            </Stack>
                        </Container>
                    </Col>
                    <Col sm={9}>
                        <Stack className={styles.main}>
                            <Container className={styles.output}>
                                <Container className="col-md-7 mx-auto">

                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    <Alert variant="light">Hello there</Alert>
                                    <Alert variant="secondary">Hello there</Alert>
                                    {
                                        this.state.loading
                                            ?
                                            <div style={{textAlign: "right", marginRight: 5}}><Spinner/></div>
                                            :
                                            ""
                                    }
                                </Container>
                            </Container>
                            <Container className="col-md-9 mx-auto">
                                <Stack direction="horizontal" gap={3}>
                                    <Form.Control className={`me-auto ${styles.textarea}`}
                                                  placeholder="Ask a question in Hungarian or English..."
                                                  type="textarea"
                                                  value={this.state.query}
                                                  onChange={e => this.setState({
                                                      ...this.state,
                                                      "query": e.target.value
                                                  })}
                                    />
                                    <Button onClick={this.submit}><Icon.Send/>Send</Button>
                                </Stack>
                            </Container>
                        </Stack>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default App;
