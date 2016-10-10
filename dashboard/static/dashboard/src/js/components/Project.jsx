// modules/About.js
import React from 'react';
import { Link } from 'react-router';

export default function Project({ project : { owner, server, stack, uuid }, deleteProject }) {
    // console.log('project props: ', owner, server, stack, uuid, deleteProject );

    function handleClick() {
        deleteProject(uuid);
    }

    return (
        <div className="m-y-2">
            <div>Project uuid: { uuid } </div>
            <div>Project owner: { owner } </div>
            <div>Stack: { stack.name } </div>
            <div>Server host: { server.host } </div>
            <button onClick={handleClick} className="btn btn--danger">Delete project</button>
            {/*<div>
                <Link to="/" activeOnlyWhenExact activeClassName="active">Back to projects</Link>
            </div>*/}
        </div>
    );
}
