# Cài đặt Exporter và Grafana agent monitor Postgresql 
## 1. Cài đặt Postgresql
- https://news.cloud365.vn/huong-dan-cai-dat-postgresql-tren-ubuntu-20-04/

## 2. Cài đặt Postgresql Exporter
- Cài đặt docker
    + https://docs.docker.com/engine/install/ubuntu/
- Change password postgres user
    + https://stackoverflow.com/questions/12720967/how-to-change-postgresql-user-password
    + `sudo -u postgres psql`
    
    ```
    postgres=# \password postgres
    Enter new password: <new-password>
    postgres=# \q
    ```
- Cài đặt Postgresql Exporter
    + https://github.com/prometheus-community/postgres_exporter
    
```
docker run \
--net=host \
-e DATA_SOURCE_NAME="postgresql://postgres:fptcloud123@localhost:5432/?sslmode=disable" \
quay.io/prometheuscommunity/postgres-exporter
```
### Using systemd
- https://schh.medium.com/monitoring-postgresql-databases-using-postgres-exporter-along-with-prometheus-and-grafana-1d68209ca687

- `wget https://github.com/prometheus-community/postgres_exporter/releases/download/v0.10.1/postgres_exporter-0.10.1.linux-amd64.tar.gz`

## 3. Cài đặt Grafana Agent
- https://grafana.com/docs/agent/latest/getting-started/
- `mkdir /etc/agent`
- `touch /etc/agent/agent.yaml`
```
docker run \
  -v /tmp/agent:/etc/agent/data \
  -v /etc/agent/agent.yaml:/etc/agent/agent.yaml \
  grafana/agent:v0.23.0
```




