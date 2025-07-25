import logo from './logo.svg';
import './App.css';
import {createRoot} from 'react-dom/client'
import Markdown from 'react-markdown'
import React, { useEffect, useState } from 'react';
import axios from 'axios';


function App() {
  const markdown = '# Hi, *Pluto*!'
  
  // get markdown content from http://localhost:3000/UniversitySelectionReport.md, using axios await.
  // Note: You will need to install axios using `npm install axios`
  // and import it at the top of this file.
  // Use the `useEffect` hook to fetch the markdown content when the component mounts.
  // Display the markdown content in the Markdown component.
  const [report, setReport] = useState('');
  // useEffect(() => {
  //   axios.get('http://localhost:8000/UniversitySelectionReport.md') // there is CORS issue with the http-server, 
  //     .then(response => {
  //       setReport(response.data);
  //       console.log('Markdown fetched successfully:', response.data);
  //     })
  //     .catch(error => {
  //       console.error('Error fetching markdown:', error);
  //     });
  // }, []);

  const markdownContent = require('./UniversitySelectionReport.md');
  console.log('Markdown content:', markdownContent);
  
  return (
    <div className="App">
      <header className="App-header">
   
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          University selection report
        </a>
        <Markdown>
          {markdownContent}
        </Markdown>
      </header>
      
    </div>
  );
}

export default App;
