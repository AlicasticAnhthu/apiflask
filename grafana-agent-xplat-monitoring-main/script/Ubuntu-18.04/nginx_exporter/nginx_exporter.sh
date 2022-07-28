#!/bin/bash
# Install nginx_exporter
version="${VERSION:-0.10.0}"
arch="${ARCH:-linux_amd64}"
bin_dir="${BIN_DIR:-/usr/local/bin}"

source nginx_agent_config.sh

# Check folder opt
mkdir -p /opt;

# Download nginx_exporter
wget "https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v$version/nginx-prometheus-exporter_${version}_${arch}.tar.gz" \
    -O /opt/nginx-prometheus-exporter.tar.gz
echo "Download nginx-prometheus-exporter succeeded"

# Check folder nginx_exporter
mkdir -p /opt/nginx-prometheus-exporter;

# move nginx_exporter to /usr/local/bin
cd /opt

tar xfz /opt/nginx-prometheus-exporter.tar.gz -C /opt/nginx-prometheus-exporter || { echo "ERROR! Extracting the nginx-prometheus-exporter tar"; exit 1; }

if [ ! -f $bin_dir/nginx_exporter ]; then
    cp "/opt/nginx-prometheus-exporter/nginx-prometheus-exporter" "$bin_dir";
fi 

# check and allow port ufw
status=$(ufw status | grep -c "inactive")
if [ $status == "0" ]; then
    ufw allow from 127.0.0.1 to any port 9113;
fi

if [ ! -f /etc/systemd/system/nginx_exporter.service ]; then
cat <<EOF > /etc/systemd/system/nginx_exporter.service
[Unit]
Description=NGINX Prometheus Exporter
After=network.target

[Service]
Type=simple
User=nginx_exporter
Group=nginx_exporter
ExecStart=/usr/local/bin/nginx-prometheus-exporter \
    --web.listen-address=$ip:9113 \
    --nginx.scrape-uri http://127.0.0.1:81/metrics

SyslogIdentifier=nginx_prometheus_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF
fi

useradd -rs /bin/false nginx_exporter

systemctl daemon-reload
systemctl enable nginx_exporter.service
systemctl start nginx_exporter.service

echo "SUCCESS! Installation nginx_exporter succeeded!"
