# Weather Station

## systemd script
```
[Unit]
Description=Haho House Weather App
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
WorkingDirectory=/home/david/weather-station
ExecStart=/home/david/weather-station/bin/python3 /home/david/weather-station/main.py

[Install]
WantedBy=multi-user.target
```
