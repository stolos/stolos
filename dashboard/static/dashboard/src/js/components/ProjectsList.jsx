import React from 'react';
import Project from './Project';

export default function({ projects, deleteProject }) {
    var projectsList = projects.map(function(project, index) {
        return (
            <Project key = {index} project = { project } deleteProject={deleteProject}/>
        );
    });
    if (projectsList.length) {
        return (
            <div className="col-xs-12">
                <h2>Projects</h2>
                <div className="row">
                    <div className="projects-container col-xs-12 m-t-1">
                        {projectsList}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="col-xs-12">
                <h2>Projects</h2>
                <div className="no-projects">
                    You have not created any projects yet
                </div>
            </div>
        );
    }
}
