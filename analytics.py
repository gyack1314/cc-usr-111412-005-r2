"""当前资料的准备入口，不含目标分析模型。"""
import json
from common import read
from counts import panels
def prepare():
    data=read()
    return panels(data)
if __name__=="__main__":print(json.dumps(prepare(),ensure_ascii=False,indent=2))
