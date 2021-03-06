import React, {Component} from 'react';
import './App.css';
import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Form} from "react-bootstrap";
import { getRandomRecipe } from "./recipes";

interface State {
  title: string;
  ingredients: string;
  steps: string;
  loading: boolean;
  data?: string;
}

class App extends Component<any, State> {
  constructor(props: any) {
    super(props);
    this.state = {title: '', ingredients: '', steps:'', loading: false};

    this.handleTitleChange = this.handleTitleChange.bind(this);
    this.handleIngredientsChange = this.handleIngredientsChange.bind(this);
    this.handleStepsChange = this.handleStepsChange.bind(this);
    this.executeRequest = this.executeRequest.bind(this);
    this.luckyRequest = this.luckyRequest.bind(this);
  }

  handleTitleChange(event: any) {
    this.setState({title: event.target.value});
  }
  handleIngredientsChange(event: any) {
    this.setState({ingredients: event.target.value});
  }
  handleStepsChange(event: any) {
    this.setState({steps: event.target.value});
  }

  executeRequest() {
    this.runRequest(this.state.title,
        this.state.ingredients,
        this.state.steps)
  }
  
  runRequest(title: string, ingredients: string, steps: string){
    this.setState({loading: true}); 
      
    var url = process.env.REACT_APP_BACKEND_URL + "generate-image";
    fetch(url,      {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      //make sure to serialize your JSON body
      body: JSON.stringify({
        title: title,
        ingredients: ingredients,
        steps: steps,
      })
    })
    .then(response => response.json())
    .then(json => {
      console.log('received image', json.id)
      this.setState({data: json.img, loading: false})
    }).catch((err) => {
      this.setState({loading: false})
      console.log(err);
  });
  }
  
  luckyRequest() {
      var recipe = getRandomRecipe()
      var title = recipe[0];
      var ingredients = recipe[1];
      var steps = recipe[2];
      
      this.setState({title: title});
      this.setState({ingredients: ingredients});
      this.setState({steps: steps});
      this.runRequest(title, ingredients, steps)
  }

  render() {
    return (
      <Container> 
        <Row className="mt-5" noGutters>
          <h1>Генерирую картинку блюда по тексту рецепта</h1>
          <p className="lead">Вставь текст рецепта с ингридиентами в поле ниже и нажми "Сгенерировать"</p>
        </Row>
        <Row noGutters>
          <Col xs={6}>
            <Form>
              <Form.Group>
                <Form.Label>Название рецепта</Form.Label>
                <Form.Control type="text" value={this.state.title} onChange={this.handleTitleChange}/>
              </Form.Group>
              <Form.Group>
                <Form.Label>Ингридиенты</Form.Label>
                <Form.Control as="textarea" value={this.state.ingredients} rows={5} onChange={this.handleIngredientsChange}/>
              </Form.Group>
              <Form.Group>
                <Form.Label>Описание шагов приготовления</Form.Label>
                <Form.Control as="textarea" value={this.state.steps} rows={5} onChange={this.handleStepsChange}/>
              </Form.Group>

            </Form>
            
              <Row>
                <Col>
                  <Button variant="light" onClick={this.executeRequest} size="lg">
                  Сгенерировать
                  </Button>
                </Col>
                <Col style={{display: 'flex', justifyContent: 'flex-end'}}>
                  <Button  variant="light" onClick={this.luckyRequest} size="lg">
                  Мне повезёт
                  </Button>
                </Col>
              </Row>
          </Col>
          <Col xs={6} className="pl-4">
            {!this.state.loading && this.state.data && <img src={`data:image/jpeg;base64,${this.state.data}`}/>}
            { this.state.loading &&
             <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%'  }}>
                <Spinner animation="border" variant="primary" />
             </div>
            }
          </Col>
        </Row>
      </Container>
    )
  }
}

export default App;
