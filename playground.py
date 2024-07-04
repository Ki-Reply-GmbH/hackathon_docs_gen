from pprint import pprint
import json

sys_cont = json.load(open("./system_context.json", "r", encoding="utf-8"))

pprint(sys_cont)