#!/usr/bin/env python3

"""websocket.py

An ansible-rulebook event source plugin for receiving events from Home Assistant
via websocket.

FIXME: write some docs, please!

"""

import asyncio
import json
import logging
import os
from typing import Any, Dict

from websockets.asyncio.client import connect

async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    logger = logging.getLogger()
    uri = args.get('uri')
    access_token = args.get('access_token')
    event_types = args.get('event_types', ['*'])
    message_count = 0

    async with connect(uri=uri, logger=logger) as websocket:
        async for message in websocket:
            # logger.debug(f"got '{message}'")

            payload = json.loads(message)
            payload_type = payload.get('type')

            if payload_type == 'auth_required':
                await websocket.send(
                    json.dumps({'type': 'auth',
                                'access_token': access_token,}))
                continue
            elif payload_type == 'auth_ok':
                for event_type in event_types:
                    await websocket.send(
                        json.dumps(
                            {'id': (message_count:=message_count+1),
                             'type': 'subscribe_events',
                             'event_type': event_type,}))
                continue

            await queue.put({
                'payload': payload,
            })

if __name__ == "__main__":
    uri = os.environ.get('HASS_WEBSOCKET_URI')
    access_token = os.environ.get('HASS_ACCESS_TOKEN')

    class MockQueue:
        print(f"Using {uri}")
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), {
        'uri': uri,
        'access_token': access_token,
    }))
