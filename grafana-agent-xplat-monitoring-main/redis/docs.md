# Cài đặt Exporter và Grafana agent monitor Redis
## 1. Cài đặt Redis server
- https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04

## 2. Cài đặt Redis Exporter
- `wget https://github.com/oliver006/redis_exporter/releases/download/v1.35.1/redis_exporter-v1.35.1.linux-amd64.tar.gz`
- `tar -xvzf redis_exporter-v1.35.1.linux-amd64.tar.gz`
- `mv redis_exporter /usr/bin/`
- `vim /etc/systemd/system/redis_exporter.service`
```
[Unit]
Description=Redis Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=redis
Group=redis
Type=simple
ExecReload=/bin/kill -HUP \$MAINPID
ExecStart=/usr/bin/redis_exporter \
  --log-format=txt \
  --namespace=redis \
  --web.listen-address=:9121 \
  --redis.addr="redis://IP_server_redis:6379" \
  --redis.password="password_database_redis" \
  --web.telemetry-path=/metrics
[Install]
WantedBy=multi-user.target                           
```

- `systemctl daemon-reload`
- `systemctl start redis_exporter.service`
- `systemctl enable redis_exporter.service`

## 3. Cấu hình grafana agent
- `docker run -d -v /tmp/agent:/etc/agent/data -v /etc/agent/agent.yaml:/etc/agent/agent.yaml grafana/agent:v0.23.0`
