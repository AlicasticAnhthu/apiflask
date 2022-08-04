#!/bin/bash

#############################################################
############ Fill in haproxy_agent configuration ############
#############################################################
username="${USERNAME:-điền user vào đây}"
password="${PASSWORD:-điền pass vào đây}"
uri="${URI:-điền uri vào đây}" # ví dụ http://haproxy.example.com:8404/stats thì điền haproxy.example.com:8404/stats


# Install haproxy_exporter
version="${VERSION:-0.13.0}"
arch="${ARCH:-linux-amd64}"
bin_dir="${BIN_DIR:-/usr/bin}"

source haproxy_agent_config.sh

# Check folder opt
mkdir -p /opt;

# Download haproxy_exporter
wget "https://github.com/prometheus/haproxy_exporter/releases/download/v$version/haproxy_exporter-$version.$arch.tar.gz" \
    -O /opt/haproxy_exporter.tar.gz
echo "Download haproxy_exporter succeeded"

# Check folder haproxy_exporter
mkdir -p /opt/haproxy_exporter;

# move haproxy_exporter to /usr/bin
cd /opt

tar xfz /opt/haproxy_exporter.tar.gz -C /opt/haproxy_exporter || { echo "ERROR! Extracting the haproxy_exporter tar"; exit 1; }

if [ ! -f $bin_dir/haproxy_exporter ]; then
    cp "/opt/haproxy_exporter/haproxy_exporter-$version.$arch/haproxy_exporter" "$bin_dir";
fi 

# check and allow port ufw
status=$(ufw status | grep -c "inactive")
if [ $status == "0" ]; then
    ufw allow from 127.0.0.1 to any port 9101;
fi

if [ ! -f /etc/systemd/system/haproxy_exporter.service ]; then
cat <<EOF > /etc/systemd/system/haproxy_exporter.service
[Unit]
Description=HAProxy Prometheus Exporter
Wants=network-online.target
After=network-online.target
[Service]
User=haproxy_exporter
Group=haproxy_exporter
Type=simple
ExecStart=/usr/bin/haproxy_exporter --web.telemetry-path="/metrics" --web.listen-address=":9101" --haproxy.scrape-uri="http://$username:$password@$uri;csv"
[Install]
WantedBy=multi-user.target
EOF
fi

useradd -rs /bin/false haproxy_exporter

systemctl daemon-reload
systemctl enable haproxy_exporter.service
systemctl start haproxy_exporter.service

echo "SUCCESS! Installation haproxy_exporter succeeded!"
