import React from 'react';
import ReactDOM from 'react-dom';
import Dashboard from './components/Dashboard';
import { BrowserRouter as Router } from 'react-router';
import $ from 'jquery';

const app = document.getElementById('root');


window.$ = $;

ReactDOM.render(
    <Router basename="/projects">
        <Dashboard />
    </Router>, app
);
