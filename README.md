# Nginx Meiling Proxy

[![CircleCI](https://circleci.com/gh/kennydo/nginx-meiling-proxy.svg?&style=shield)](https://circleci.com/gh/kennydo/nginx-meiling-proxy)

Named after the mythical gatekeeper Hong Meiling, the Nginx Meiling Proxy handles `auth_request`s from your Nginx.

# Usage

Suppose you want to run a service, but you want finer controls over who has access to it. It's easy to accomplish this with Nginx and Meiling!

First, you need to update your Nginx config to include an internal `auth_request` endpoint, and sett `auth_request` for the `location` that you want to protect, like so (assuming you have Meiling running at `127.0.0.1:8000`):
```
server {
    server_name grafana.example.com;
    listen 443 ssl;

    error_page 401 = @error401;

    location @error401 {
        return 302 https://meiling.example.net/oauth;
    }

    location = /nginx/auth_request {
        internal;
        proxy_pass http://127.0.0.1:8000;
        proxy_pass_request_body off;
        proxy_set_header X-Nginx-Host $host;
        proxy_set_header X-Nginx-Request-Method $request_method;
        proxy_set_header X-Nginx-Request-Uri $request_uri;
    }

    location / {
        auth_request /nginx/auth_request;
        auth_request_set $meiling_user $upstream_http_x_meiling_user;

        proxy_set_header X-Webauth-User $meiling_user;
        proxy_pass http://127.0.0.1:8000/;

        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
    }
}
```

Then, create a config file, following the example in [sample_config.toml](config/sample_config.toml).

Then, I run it like so:
```
$ MEILING_CONFIG=~/meiling_config.toml gunicorn meiling:create_app\(\) --reload -b 0.0.0.0:8000 --access-logfile - --log-level info
```
