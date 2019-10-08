import React from 'react';
import logo from './logo.svg';
import './App.css';


var submitForm = function (e) {
    e.preventDefault();
    const data = new FormData(e.target);
    const inF = data.get('inputFile')
    const ouF = data.get('outputFile')

    if (!ouF) {
        alert("Missing output file name")
        return
    }
    fetch('https://wl3de0ty60.execute-api.eu-west-1.amazonaws.com/dev/jobs', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': "*",
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'input': inF,
        'output': ouF,
      })
    }).then((responseJson) => {
        alert("URL to download GIF will be send to the phone subscribed to SNS topic (Kamil's phone) :)")
    });
}

function App() {
  return (
    <div className="App">
      <header className="App-header">

        <form onSubmit={submitForm}>
            <label>You can select of the the following input files:</label>
            <br/>
            <select name="inputFile" id="inputFile">
              <option value="cat2.mp4">cat2.mp4</option>
              <option value="cat_walking.mp4">cat_walking.mp4</option>
            </select>
            <br/>

            <label>Output file name</label>
            <br/>
            <input name="outputFile" id="outputFile"></input>
            <br/>

            <button>Create GIF</button>
        </form>


      </header>
    </div>
  );
}

export default App;
