#! /usr/bin/env python
import subprocess

SERVICE_PATH = "service "
SERVICE = "samba"

def restart_service():
  subprocess.Popen( SERVICE_PATH + " " + SERVICE + " restart", shell=True, bufsize=0,
    stderr=open('/dev/null', 'w'),
    stdout=open('/dev/null', 'w'))

def reload_service():
  subprocess.Popen( SERVICE_PATH + " " + SERVICE + " reload", shell=True, bufsize=0,
    stderr=open('/dev/null', 'w'),
    stdout=open('/dev/null', 'w'))


