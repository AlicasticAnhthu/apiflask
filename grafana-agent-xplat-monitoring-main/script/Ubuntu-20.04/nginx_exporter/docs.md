# Document cài đặt Nginx exporter 
- Enable the stub status module
    + Thêm phần sau vào file `/etc/nginx/sites-available/default`
    ```
    server { 
    		listen localhost:81;
    		location /metrics {
    			stub_status on;
    		}
    }
    ```
- Sau đó restart lại nginx
    + `system restart nginx`
- Kiểm tra xem nginx đã listen tại port 81 
    + `curl localhost:81/metrics`
- Điền ip vào file `nginx_agent_config.sh`
- Chạy lệnh `bash nginx_exporter.sh`
