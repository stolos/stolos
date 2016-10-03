// modules/About.js
import React from 'react'
import ProjectsList from './ProjectsList';

export default function(props) {
	console.log('Projects.render()');
	return (
		<div>
            <ProjectsList { ...props } />
		</div>
	)
}
