import React from 'react';
import { Match } from 'react-router';
import Projects from './Projects';

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
