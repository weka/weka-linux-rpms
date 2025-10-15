# set DOCKER_HOST so docker cli commands will work with podman (for upgrades of older WMS systems)
export DOCKER_HOST=unix:///run/podman/podman.sock
