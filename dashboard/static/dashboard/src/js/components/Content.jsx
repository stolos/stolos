import React from 'react';
import {Match, Miss, Redirect} from 'react-router';
import Projects from './Projects';
import Project from './Project';

export default function Content({ projects }) {
    console.log('Content.render()');
    return (
        <div className="col-sm-9" id="content">
            <div className="row" id="header">Stolos Dashboard</div>
            <Match
                exactly
                pattern="/"
                render={(defaultProps) => <Projects projects = {projects} {...defaultProps} />}
                />
            <Match
                pattern={`/:uuid/services`}
                render={(defaultProps) => {
                    var project = projects.filter(function(project) {
                        return (project.uuid === defaultProps.params.uuid);
                    });
                    return <Project project = {project[0]} />;
                }}
                />
        </div>
    );
}
