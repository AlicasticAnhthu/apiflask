# Cài đặt Exporter và Grafana agent monitor MongoDB
## 1. Cài đặt MongoDB
- https://viblo.asia/p/cach-cai-dat-va-su-dung-mongodb-co-ban-tren-ubuntu-1804-1VgZvPOO5Aw
- https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04

## 2. Cài đặt MongoDB exporter
- https://devconnected.com/mongodb-monitoring-with-grafana-prometheus/
- `mkdir mongodb-exporter`
- `cd mongodb-exporter`
- `wget https://github.com/percona/mongodb_exporter/releases/download/v0.7.1/mongodb_exporter-0.7.1.linux-amd64.tar.gz`
- `tar -xvzf mongodb_exporter-0.7.1.linux-amd64.tar.gz`
- `useradd -rs /bin/false mongodb`
- `mv mongodb_exporter /usr/local/bin/`

```
use admin
db.createUser(
  {
    user: "mongodb_exporter",
    pwd: "password",
    roles: [
        { role: "clusterMonitor", db: "admin" },
        { role: "read", db: "local" }
    ]
  }
)
```

```
$ db.adminCommand( { shutdown: 1 } )
$ exit
$ sudo mongod --auth --port 27017 --config /etc/mongod.conf &
```

-  `vim /opt/mongodb-exporter/mongodb-exporter.env`

    ```
    MONGODB_URI=mongodb://mongodb_exporter:password@localhost:27017
    ```
- `vim /lib/systemd/system/mongodb_exporter.service`
    ```
    [Unit]
    Description=MongoDB Exporter
    User=mongodb

    [Service]
    Type=simple
    Restart=always
    EnvironmentFile=/opt/mongodb-exporter/mongodb-exporter.env
    ExecStart=/usr/local/bin/mongodb_exporter

    [Install]
    WantedBy=multi-user.target
    ```

    ```
    systemctl daemon-reload
    systemctl start mongodb_exporter.service
    ```








