import os
import re
import urllib.parse
import tkinter as tk
from tkinter import filedialog

# Prompt the user to select the input file
root = tk.Tk()
root.withdraw()
input_file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text Files", "*.txt")])
attack_types = ['SQL Injection', 'XSS', 'CRLF', 'Format String','SSCI','External Redirect','Buffer Overflow', 'RFI', 'Path Traversal', 'Remote OS Command Injection']


# Construct the path to the output file in the same directory as the input file
folder_path, input_file = os.path.split(input_file_path)
input = input_file.split('.',1)[0].strip()

# Define the keyword to filter on
xss_payload_pattern = re.compile(r'<script|<textarea|<form|<marquee|<iframe|<frame|<xss|<var|<object|<xml|<button|<embed|<font|<select|<div|<meta|<br|<label|<set|<img|<audio|<video|<svg|<title|<input|<circle|<body|<p|<html|<style|<a|<isindex|<x|<sc|<foo|<object|<link|prompt|alert|javascript:|xss.nasl', flags=re.IGNORECASE)
#test_pattern = re.compile(r'[<|</]\s+(script|textarea|form|marquee|iframe|frame|xss|object|xml|button|embed|div|meta|br|img|audio|video|svg|title|input|circle|body|html|style|a|object|link)', flags=re.IGNORECASE)
#/examples/jsp/cal/login.pl?login=ledgersmb_script_code_exec.nasl&script=-e print "content-type: text/plain\x0d\x0a\x0d\x0a";system(id)&action=logout - 14031
sql_injection_payload_pattern = re.compile(r"\b(or|and)\b\s+\d+|\b(or|and)\b\s+(@@version|EXISTS)|\bselect\b\s+(?:\*|\w+)\s+\bfrom\b|\binsert\b\s+into\b|\bunion\b\s+(?:all\s+)?\bselect\b|\bconcat\b|\border\b\s+by\b|\bgroup\b\s+by\b|\bdelete\b\s+\bfrom\b|union\s+select|union\W+select|\bdrop\b\s+(?:table|database)\b|\bwaitfor\b\s+delay\b|\bbenchmark\b|\b(if)\b\s+\(.+?=.+?\)|\blike\b\s+'.*?'|\b(?:OR|AND)\b\s+(?:(?:(?:\d+\s*[=<>]+\s*\d+)|(?:[a-z_]+\s*[=<>]+\s*[a-z_]+))|(?:\w+\s*=\s*[']?\w+[']?))|['\";]+--.*|(AND|OR|if)\b\s+[?:'|\"|=|like|sleep|1=1|0=0|a=a]", flags=re.IGNORECASE)
####sql_injection_payload_pattern = re.compile(r"\bselect\b.*\bfrom\b|\binsert\b.*\binto\b|\bunion\b.*\bselect\b|\b(or|and)\b.*\blike\b|select\s+from|select\W+from|concat|order\s+by|group\s+by|insert\s+into|waitfor\s+delay|delete\s+from|drop|union\s+select|union\W+select|benchmark|\b(and|AND|or|OR|if)\b\s+[?:'|\"|=|like|sleep|1=1|0=0|a=a]|select\s+[*]|\b(and|or)\b\s+\w+\s*=\s*\w+|(?:or|and)\s+\(.+?=.+?", flags=re.IGNORECASE)
#/top.php?stuff=(1-(select null from (select null) t where 'n681t2ki'='n681t2ki'))
#waitfor+delay
#Pasar+por+caja%27OR%27a%3D%27a <=> Pasar+por+caja'OR'a='a
rfi_payload_pattern = re.compile(r'(http|https)://[a-zA-Z0-9\./-]*\.(php|asp|aspx|jsp)')
restricted_files = re.compile(r'[a-zA-Z0-9\./-]*\.(htaccess|htdigest|htpasswd|asa|asax|ascx|backup|bak|bat|cdx|cer|cfg|cmd|config|conf|csproj|csr|dat\b|db|dbf|dll|dos|htr|htw|ida|idc|idq|inc\b|ini\b|key|licx|lnk|exe|old)', flags=re.IGNORECASE)
#ssci_payload_pattern = re.compile(r'(;|&&|\|\|)(\s+)?(exec|sh|bash|curl|wget|tftp|ftp|nc|python|perl|ruby|sleep|ping|rm|uname|del|&rem|&|#)(\s+)?\(')
path_traversal_payload_pattern = re.compile(r'\.\./|\.\.\\|%2e%2e%2f|%2e%2e.*?|%2e%2e\\|%2e%2e%5c|..%5c|..%2f|..0x5c|/etc/passwd|etc/passwd|\\etc\\passwd|etc/shadow|etc:passwd|usr/bin|%u002e|%u00255c|%u2215|%u2216|%252e|%25%5c|%252f|%255c|%8.8x|%25%5c|\$\(.*?\)|\{.*?\}')
external_redirect_payload_pattern = re.compile(r'http[s]?://(?!localhost|127\.0\.0\.1).*|\/\/.*?redirect_uri=.*')
crlf_payload_pattern = re.compile(r'(%0a|%0d|%0d%0a|%23)')
buffer_overflow_payload_pattern = re.compile(r'\\x[0-9a-fA-F]{2}|&#x[0-9a-fA-F]')
remote_os_command_injection_payload_pattern = re.compile(r'\b(echo|ping|sleep|uname|del|rm|ls|whoami|whois|exit|telnet|nc|curl|wget|bash|ruby|python|perl|netstat|exec|tftp|ftp|ver|&rem|system|shutdown)\b|(sleep|uname|del|rm\b)|\b(id\s*=\s*[^&\s]*)|(^[^&\s]*\s+id\s*=\s*[^&\s]*)|(;|\||&)\s*id\s*($|\||&|\s)', flags=re.IGNORECASE) #loc file.exe
#remote_os_command_injection_payload_pattern = re.compile(r'(;|&&|\|\|)(\s+)?(cat|ls|id|whoami|ping|telnet|nc|curl|wget|bash|sh|ruby|python|perl)(\s+)?\(') \||\$\(|\)|\$\(.*?\)|\{.*?\}|\[.*?\]|[\x0a\x0d](sleep|uname|del|rm)
ssi_payload_pattern = re.compile(r'<!--#|-->#|<!--|-->')
format_string_error_payload_pattern = re.compile(r'%n|%s|%x|%d|%p|%c|%f|%h|%u|%o|%e|%E|%g|%G|%i|%n|%p|%s|%S|%t|%u|%x|%X|%z')
def classify_attack_type1(line):
    if restricted_files.search(line):
        return 'Restricted_files'
    elif rfi_payload_pattern.search(line):
        return 'RFI'
    elif ssi_payload_pattern.search(line):
        return 'SSI'
    elif xss_payload_pattern.search(line):
        return 'XSS'
    elif sql_injection_payload_pattern.search(line):
        return 'SQL_Injection' 
    
    elif external_redirect_payload_pattern.search(line):
        return 'External_Redirect'
    # elif remote_os_command_injection_payload_pattern.search(line):
    #     return 'OSCommand_Injection'
    elif path_traversal_payload_pattern.search(line):
        return 'Path_Traversal'
    elif format_string_error_payload_pattern.search(line):
        return 'Format_String'
    else:
        return 'Unknown'
def decodeurl(payload):
    return urllib.parse.unquote_plus(urllib.parse.unquote(payload))
def split_input(payload):
    if "?" in payload:
        payload = payload.split("?", 1)[1].strip()
        #payload = payload.split(" ", 1)[0].strip()
        if "=" in payload:
            payload = payload.split("=", 1)[1].strip()
        return urllib.parse.unquote_plus(urllib.parse.unquote(payload))
    return ""

# Open the input and output file
with open(input_file_path, 'r',encoding='cp1252', errors='ignore') as input_file:
    # Read each line from the input file
    for line in input_file:
        # if split_input(line) !="":
        #     attack_type = classify_attack_type1(decodeurl(line)) 
        # else:
        #     attack_type = "Unknown"
        attack_type = classify_attack_type1(decodeurl(line)) 
        output_filepath = os.path.join(folder_path, f'{input}_{attack_type}.txt')
        with open(output_filepath, 'a') as f:
            f.write(line + "\n")

# Print a message indicating the output file has been saved
print(f"Filtered to {folder_path}")