#!/bin/bash                                                                                                                                                                                               [13/2318]
# Install apache_exporter
version="${VERSION:-0.11.0}"
arch="${ARCH:-linux-amd64}"
bin_dir="${BIN_DIR:-/usr/local/bin}"
# Check folder opt
mkdir -p /opt;                        

# Download apache_exporter
wget "https://github.com/Lusitaniae/apache_exporter/releases/download/v$version/apache_exporter-$version.$arch.tar.gz" \
    -O /opt/apache_exporter.tar.gz     
echo "Download apache_exporter succeeded"
                                                                                                         
# Check folder apache_exporter
mkdir -p /opt/apache_exporter;                

# move apache_exporter to /usr/bin
cd /opt

tar xfz /opt/apache_exporter.tar.gz -C /opt/apache_exporter || { echo "ERROR! Extracting the apache_exporter tar"; exit 1; }

if [ ! -f $bin_dir/apache_exporter ]; then
    cp "/opt/apache_exporter/apache_exporter-$version.$arch/apache_exporter" "$bin_dir";
fi 

# check and allow port ufw
status=$(ufw status | grep -c "inactive")
if [ $status == "0" ]; then
    ufw allow from 127.0.0.1 to any port 9117;
fi

if [ ! -f /etc/systemd/system/apache_exporter.service ]; then
cat <<EOF > /etc/systemd/system/apache_exporter.service
[Unit]
Description=Prometheus
Documentation=https://github.com/Lusitaniae/apache_exporter
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=apache_exporter
Group=apache_exporter
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/local/bin/apache_exporter \
  --insecure \
  --scrape_uri=http://localhost/server-status/?auto \
  --telemetry.address=0.0.0.0:9117 \
  --telemetry.endpoint=/metrics

SyslogIdentifier=apache_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF
fi

useradd -rs /bin/false apache_exporter

systemctl daemon-reload
systemctl enable apache_exporter.service
systemctl start apache_exporter.service

echo "SUCCESS! Installation apache_exporter succeeded!"
