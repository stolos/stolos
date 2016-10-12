import React from 'react';
import {Match, Miss, Redirect} from 'react-router';
import Projects from './Projects';
import Project from './Project';

export default function Content({ projects }) {
    console.log('Content.render()');
    return (
        <main className="col-sm-9 col-xl-10">
            <div className="row" id="header">
                <div className="col-xs-12">
                    Stolos Dashboard
                </div>
            </div>
            <div id="content" className="row">
                <Match
                    exactly
                    pattern="/"
                    render={(defaultProps) => <Projects apiUrl="/api/a0.1/projects/" {...defaultProps} />}
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
        </main>
    );
}
