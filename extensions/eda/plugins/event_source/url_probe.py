#!/usr/bin/env python3

"""url_probe.py.

An ansible-rulebook event source plugin that polls a set of URLs and sends
events with their status.

Arguments:
---------
    urls - a list of urls to poll
    delay - the number of seconds to wait between polling
    verify_ssl - verify SSL certificate
    headers - HTTP headers

Example:
-------
    - name: wait for Home Assistant person state changes
      runejuhl.unusual_ansible.url_probe:
        urls:
        - '{{ hass_baseurl }}/api/states/person.rune'
        headers:
          Authorization: 'Bearer {{ hass_token }}'
          content-type: application/json
        delay: 10

"""

import asyncio
from typing import Any

import aiohttp

OK = 200


async def main(queue: asyncio.Queue[Any], args: dict[str, Any]) -> None:
    """Poll a set of URLs and send events with status."""
    urls = args.get("urls", [])
    delay = int(args.get("delay", 1))
    verify_ssl = args.get("verify_ssl", True)
    headers = args.get('headers', {})

    if not urls:
        return

    while True:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                for url in urls:
                    async with session.get(url, verify_ssl=verify_ssl) as resp:
                        json_body = await resp.json()
                        await queue.put(
                            {
                                "url_probe": {
                                    "url": url,
                                    "status": "up" if resp.status == OK else "down",
                                    "status_code": resp.status,
                                    "body": json_body,
                                },
                            },
                        )

        except aiohttp.ClientError as exc:
            client_error = str(exc)
            await queue.put(
                {
                    "url_check": {
                        "url": url,
                        "status": "down",
                        "error_msg": client_error,
                    },
                },
            )

        await asyncio.sleep(delay)


if __name__ == "__main__":
    """MockQueue if running directly."""

    class MockQueue(asyncio.Queue[Any]):
        """A fake queue."""

        async def put(self: "MockQueue", event: dict[str, Any]) -> None:
            """Print the event."""
            print(event)  # noqa: T201

    asyncio.run(main(MockQueue(), {"urls": ["http://redhat.com"]}))
