import re
import json
import time
from urllib.parse import unquote
from urllib.parse import urlparse
import pandas as pd

# PATTERN = r'^(GET|get|POST|post)\s(.*)(HTTP/\d{1}.\d{1})'
# URL_PUNCTUATIONS = '/+?&;=,()<>*!$#|^{}\~@.`[]:\'\"'

### Detecting URL encoding format

# PATH_TRANSFORMATIONS = [ [r'[a-zA-z0-9\-\_]+', 'PathString']]
# URL_ENCODED_PATTERN = r'.*\%[0-9a-fA-f]{2}.*'

QUERY_NUMBER_TRANSFORMATION = r'^[0-9]+'
QUERY_PURE_STR_TRANSFORMATION = r'^[a-zA-Z\-\_]+$'
# QUERY_UNICODE_STR_TRANSFORMATION = r'[\w]+'
QUERY_UNICODE_STR_TRANSFORMATION = r"[^\u0020-\u007F]+"
# QUERY_HEX_STR_TRANSFORMATION = r'^((0x|0X)?[a-fA-F0-9]{2})+$'
QUERY_HEX_STR_TRANSFORMATION =r"^[a-fA-F0-9]+$"

RestrictedFile_TRANSFORMATION = r"^.*?\b(htaccess|htdigest|htpasswd|asa|asax|ascx|backup|bak|bat|cdx|cer|cfg|cmd|config|conf|csproj|csr|dat|db|dbf|dll|dos|htr|htw|ida|idc|idq|inc|ini|key|licx|lnk|exe|old|mdb|sql|php|pwd|log|nsconfig|svn|bash_history|cs|git|wwwacl|proclog|www_acl|bashrc)\b.*$"


QUERY_RFI_TRANSFORMATION =r"^.*?\b(http|https|ftp|file)\b.*$"

QUERY_LFI_TRANSFORMATION =r"^.*?\b(etc|htpasswd|passwd|system|usr)\b.*$"
# QUERY_XXE_TRANSFORMATION =r"(doctype|entity|system|xmlns)"

QUERY_NULL_CHAR_TRANSFORMATION =  r"(x00|%00)"
QUERY_CRLF_TRANSFORMATION =r"(%0d|%0a)"


QUERY_SQL_KEYWORD_TRANSFORMATION = ['waitfor','delay','space', 'case', 'upper', 'produce', 'primary', 'log', 'between', 'reverse', 'greatest', 'insert', 'outer', 'instr', 'length', 'replace', 'div', 'sqrt', 'set', 'min', 'any', 'group', 'key', 'and', 'inner', 'like', 'create', 'exp', 'top', 'exist', 'left', 'lcase', 'pow', 'rand', 'union', 'log2', 'index', 'is', 'abs', 'as', 'ltrim', 'max', 'having', 'delete', 'mod', 'check', 'select', 'values', 'foreign', 'view', 'concat', 'mid', 'add', 'format',  'substr', 'avg', 'update', 'desc', 'join', 'by', 'round', 'drop', 'strcmp', 'trim', 'database', 'limit', 'rtrim', 'lpad', 'substring', 'rpad', 'count', 'locate', 'asc', 'log10', 'field', 'rownum', 'alter', 'unique', 'constraint', 'column', 'not', 'truncate', 'backup', 'table', 'where', 'all', 'position', 'ucase', 'repeat', 'lower', 'order', 'sum', 'or', 'in', 'into', 'right', 'ascii', 'distinct', 'from', 'null', 'floor', 'least', 'exec', 'default', 'if', 'else', 'end', 'convert', 'cast', 'information','schema', 'table', 'column', 'tables', 'all','col','comments', 'sleep', 'pg_sleep' ]

QUERY_HTML_KEYWORD_TRANSFORMATION = ['script', 'document','location','cookie','history','body','onchange', 'onerror', 'img', 'onload', 'print', 'onmouseover', 'onfocus', 'onclick', 'onresize','onkeypress','console','svg','onload','div','contentWindow','img-src','autofocus','http-equiv', 'www','com','window']

