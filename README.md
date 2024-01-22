# netdata-curl-collector
Netdata custom curl collector.
This collector charts the following [curl reported metrics](https://curl.se/docs/manpage.html):
- time_namelookup
- time_appconnect
- time_connect
- time_total

# Install
1. Copy files to the following folders:  
 - curl_request.chart.py -> /usr/libexec/netdata/python.d/
 - curl_request.conf  -> /etc/netdata/python.d/  

2. Add your desired job urls to the configuration file.  
3. If relevant, enable python.d plugin in netdata configuration (/etc/netdata/netdata.conf):
```
[plugins]
        . . .
         python.d = yes
        . . .
```
4. Restart netdata: `sudo systemctl status  netdata`

# Troubleshoot
```sh
# Switch to netdata user:
sudo -u netdata -s
# Execute the collector ad-hoc in debug mode:
/usr/libexec/netdata/plugins.d/python.d.plugin curl_request debug trace nolock
```
