// modules/About.js
import React from 'react';
import { Link } from 'react-router';

export default function Project({ project : { owner, server, stack, uuid } }) {
    console.log('project props: ', owner, server, stack, uuid );
    return (
        <div>
            <div>Project uuid: { uuid } </div>
            <div>Project owner: { owner } </div>
            <div>Stack: { stack.name } </div>
            <div>Server host: { server.host } </div>
            <div>
                <Link to="/" activeOnlyWhenExact activeClassName="active">Back to projects</Link>
            </div>
        </div>
    );
}
