import 'bootstrap/dist/css/bootstrap.min.css';

import React from 'react';
import "./App.css"
import styles from "./App.module.css"
import {Alert, Button, Col, Container, Form, Navbar, Row, Spinner, Stack} from "react-bootstrap";
import * as Icon from 'react-bootstrap-icons';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL

interface Props {
}

class State {
    public query: string = "";
    public loading: boolean = false;
    public outputMessages: {
        sender: "user" | "bot",
        content: string,
    }[] = [];
}

class App extends React.Component<Props, State> {
    state = new State();

    submit = async () => {
        const query = this.state.query;
        await this.setState({
            ...this.state,
            query: "",
            loading: true,
            outputMessages: [...this.state.outputMessages, {sender: "user", content: query}],
        });
        let result: string;
        try {
            result = await (await fetch(BACKEND_URL + "/question", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                }, body: JSON.stringify({
                    query,
                })
            })).json();
        } catch (e) {
            await this.setState({
                ...this.state,
                outputMessages: [...this.state.outputMessages, {sender: "bot", content: "Error\n" + String(e)}]
            });
        }
        await this.setState({
            ...this.state,
            loading: false,
            outputMessages: [
                ...this.state.outputMessages,
                {
                    sender: "bot",
                    // @ts-ignore
                    content: result && result.completion,
                }]
        });
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
                                <Button
                                    style={{textAlign: "left"}}
                                    variant="dark"
                                    onClick={() => this.setState(new State())}
                                ><Icon.ArrowClockwise/> Reset</Button>
                                <Button
                                    style={{textAlign: "left"}}
                                    variant="dark" href="https://njt.hu/"
                                    target="_blank"
                                ><Icon.Archive/> Corpus Source</Button>
                                <Button
                                    style={{textAlign: "left"}}
                                    variant="dark"
                                    href="https://github.com/gmatt/metaplayers-hackathon-2023"
                                    target="_blank"
                                ><Icon.Git/> Git Repo</Button>
                            </Stack>
                        </Container>
                    </Col>
                    <Col sm={9}>
                        <Stack className={styles.main}>
                            <Container className={styles.output}>
                                <Container className="col-md-7 mx-auto">
                                    <>
                                        {this.state.outputMessages.map((message, key) => {
                                            if (message.sender === "user") {
                                                return <Alert variant="light" key={key}>{message.content}</Alert>
                                            } else {
                                                return <div className="alert alert-secondary" role="alert"
                                                            dangerouslySetInnerHTML={{__html: message.content}}></div>
                                            }
                                        })}
                                    </>
                                    {
                                        this.state.loading
                                            ?
                                            <div style={{textAlign: "right", marginRight: 5, marginTop: 5}}>
                                                <Spinner/>
                                            </div>
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
                                                  onKeyDown={e => (e.keyCode === 13) && this.submit()}
                                    />
                                    <Button onClick={this.submit}
                                            disabled={!this.state.query.length}><Icon.Send/>Send</Button>
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
