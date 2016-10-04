import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import { BrowserRouter as Router } from 'react-router';
import $ from 'jquery';

const app = document.getElementById('root');


window.$ = $;

$.ajax({
    url : "/api/a0.1/projects/",

})
.done(function( data ) {
    console.log(data);
    ReactDOM.render(
        <Router basename="/projects">
            <App projects = {data}/>
        </Router>, app
    );
});
