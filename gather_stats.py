import subprocess
import os
import requests


if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")


cmd_info = {
    '_id': "lsblk --nodeps -no serial /dev/sda | md5sum | awk '{ print $1 }'",
    'device': "dmidecode -s system-product-name",
    'os_version': "lsb_release -r | awk '{ print $2 }'",
    'cpu_model': "dmidecode -s processor-version",
    'locale': "echo $LANG",
    'ram': "free -m | grep Mem | awk '{ print $2 }'",
    'hdd_size': "df -H | grep /dev/sda1 | awk '{ print $2 }'"
}

collected = {}

for cmd in cmd_info:
    print cmd_info[cmd]

    proc = subprocess.Popen(cmd_info[cmd], shell=True, stdout=subprocess.PIPE)
    tmp = proc.stdout.read()[0:-1]
    collected[cmd] = tmp

print collected

put = requests.post("https://stats.galliumos.org/new_install/", json=collected)