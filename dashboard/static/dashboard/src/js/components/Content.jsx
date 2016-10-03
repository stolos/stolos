import React from 'react';
import { Match, Miss, Redirect } from 'react-router';
import Projects from './Projects';
import Project from './Project';

export default function Content() {
	console.log('Content.render()');
	return (
		<div className="col-sm-9" id="content">
            <div className="row" id="header">Stolos Dashboard</div>
            <Match exactly pattern="/" component={Projects} />
            <Match  pattern="/:uuid/services" component={Project} />
		</div>
	)
}
