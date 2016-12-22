import React from 'react';
import yaml from 'js-yaml';

export default function Project({
    project : {
        routing_config : {
            domain,
            config : {
                subdomains
            }
        },
        stack : {
            docker_compose_file,
            slug
        },
        uuid
    },
    deleteProject
}) {

    function handleClick() {
        if (window.confirm("Project deletion is irreversible. Continue?")) {
            deleteProject(uuid);
        }
    }

    var yamlConfig = yaml.safeLoad(docker_compose_file);

    var services = [];

    for (var key in yamlConfig.services) {
        if (yamlConfig.services.hasOwnProperty(key)) {
            if (yamlConfig.services[key].ports) {
                var serviceURL = domain.split('.');
                if (subdomains === true) {
                    serviceURL.unshift(key);
                } else {
                    serviceURL[0] = `${serviceURL[0]}-${key}`;
                }
                serviceURL = serviceURL.join('.');
                services.push(
                    <span key={key} className="tag tag-primary m-r-1">
                        <a href={ "http://" + serviceURL } target="_blank">{ key }</a>
                    </span>
                );
            }
        }
    }

    return (
        <div className="card card-block">
            <div className="card-text">
                <div><strong>UUID:</strong> { uuid } </div>
                <div><strong>Public URL:</strong> <a href={ "http://" + domain } target="_blank">{ domain }</a></div>
                <div><strong>Stack:</strong> { slug }</div>
                <div><strong>Services:</strong> { services }</div>
            </div>
            <button onClick={handleClick} className="btn btn--danger m-t-1 pull-xs-right">Delete project</button>
        </div>
    );
}
