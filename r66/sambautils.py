#! /usr/bin/env python
import subprocess

SERVICE_PATH = "service "
SERVICE = "samba"

def restart_service():
  res = subprocess.Popen( SERVICE_PATH + " " + SERVICE + " restart", shell=True, bufsize=0,
    stderr=open('/dev/null', 'w'),
    stdout=open('/dev/null', 'w')).returncode
  return res


