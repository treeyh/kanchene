#-*- encoding: utf-8 -*-

import json


def encode(obj):
    return json.dumps(str, encoding='utf-8', ensure_ascii=False, skipkeys=False)
    

def decode(str):
    return json.loads(str, encoding='utf-8')
