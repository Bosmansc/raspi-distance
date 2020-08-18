import sys
import socket
import argparse
from struct import pack

version = 0.3

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {		'info'     : '{"system":{"get_sysinfo":{}}}',
                    'on'       : '{"system":{"set_relay_state":{"state":1}}}',
                    'off'      : '{"system":{"set_relay_state":{"state":0}}}',
                    'ledoff'   : '{"system":{"set_led_off":{"off":1}}}',
                    'ledon'    : '{"system":{"set_led_off":{"off":0}}}',
                    'cloudinfo': '{"cnCloud":{"get_info":{}}}',
                    'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
                    'time'     : '{"time":{"get_time":{}}}',
                    'schedule' : '{"schedule":{"get_rules":{}}}',
                    'countdown': '{"count_down":{"get_rules":{}}}',
                    'antitheft': '{"anti_theft":{"get_rules":{}}}',
                    'reboot'   : '{"system":{"reboot":{"delay":1}}}',
                    'reset'    : '{"system":{"reset":{"delay":1}}}',
                    'energy'   : '{"emeter":{"get_realtime":{}}}'
                    }

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
# Python 3.x Version
if sys.version_info[0] > 2:
    def encrypt(string):
        key = 171
        result = pack('>I', len(string))
        for i in string:
            a = key ^ ord(i)
            key = a
            result += bytes([a])
        return result

    def decrypt(string):
        key = 171
        result = ""
        for i in string:
            a = key ^ i
            key = i
            result += chr(a)
        return result

# Parse commandline arguments
# parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
# parser.add_argument("-t", "--target", metavar="<hostname>", required=True, help="Target hostname or IP address", type=validHostname)
# parser.add_argument("-p", "--port", metavar="<port>", default=9999, required=False, help="Target port", type=validPort)
# parser.add_argument("-q", "--quiet", dest='quiet', action='store_true', help="Only show result")
# parser.add_argument("--timeout", default=10, required=False, help="Timeout to establish connection")
# group = parser.add_mutually_exclusive_group(required=True)
# group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)
# group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")
# args = parser.parse_args()


# Set target IP, port and command to send
ip = '192.168.0.211'
port = 9999
cmd_on = commands['on']
cmd_off = commands['off']
timeout = 10

# Send command and receive reply
try:
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.settimeout(timeout)
    sock_tcp.connect((ip, port))
    sock_tcp.settimeout(None)
    sock_tcp.send(encrypt(cmd_on))
    sock_tcp.send(encrypt(cmd_off))
    sock_tcp.send(encrypt(cmd_on))
    sock_tcp.send(encrypt(cmd_off))
    data = sock_tcp.recv(2048)
    sock_tcp.close()

    decrypted = decrypt(data[4:])

    print(decrypted)
    print("Sent:     ", cmd_off)
    print("Received: ", decrypted)

except socket.error:
    quit("Could not connect to host " + ip + ":" + str(port))