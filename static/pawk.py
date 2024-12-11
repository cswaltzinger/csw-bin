from sys import argv as args 
from sys import stdin  
import re 

MODE = "DEV"
ORIGINAL_PRINT = print
dquote = "\""
dq=dquote
squote = "\'"
sq=squote

top = False
regex =  r"\s+"
delimiter =  None
fields =  None
top = False


def print(*objects, sep=' ', end='\n', file=None, flush=False):
    if MODE == "DEV":
        ORIGINAL_PRINT(*objects, sep=sep, end=end, file=file, flush=flush)
    else:
        ORIGINAL_PRINT("dev mode is off")

MODE = "DEV"

def is_list_like(obj):
    return isinstance(obj, (list, tuple, set))

def is_iter(obj):
    return hasattr(obj, '__iter__')

def get_key(theDict,val):
    ret = []
    for key, value in theDict.items():
        if val == value:
            return ret.append(key)
    if len(ret) >= 1:
        if len(ret) == 1:
            return ret[0]
        return ret
    return None



cl_args_name = {
    "-d": "delimiter",
    "-f": "fields",
    "-r": "regex",
}

cl_args_value = {
    "regex": r"\s+",
    "delimiter": None,
    "fields": None,
    "top":False 
}
cl_desc = {
    "regex": "The regex to split the input line by",
    "delimiter": "The delimiter to split the input line by",
    "fields": "The fields that the line should be mapped to in order ",
    "top": "If the first line should be treated as the fields",
    "inp": "The raw input line",
    "line": "The raw input (inp) split by the regex",
    "index": "The index or number of the line in the input",
    "args": "A dictionary of the fields in the line",
}
cl_args_type = {
    "regex": str,
    "delimiter": str,
    "fields": str,
    "top": bool,

    "inp": str,
    "line": list,
    "index": int,
    "args": dict,
}

cl_args_desc={ 
   key:{
        "desc":cl_desc.get(key),
        "default":cl_args_value.get(key),
        "type":cl_args_type.get(key),
        "aliases":get_key(cl_args_name,key)
    } for key in cl_desc
}

if len(args) == 1 or "-h" in args or "--help" in args or "help" in args: 
    if len(args) == 1:
        intro = ["fields","delimiter","regex","top"]
        fieldIntro = " | ".join([f'-{item[0]} <{item}>' for item in intro])
        print(f"pawk 'printif <python-bool>,<python-object-to-print>' ")
        print(f"\tprints the <python-object-to-print> if the <python-bool> is true, else it prints nothing\n")
        print(f"pawk [{fieldIntro}] '<python-expression>' ")
        print(f"   vars within <python-expression>: ")
        fieldDesc = ["line","inp","index","args"]
        for key in fieldDesc:
            print(f"\t  |{key:->8}: {cl_desc[key]}")
        print("")
    else:
        if len(args) == 2:
            args =cl_args_desc
        for key in args:
            if key in ["-h", "--help", "help"]:
                continue
            if key in cl_args_desc:
                print(key)
                vals = cl_args_desc[key]
                for key2 in vals:
                    print(f"  {key2:>10}:",vals[key2])
                print("\n")
            
    exit(0)

args = args[1:]
expression = args[-1]
printif = False
if expression.startswith("printif"):
    printif = True
    expression = expression.replace("printif", "")
    while expression[0] in [" ", "\t",":"] and len(expression) > 0:
        expression = expression[1:]
    if len(expression)==0:
        raise Exception("printif must be followed by a condition")
args = args[:-1]




while len(args) > 0 and args[0][0] == '-':
    if "--" in args[0]:
        if "=" in args[0]:
            newArgs= args[0].split("=")
            cl_args_value[newArgs[0].replace("--","")] = newArgs[1]
        else:
            cl_args_value[args[0].replace("--","")] = True
        args = args[1:]
        continue

    if args[0] in cl_args_name:
        cl_args_value[cl_args_name[args[0]]] = args[1]
        args = args[2:]

global_namespace = globals()

for key in cl_args_value:
    global_namespace[key] = cl_args_value[key]


if top:
    fields = stdin.readline()
    fields = fields.strip()
    if delimiter != None:
        fields = [x.strip() for x in fields.split(delimiter) if len(x.strip()) > 0]
        fields = [re.split(regex, field)[0] for field in fields]
    else:
        fields = re.split(regex, fields)
elif fields != None:
    # fields = re.split(regex, fields.strip())
    if delimiter != None:
        fields = [x.strip() for x in fields.split(delimiter) if len(x.strip()) > 0]
        fields = [re.split(regex, field)[0] for field in fields]
    else:
        fields = re.split(regex, fields)



index = 0 
for line in stdin:
    if line == None or (str(line).lower().startswith("None") and len(str(line)) <= 5):
        continue

    args = {}
    # line = line.strip()
    if line.endswith("\n"):
        line = line[:-1]
    raw_line = line 
    # if len(line) == 0 or line =="None":
    #     continue
    #arry of line input strings 
    line = re.split(regex, line.strip())

    
    if fields != None:
        for i in range(len(fields)):
            val = None
            if i < len(line):
                val = line[i]
            global_namespace[fields[i]] = val
            global_namespace[fields[i].lower()] = val
            args[fields[i].lower()] = val

        lastArg = args[fields[-1].lower()]
        restOfLine = raw_line[raw_line.index(lastArg):]
        args[fields[-1].lower()] = restOfLine

    global_namespace["line"] = line 
    global_namespace["inp"] = raw_line 
    global_namespace["index"] = index 
    global_namespace["args"] = args 
    index+=1 

    try:
        # Evaluate the expression using the globals of the calling process
        SHOULD_RUN_EXEC = False
        if expression.count("\n") <= 1:
            try:
                result = eval(expression, global_namespace)
                if type(result) == bool and result:
                    print(raw_line)
                elif printif:
                    prnt = result[0]
                    res =result[1:]
                    if len(res ) == 1:
                        res = res[0]
                    if type(prnt) == bool and prnt:
                        print(res)
                        continue 
                else:
                    print(result)
            except Exception as e:
                SHOULD_RUN_EXEC = True
                # print(e)
                    # print(f"FAILED: {index}","\n")
        else:
            SHOULD_RUN_EXEC = True
            # print("Running exec")
        if SHOULD_RUN_EXEC:
            exec(expression, global_namespace)
    except Exception as e:
        print(f"FAILED: {index}| {line}\n")
        # print(e,"\n")   
        # exp = expression.split("\n")
        # for i in range(len(exp)):
        #     print(i+1, exp[i])
        # print("\n")








