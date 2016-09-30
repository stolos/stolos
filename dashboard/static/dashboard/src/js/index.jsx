import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import Content from './components/Content';
import Projects from './components/Projects';
import Project from './components/Project';
import Home from './components/Home';
import NotFound from './components/NotFound';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';


ReactDOM.render(
	<Router history={browserHistory}>
		<Route path="/" component={App}>
			<IndexRoute component={Home}/>
			<Route path="/projects" component={Projects}/>
			<Route path="/projects/:uuid/services" component={Project}/>
		</Route>
		<Route path="*" component={NotFound}/>
	</Router>,
	document.getElementById('root')
)
