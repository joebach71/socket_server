import React from 'react';
import './App.css';
import axios from "axios";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      storage: []
    };
  }
  componentDidMount() {
    this.getStorage();
  }
  getStorage = () => {
    axios
      .get("http://localhost:8080/?format=json")
      .then(res => {
        this.setState({ storage: res.data });
      })
      .catch(err => console.log(err));
  };
  renderStorage = () => {
    return this.state.storage.map(entry => (

      <div class="card">
        <div class="card-header" id={`heading${ entry.pk }`}>
            <button class="btn btn-primary" data-toggle="collapse" data-target={`#collapse${ entry.pk }`} aria-expanded="true" aria-controls={`collapse{ entry.pk }`}>
              { entry.key }
            </button>
        </div>

        <div id={`collapse${ entry.pk }`} class="collapse hide" aria-labelledby={`heading${ entry.pk }`} data-parent="#accordion">
          <div class="card-body text-light bg-dark">
            { entry.value }
          </div>
        </div>
      </div>

    ));
  };
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <div id="accordion">
            { this.renderStorage() }
          </div>            
        </header>
      </div>
    );
  }
}

export default App;
