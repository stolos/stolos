from requests.exceptions import ConnectionError, HTTPError, Timeout

from sister_watchd import celery_app

from helpers import ceryx


@celery_app.task(bind=True, default_retry_delay=10)
def set_route(self, source, target):
    client = ceryx.Client.get_default()
    try:
        result = client.set_route(source, target)
    except (ConnectionError, Timeout, HTTPError) as exc:
        raise self.retry(exc=exc)
	return {'set': True, 'source': source, 'target': target}


@celery_app.task(bind=True, default_retry_delay=10)
def unset_route(self, source):
    client = ceryx.Client.get_default()
    try:
        result = client.unset_route(source)
    except (ConnectionError, Timeout, HTTPError) as exc:
        raise self.retry(exc=exc)
	return {'unset': True, 'source': source}
