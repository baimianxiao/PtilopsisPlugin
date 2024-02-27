# -*- encoding:utf-8 -*-
import json


# 写json文件
def write_json(data, path):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            return True
    except:
        return False


# 读json文件
def get_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            file = file.read()
            return json.loads(file)
    except:
        return False
