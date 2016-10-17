import React from 'react';
import {Match, Miss, Redirect} from 'react-router';
import Projects from './Projects';
import Project from './Project';

export default function Content() {
    return (
        <div id="content" className="col-xs-12">
            <div className="row">
                <Match
                    pattern="/"
                    render={(defaultProps) => <Projects apiUrl="/api/a0.1/projects/" {...defaultProps} />}
                    />
            </div>
        </div>
    );
}
