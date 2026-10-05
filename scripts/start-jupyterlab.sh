#!/usr/bin/env bash
exec uv run --project scripts jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --IdentityProvider.token='' \
    --ServerApp.password='' \
    --ContentsManager.allow_hidden=true