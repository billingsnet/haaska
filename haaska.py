#!/usr/bin/env python3
# coding: utf-8
#
# Alexa Smart Home Skill v3 proxy for Home Assistant
# Forwards directives to HA's /api/alexa/smart_home endpoint
#

import json
import logging
import urllib.request

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def event_handler(event, context):
    with open('config.json') as f:
        config = json.load(f)

    url = config['url'].rstrip('/') + '/alexa/smart_home'
    token = config.get('bearer_token', config.get('password', ''))

    logger.info('Forwarding to %s: %s', url, event.get('directive', {}).get('header', {}).get('name', '?'))

    data = json.dumps(event).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        logger.error('HTTP %s from HA: %s', e.code, body[:500])
        raise