QUERY_JAVASCRIPT_TRANSFORMATION =['javascript','alert', 'throw', 'script','src','elem',  'setTimeout', 'document','.cookie','domain', 'appendChild','createElement','write','getElementById','createElement','createEvent','innerHTML','function()','responseText','lookupMethod', 'location.href','herf.iframe','fromCharCode','vbscript','expression','text','background','image','css','XSS','STYLE','behavior','base64','confirm','eval','prompt','confirm','data','set','cookie','xss']

QUERY_OS_COMMAND_TRANSFORMATION = ['useradd', 'snap', 'hash', 'history', 'shasum', 'shutdown', 'chown', 'whatis', 'source', 'ps', 'shred', 'tar', 'echo', 'set', 'pwd', 'test', 'service', 'man', 'type', 'zip', 'netstat', 'ping', 'readarray', 'sudo', 'stat', 'sha1sum', 'userdel', 'exit', 'rm', 'who', 'apt', 'rmdir', 'top', 'vi', 'wc', 'which', 'until', 'locale', 'patch', 'times', 'export', 'scp', 'awk', 'base64', 'dpkg', 'alias', 'nano', 'printf', 'pushd', 'pacman', 'systemctl', 'neofetch', 'sha256sum', 'paste', 'timedatectl', 'dir', 'cd', 'nc', 'sh', 'unalias', 'tail', 'chsh', 'ssh', 'ss', 'touch', 'bash', 'grep', 'less', 'whoami', 'chmod', 'wget', 'curl', 'du', 'mv', 'unzip', 'perl', 'time', 'unset', 'sha512sum', 'batch', 'cp', 'hostnamectl', 'df', 'systemd', 'kill', 'wait', 'head', 'uname', 'popd', 'apt-get', 'telnet', 'hostname', 'tee', 'passwd', 'mkdir', 'read', 'python3', 'find', 'umask', 'variables', 'htop', 'host', 'su', 'more', 'cat', 'ls', 'sed', 'yum', 'python', 'vim']

DATASET_FEATURES = ["../","..\\","--","/*","*/","&&","||","/","+","?","&",";","=",",","'","\"","(",")","<",">","*","!","$","#","|","^","{","}","\\","%","~","@",".","`","[","]",":","NullChar","SQL","HTML","JavaScript","OSCommand","Number","PureString","HexString","UnicodeString","MixString","LFI","RFI","CRLF","RestrictedFile","Label"]

print(f"Length of DATASET_FEATURES {len(DATASET_FEATURES)}")
# print(f" DATASET_FEATURES {DATASET_FEATURES.index('RestrictedFile')}")
# print(f" DATASET_FEATURES {DATASET_FEATURES[52]}")
DATASET_LABELS = 1

DATASET_PATH = "/home/yoyoo/KLTN/detect_attack_by_reinforcement_learning/data/matrix4/origin/demo.txt"
PARSED_DATASET_PATH = '../data/matrix4/temp/demo.csv'

