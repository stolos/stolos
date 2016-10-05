// modules/About.js
import React from 'react';
import { Link } from 'react-router';

export default function Project({ project : { owner, server, stack, uuid } }) {
    console.log('project props: ', owner, server, stack, uuid );
    return (
        <div className="m-y-2">
            <div>Project uuid: { uuid } </div>
            <div>Project owner: { owner } </div>
            <div>Stack: { stack.name } </div>
            <div>Server host: { server.host } </div>
            <button className="btn btn--danger">Delete project</button>
            {/*<div>
                <Link to="/" activeOnlyWhenExact activeClassName="active">Back to projects</Link>
            </div>*/}
        </div>
    );
}
