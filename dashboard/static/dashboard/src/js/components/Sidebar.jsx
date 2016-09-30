import React, { Component } from 'react';
import { IndexLink } from 'react-router'
import NavLink from './NavLink'

export default class Sidebar extends Component{
	render() {
		console.log('Sidebar.render()');
		return (
			<div className="col-sm-3" id="sidebar">
				<ul role="nav">
					<li><IndexLink to="/" activeClassName="active">Home</IndexLink></li>
					<li><NavLink to="/projects">Projects</NavLink></li>
				</ul>
			</div>
		)
	}
};