def parse_data_from_request(request):
    # print("#######################")
    request_transforming_matrix = [0]*(len(DATASET_FEATURES)-1)
    # print(f"len(request_transforming_matrix) {len(request_transforming_matrix)}")
    # request = request.replace('\r', '').strip('\r\n')
    request = request.strip('\r\n')
    fields = request.split('\n')
    if len(fields) < 1:
        print('Invalid request.\n' %(request))
        return []

    data = ''
    # if fields[0].lower().startswith('get'):
    # print("fields", fields)  #fields ['/bmeun223.exe?<meta http-equiv=set-cookie content="testhhwu=7044">']
    # print("fields[0]", fields[0]) # fields[0] /bmeun223.exe?<meta http-equiv=set-cookie content="testhhwu=7044">

    elements = fields[0].split()
    elements = list(filter(None, elements))
    # print("elements",elements)
    for item in  (elements):
        print(f"item {item}")
        #     if elements[0] and elements[0].lower() != 'get':
        #         print('Invalid request.\n' %(request))
        #         return []
        if item:
            data = item.strip()
        else:
            return []
        print("data: ",data)

        # print("-----------")
    
        ### Get URL path and query
        # try:
        #     url = urlparse(data)
        #     data = '%s %s' %(url.path, url.query)
        # except:
        #     print('Invalid URL: %s'%(data))
        
        data = data.lower()
        print("data2: ",data)

        # ################# counter data ############
         ### Find ?
        c = '?'
        request_transforming_matrix[DATASET_FEATURES.index('?')] += data.count(c)
        data = data.replace(c,' ')

        ### Find %0d
        c = "%0d"
        request_transforming_matrix[DATASET_FEATURES.index('CRLF')] += data.count(c)
        data = data.replace(c,' ')

        ### Find %0a
        c = '%0a'
        request_transforming_matrix[DATASET_FEATURES.index('CRLF')] += data.count(c)
        data = data.replace(c,' ')

        ### Find \|0d
        c = '|0d'
        request_transforming_matrix[DATASET_FEATURES.index('CRLF')] += data.count(c)
        data = data.replace(c,' ')

        ### Find 0a\|
        c = '0a|'
        request_transforming_matrix[DATASET_FEATURES.index('CRLF')] += data.count(c)
        data = data.replace(c,' ')

        ### Find %00
        c = "%00"
        request_transforming_matrix[DATASET_FEATURES.index('NullChar')] += data.count(c)
        data = data.replace(c,'')


        ### Find ../
        c = '../'
        request_transforming_matrix[DATASET_FEATURES.index('../')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ..\\
        c = '..\\'
        request_transforming_matrix[DATASET_FEATURES.index('..\\')] += data.count(c)
        data = data.replace(c,' ')

        ### Find --
        c = '--'
        request_transforming_matrix[DATASET_FEATURES.index('--')] += data.count(c)
        data = data.replace(c,' ')

        ### Find /*
        c = '/*'
        request_transforming_matrix[DATASET_FEATURES.index('/*')] += data.count(c)
        data = data.replace(c,' ')

        ### Find */
        c = '*/'
        request_transforming_matrix[DATASET_FEATURES.index('*/')] += data.count(c)
        data = data.replace(c,' ')

        ### Find &&
        c = '&&'
        request_transforming_matrix[DATASET_FEATURES.index('&&')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ||
        c = '||'
        request_transforming_matrix[DATASET_FEATURES.index('||')] += data.count(c)
        data = data.replace(c,' ')

        ### Find /
        c = '/'
        request_transforming_matrix[DATASET_FEATURES.index('/')] += data.count(c)
        data = data.replace(c,' ')

        ### Find +
        c = '+'
        request_transforming_matrix[DATASET_FEATURES.index('+')] += data.count(c)
        data = data.replace(c,' ')

       

        ### Find &
        c = '&'
        request_transforming_matrix[DATASET_FEATURES.index('&')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ;
        c = ';'
        request_transforming_matrix[DATASET_FEATURES.index(';')] += data.count(c)
        data = data.replace(c,' ')

        ### Find =
        c = '='
        request_transforming_matrix[DATASET_FEATURES.index('=')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ,
        c = ','
        request_transforming_matrix[DATASET_FEATURES.index(',')] += data.count(c)
        data = data.replace(c,' ')

        ### Find '
        c = "'"
        request_transforming_matrix[DATASET_FEATURES.index("'")] += data.count(c)
        data = data.replace(c,' ')

        ### Find "
        c = '\"'
        request_transforming_matrix[DATASET_FEATURES.index('\"')] += data.count(c)
        data = data.replace(c,' ')

        ### Find (
        c = '('
        request_transforming_matrix[DATASET_FEATURES.index('(')] += data.count(c)
        data = data.replace(c,' ')

        ### Find )
        c = ')'
        request_transforming_matrix[DATASET_FEATURES.index(')')] += data.count(c)
        data = data.replace(c,' ')

        ### Find <
        c = '<'
        request_transforming_matrix[DATASET_FEATURES.index('<')] += data.count(c)
        data = data.replace(c,' ')

        ### Find >
        c = '>'
        request_transforming_matrix[DATASET_FEATURES.index('>')] += data.count(c)
        data = data.replace(c,' ')

        ### Find *
        c = '*'
        request_transforming_matrix[DATASET_FEATURES.index('*')] += data.count(c)
        data = data.replace(c,' ')

        ### Find !
        c = '!'
        request_transforming_matrix[DATASET_FEATURES.index('!')] += data.count(c)
        data = data.replace(c,' ')

        ### Find $
        c = '$'
        request_transforming_matrix[DATASET_FEATURES.index('$')] += data.count(c)
        data = data.replace(c,' ')

        ### Find #
        c = '#'
        print("------")
        print("b4 #:", data)
        request_transforming_matrix[DATASET_FEATURES.index('#')] += data.count(c)
        data = data.replace(c,' ')
        print("after #:",data)
        print("------")

        ### Find |
        c = '|'
        request_transforming_matrix[DATASET_FEATURES.index('|')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ^
        c = '^'
        request_transforming_matrix[DATASET_FEATURES.index('^')] += data.count(c)
        data = data.replace(c,' ')

        ### Find {
        c = '{'
        request_transforming_matrix[DATASET_FEATURES.index('{')] += data.count(c)
        data = data.replace(c,' ')

        ### Find }
        c = '}'
        request_transforming_matrix[DATASET_FEATURES.index('}')] += data.count(c)
        data = data.replace(c,' ')

        ### Find \\
        c = '\\'
        request_transforming_matrix[DATASET_FEATURES.index('\\')] += data.count(c)
        data = data.replace(c,' ')

        ### Find %
        c = '%'
        request_transforming_matrix[DATASET_FEATURES.index('%')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ~
        c = '~'
        request_transforming_matrix[DATASET_FEATURES.index('~')] += data.count(c)
        data = data.replace(c,' ')

        ### Find @
        c = '@'
        request_transforming_matrix[DATASET_FEATURES.index('@')] += data.count(c)
        data = data.replace(c,' ')

        ### Find .
        c = '.'
        request_transforming_matrix[DATASET_FEATURES.index('.')] += data.count(c)
        data = data.replace(c,' ')

        ### Find `
        c = '`'
        request_transforming_matrix[DATASET_FEATURES.index('`')] += data.count(c)
        data = data.replace(c,' ')

        ### Find [
        c = '['
        request_transforming_matrix[DATASET_FEATURES.index('[')] += data.count(c)
        data = data.replace(c,' ')

        ### Find ]
        c = ']'
        request_transforming_matrix[DATASET_FEATURES.index(']')] += data.count(c)
        data = data.replace(c,' ')

        ### Find :
        c = ':'
        request_transforming_matrix[DATASET_FEATURES.index(':')] += data.count(c)
        data = data.replace(c,' ')

        ### Find &&
        c = '&&'
        request_transforming_matrix[DATASET_FEATURES.index('&&')] += data.count(c)
        data = data.replace(c,' ')

        ### split data
        data = data.split()
        data = list(filter(None, data))
        # print(f"data3: {(data)}")
        ### Find SQLKeyword, OSCommand, Numbers, PureString, UnicodeString, HexString, MixString
        for i in range(0, len(data)):
            print(f"data[{i}]:", data[i])
            
           
            if re.search(QUERY_LFI_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('LFI')] += 1
                print('!! LFI')
            elif re.search(QUERY_RFI_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('RFI')] += 1
                print('!! RFI')
            elif re.search(QUERY_NULL_CHAR_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('NullChar')] += 1
                print('!! NullChar')
            elif re.search(QUERY_CRLF_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('CRLF')] += 1
                print('!! CRLF')
            elif re.search(RestrictedFile_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('RestrictedFile')] += 1 
                print('!! RestrictedFile')

            elif data[i] in QUERY_SQL_KEYWORD_TRANSFORMATION:
                request_transforming_matrix[DATASET_FEATURES.index('SQL')] += 1
                print("!! SQL")
           
            elif data[i] in QUERY_HTML_KEYWORD_TRANSFORMATION:
                request_transforming_matrix[DATASET_FEATURES.index('HTML')] += 1
                print('!! HTML')
            elif data[i] in QUERY_OS_COMMAND_TRANSFORMATION:
                request_transforming_matrix[DATASET_FEATURES.index('OSCommand')] += 1
                print('OSCommand')
            elif data[i] in QUERY_JAVASCRIPT_TRANSFORMATION:
                request_transforming_matrix[DATASET_FEATURES.index('JavaScript')] += 1
                print('JavaScript')
            elif re.fullmatch(QUERY_NUMBER_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('Number')] += 1
                print('!! Number')
            elif re.fullmatch(QUERY_PURE_STR_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('PureString')] += 1
                print('!! PureString')
            elif re.fullmatch(QUERY_HEX_STR_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('HexString')] += 1
                print('!! HexString')
            elif re.fullmatch(QUERY_UNICODE_STR_TRANSFORMATION, data[i]):
                request_transforming_matrix[DATASET_FEATURES.index('UnicodeString')] += 1
                print('!! UnicodeString')
            else:
                request_transforming_matrix[DATASET_FEATURES.index('MixString')] += 1
                print('MixString')

        for i in range(0, len(request_transforming_matrix)):
            if request_transforming_matrix[i] > 255:
                request_transforming_matrix[i] = 255

    # print(" len request_transforming_matrix ", len(request_transforming_matrix))
    # print('%s\n' %request_transforming_matrix)
    # print("#######################")

    return request_transforming_matrix

def read_requests_from_file(file):
    matrix = {}
    for f in DATASET_FEATURES:
        matrix[f] = []
    # print("!!!!!!!!!!__!!!!!!!!!!")
    parsed_lines = 0
    # parsed_file = open(PARSED_DATASET_PATH, "w")
    with open(file,"r") as fi:
        lines = fi.readlines()
        # total_lines = len(lines)
        request = ''
        # print(lines)
        for index, ln in enumerate(lines):
            print(f"ln: {ln} and remain lines {len(lines) - index} and index {index}")
    #         if ln:
    #             # if re.match(PATTERN, ln):
    #         # if request:
                # print(f"ln: {ln}") # ln: /bmeun223.exe?<meta http-equiv=set-cookie content="testhhwu=7044">
            request = ln.strip('\r\n')
            # print(f"request: {request}") # request: /bmeun223.exe?<meta http-equiv=set-cookie content="testhhwu=7044">
            # print("requets in parse_data_from_request ",request)
            ### Put to matrix
            data = parse_data_from_request(request)

            # print("data in parse_data_from_request ", data )
            # print("data in parse_data_from_request ", len(data) )
            for i in range(0, len(DATASET_FEATURES)-1):
                matrix[DATASET_FEATURES[i]].append(data[i])
            matrix[DATASET_FEATURES[-1]].append(DATASET_LABELS)

            parsed_lines += 1
            # request = ''
    #         # request = ln
    #         else:
    #             request = ''
    #             request += ln
    # #         # else:
    # #         #     request += ln
    # request = request.strip('\r\n')
    # print("len requets in parse_data_from_request ",len(request))
    
    # ### Put to matrix
    # data = parse_data_from_request(request)
    # print("^^^^^^^^^^^^^6")

    # print("Put to matrix, 2.1")

    # for i in range(0, len(DATASET_FEATURES)-1):
    #     matrix[DATASET_FEATURES[i]].append(data[i])
    # matrix[DATASET_FEATURES[-1]].append(DATASET_LABELS)

    parsed_lines += 1

    # try:
    #   df = pd.DataFrame(matrix)
    # except:
    #   print("matrix",matrix)
    # print("matrix",matrix)
    # print("len matrix",len(matrix['./']))
    df = pd.DataFrame(matrix)
      

    df.to_csv(PARSED_DATASET_PATH, index=False)
    print("!!!!!!!!!!_99_!!!!!!!!!!")

    return parsed_lines


parsed_lines = read_requests_from_file(DATASET_PATH)

print('%s requests are parsed.' %parsed_lines)