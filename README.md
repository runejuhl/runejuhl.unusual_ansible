# Unusual Ansible

A collection of more unusual Ansible plugins.

## Contents

### `hass_websocket` event plugin

Fetch events from Home Assistant using websocket.

### `http_sse` event plugin

Fetch events using HTTP Server-Sent Events (SSE).

### `mqtt` event plugin

Fetch events from MQTT.

Copied from https://github.com/cloin/event-driven-minecraft/ and modified to
work with newer libraries and unmarshal events with JSON payloads.

### `url_probe` event plugin

A clone of `ansible.eda.url_check` that allows setting arbitrary headers and
unmarshals JSON responses.
