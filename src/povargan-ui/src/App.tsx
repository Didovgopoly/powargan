import React, {Component} from 'react';
import './App.css';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Form} from "react-bootstrap";

interface State {
  request: string;
  data?: string;
}

class App extends Component<any, State> {
  constructor(props: any) {
    super(props);
    this.state = {request: ''};

    this.handleChange = this.handleChange.bind(this);
    this.executeRequest = this.executeRequest.bind(this);
  }

  handleChange(event: any) {
    this.setState({request: event.target.value});
  }

  executeRequest() {
    var url = process.env.REACT_APP_BACKEND_URL + "generate-image";
    fetch(url,      {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      //make sure to serialize your JSON body
      body: JSON.stringify({
        text: this.state.request,
      })
    })
    .then(response => response.json())
    .then(json => {
      console.log('received image', json.id)
      this.setState({data: json.img})
    }).catch((err) => {
    console.log(err);
  });
    // fetch(process.env.REACT_APP_BACKEND_URL + "generate-image")
    //   .then(response => response.json())
    //   .then(json => {
    //     console.log('received image', json.id)
    //     this.setState({data: json.img})
    //   });
  }

  render() {
    return (
      <div className="container">
        <div className="row mt-5">
          <h1>Генерирую картинку блюда по тексту рецепта</h1>
          <p className="lead">Вставь текст рецепта с ингридиентами в поле ниже и нажми "Сгенерировать картинку"</p>
        </div>
        <div className="row">
          <div className="col-6">
            <Form>
              <Form.Group controlId="exampleForm.ControlTextarea1">
                <Form.Control as="textarea" rows={10} onChange={this.handleChange}/>
              </Form.Group>
            </Form>
            <Button variant="light" onClick={this.executeRequest} size="lg">
              Сгенерировать картинку
            </Button>
          </div>
          <div className="col-6">
            {this.state.data && <img src={`data:image/jpeg;base64,${this.state.data}`}/>}
          </div>
        </div>
      </div>
    )
  }
}

export default App;
