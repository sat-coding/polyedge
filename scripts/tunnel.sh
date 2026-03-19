#!/usr/bin/env bash
set -e
/data/.openclaw/workspace/.bin/cloudflared tunnel --url http://127.0.0.1:3000
