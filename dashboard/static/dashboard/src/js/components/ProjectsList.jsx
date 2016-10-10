import React from 'react';
import NavLink from './NavLink';
import Project from './Project';

export default function({ projects, deleteProject }) {
    console.log(deleteProject);
    var projectsList = projects.map(function(project, index) {
        // console.log(project);
        return (
        <li key = {index} >
            <Project project = { project } deleteProject={deleteProject}/>
        </li>
        );
    });
    return (
        <div className="col-xs-12">
            <h2>Projects</h2>
            <ul>
                {projectsList}
            </ul>
        </div>
    );
}
