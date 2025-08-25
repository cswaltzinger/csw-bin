#!/Users/csw/.config/anaconda3/bin/python
import os 
from sys import argv as args
import google.generativeai as genai
import json 

args = args[1:]

all = False



while args[0].startswith("-"):
    arg = args.pop(0)
    arg = arg.replace("-", "")
    if arg == "all":
        all = True
    if arg == "jack":
        print("jack")
        exit(0)


BLUE="\033[94m"
RESET="\033[0m"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print(e)
    print("Failed to configure model")
    exit(1)



QUESTION="bash split like python string method"
if len(args) > 0:
    QUESTION = " ".join(args)
CONFIG='''
Please, respond to the query with the provided json format below where name is the name of the method or function to be used, usage is  how to use the function in one line of code and example is a full code example of the function in use.  if there are multiple ways of accomplishing the method, simply add them as a different part of the response array.for example if we were to respond with the javascript substring function, the response would look like this: 
[
        {
                "name": "substring", 
                "usage": "str.substring(1, 4)",
                "example":"let str = \"Hello World!\";\\nlet res = str.substring(1, 4);\\nconsole.log(res);"
        }
]
'''


def responseToJSON(text):
    while not (text.endswith("]") or text.endswith("}")):
        text = text[:-1]

    while not (text.startswith("[") or text.endswith("{")):
        text = text[1:]
    text = text.strip()
    return json.loads(text)

def main():
    global QUESTION, CONFIG, model
    MESSAGE = QUESTION + CONFIG


    response = model.generate_content(MESSAGE)
    text = response.text

    try:
        js = responseToJSON(text)
        if type(js) == dict:
            js = [js]
        for index in range(len(js)):
            way = js[index]
            name, usage, example = way["name"], way["usage"], way["example"]
            blueName = f"{BLUE}{name}{RESET}"
            example = example.replace(name, blueName)
            exLines = example.split("\n")
            usage = usage.replace(name, blueName)
            



            if all:
                print(f"{index+1}: {name}\t{usage}{RESET}")
                maxLen = max([len(line) for line in exLines]) 
                print("_"*maxLen)  
                for line in exLines:
                    print(f"{line}")
                print("="*maxLen)  
            else:
                print(f"{index+1}:\t{usage}")

    except Exception as e:
        print(e)
        print("Response text:")
        for line in text.split("\n"):
            print("\t",line)

if __name__ == "__main__":
    main()
    exit(0)