import React from 'react';
import NavLink from './NavLink';

export default function({ projects }) {
    var projectsList = projects.map(function(project, index) {
        return (
            <li key = {index} >
                <NavLink to={`/${project.uuid}/services`} activeClassName="active">Project {index + 1}</NavLink>
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
