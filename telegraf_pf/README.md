* telegraf_pf

This script parses the output of pfctl and prints structured JSON. Written originally to run on a pfsense appliance and feed Telegraf->InfluxDB

** pfSense Quick Start

1. SSH to appliance, open the shell

2. Download the script to /root/bin, and give execute permissions:
```
mkdir /root/bin
cd /root/bin
fetch https://raw.githubusercontent.com/richardtector/misc-scripts/master/telegraf_pf/pfstats.py
chmod o+x pfstats.py
```

3. Install and enable telegraf:
```
pkg install telegraf
echo 'telegraf_enable=YES' >> /etc/rc.conf
```

4. Add the following to telegraf.conf using your favourite text editor:
```
[[inputs.exec]]
 commands = ["/root/bin/pfstats.py"]
 timeout = "5s"
 name_suffix = "_pf"
 data_format = "json"
```
Whilst there, configure your InfluxDB hostname and credentials.

5. Start telegraf
```
service telegraf start
````
