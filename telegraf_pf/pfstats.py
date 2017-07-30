#!/usr/local/bin/python2

"""
Script to pull stats from pf (on FreeBSD) and output as JSON for ingestion into
Telegraf/InfluxDB

Notes:
 o Python 2 required due to lack of python3 package on pfSense
 o Full python2 shebang required due to empty path in Telegraf environment.
"""

import json
import re
import subprocess
import sys

if sys.version_info[0] == 3:
	pfout = subprocess.run(['/sbin/pfctl', '-si'], check=True, stdout=subprocess.PIPE).stdout
else:
	pfout = subprocess.check_output(['/sbin/pfctl', '-si'])
pfout = pfout.decode('utf-8').split("\n")

# Set up storage
data = {}
data['states'] = {}

# Regex attempts to grab both available numbers - decimals ignored
stat_re = re.compile("[\sA-Za-z]+(\d+)\s+(\d+)?")
for line in pfout:
	if line.startswith("  current entries"):
		data['states']['count'] = int(stat_re.search(line).group(1))
	if line.startswith("  searches"):
		data['states']['searches'] = int(stat_re.search(line).group(2))
	if line.startswith("  inserts"):
		data['states']['inserts'] = int(stat_re.search(line).group(2))
	if line.startswith("  removals"):
		data['states']['removals'] = int(stat_re.search(line).group(2))

print(json.dumps(data))
