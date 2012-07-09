#! /usr/bin/env python
import subprocess

IFCONFIG = "/sbin/ifconfig"
CMD_IP = "/bin/ip"
CMD_IWCONFIG = "/sbin/iwconfig"
CMD_BRCTL = "/sbin/brctl"
CMD_WPA_PASSPHRASE = "/usr/bin/wpa_passphrase"

def get_wpa_passphrase(ssid, passphrase):
  pipe = subprocess.Popen( CMD_WPA_PASSPHRASE + " " + ssid + " "
          + passphrase, shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
  for l in pipe:
    if l.find("#psk=") != -1:
        continue
    if l.find("psk=") != -1:
      return l.split("psk=")[1].strip()

  raise Exception("No passphrase generated")


def get_interfaces_names():
  res = []
  pipe = subprocess.Popen( CMD_IP + " addr show", shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
  for l in pipe:
    if l.startswith(" "):
      continue
    res.append(l.split(":")[1].strip())
  return res

def is_interface(name):
    interfaces = get_interfaces_names()
    try:
        interfaces.index(name)
        return True
    except ValueError:
        return False

def get_interface_info(name):
  res = {}
  pipe = subprocess.Popen( CMD_IP + " addr show " + name, shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
  firstline = pipe.readline()
  f = firstline
  res["name"] = f.split(":")[1].strip()
  res["flags"] = f[f.index("<")+1:f.index(">")].split(",")
  f = f[f.index(">")+1:].strip().split(" ")
  for i in range(len(f) / 2):
    res[f[i*2]] = f[i*2+1]
  for l in pipe:
    l = l.strip().split(" ")
    for i in range(len(l) / 2):
      res[l[i*2]] = l[i*2+1]
      if l[i*2] == "scope":
        res["scope"] = l[l.index("scope")+1:]
  return res


def get_wifi_interfaces_names():
  res = []
  pipe = subprocess.Popen( CMD_IWCONFIG, shell=True, bufsize=0,
    stdout=subprocess.PIPE, stderr=open('/dev/null', 'w')).stdout
  for l in pipe:
    if l.startswith(" "):
      continue
    if l.find("no wireless") != -1:
      continue # isnt a WiFi device
    res.append(l.split(" ")[0])
  return res


def is_wifi_interface(name):
    wifis = get_wifi_interfaces_names()
    try:
        wifis.index(name)
        return True
    except ValueError:
        return False


def get_wifi_interface_info(name):

  _names = get_wifi_interfaces_names()
  try:
    _names.index(name)
  except ValueError:
    raise Exception("It is not a WiFi device")

  res = {}
  pipe = subprocess.Popen( CMD_IWCONFIG + " " + name, shell=True, bufsize=0,
    stdout=subprocess.PIPE, stderr=open('/dev/null', 'w')).stdout
  cmd_output = ""
  for l in pipe:
    cmd_output = cmd_output + l.strip() + " "

  res["wifi"] = True
  res["name"] = cmd_output.split(" ")[0]
  res["ieee"] = cmd_output.split("IEEE")[1].strip().split(" ")[0]

  try:
    res["frequency"] = cmd_output.split("Frequency:")[1].strip().split(" ")[0]
  except Exception:
    pass

  try:
    res["essid"] = cmd_output.split("ESSID:")[1].strip().split(" ")[0]
  except Exception:
    pass

  res["mode"] = cmd_output.split("Mode:")[1].strip().split(" ")[0]
  try:
    res["access_point"] = cmd_output.split("Access Point:")[1].strip().split(" ")[0]
  except Exception:
    pass

  res["tx_power"] = cmd_output.split("Tx-Power=")[1].strip().split(" ")[0]
  res["retry_long_limit"] = cmd_output.split("limit:")[1].strip().split(" ")[0]
  res["rts_thr"] = cmd_output.split("RTS thr:")[1].strip().split(" ")[0]
  res["fragment_thr"] = cmd_output.split("Fragment thr:")[1].strip().split(" ")[0]

  try:
    res["encryption_key"] = cmd_output.split("Encryption key:")[1].strip().split(" ")[0]
  except Exception:
    pass

  res["power_management"] = cmd_output.split("Power Management:")[1].strip().split(" ")[0]
  return res


def get_bridge_interfaces_names():
  res = []
  pipe = subprocess.Popen( CMD_BRCTL + " show", shell=True, bufsize=0,
    stdout=subprocess.PIPE, stderr=open('/dev/null', 'w')).stdout

  firstline = pipe.readline()
  f = firstline # Nothing to do. It's the header

  for l in pipe:
    if l.startswith("\t"):
      continue
    res.append(l.split("\t")[0])
  return res


def is_bridge(name):
    bridges = get_bridge_interfaces_names()
    try:
        bridges.index(name)
        return True
    except ValueError:
        return False


def get_bridge_interface_info(name):
  res = {}

  pipe = subprocess.Popen( CMD_BRCTL + " show", shell=True, bufsize=0,
    stdout=subprocess.PIPE, stderr=open('/dev/null', 'w')).stdout
  firstline = pipe.readline()
  f = firstline # Nothing to do. It's the header
  bridge_name_found = False

  for l in pipe:
    ll = l.strip()
    lll = l.split("\t")
    if bridge_name_found:
        if lll[0] == "":
            res["interfaces"].append(ll)
        else:
            break
    if lll[0] == name:
        bridge_name_found = True

        while True: # deleting empty items
            try:
              lll.remove("")
            except ValueError:
              break
        try:
            res["name"] = name.strip()
        except Exception:
            pass

        try:
            res["id"] = lll[1].strip()
        except Exception:
            pass

        try:
            _stp = lll[2].strip()
            res["stp"] = True
            if _stp == "no":
              res["stp"] = False
        except Exception:
            pass

        try:
            if lll[3].strip() == "":
              res["interfaces"] = []
            else:
              res["interfaces"] = [lll[3].strip()]
        except Exception:
            pass

  return res


