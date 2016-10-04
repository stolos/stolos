import React from 'react';
import NavLink from './NavLink';
import Project from './Project';

export default function({ projects }) {
    console.log(projects);
    var projectsList = projects.map(function(project, index) {
        console.log(project);
        return (
        <li key = {index} >
            <Project project = { project } />
        </li>
        );
    });
    return (
        <div>
            <h2>Projects</h2>
            <ul>
                {projectsList}
            </ul>
        </div>
    );
}
