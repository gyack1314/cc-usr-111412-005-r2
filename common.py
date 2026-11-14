"""冻结资料、精确金额和可审计发布的基础接口。"""
from pathlib import Path
from decimal import Decimal,InvalidOperation
from copy import deepcopy
import json,hashlib,os,tempfile

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def money(value):
    if isinstance(value,(float,bool)):raise ValueError('金额须为十进制字符串或整数')
    try:x=Decimal(value)
    except (InvalidOperation,TypeError):raise ValueError('非法金额')
    if not x.is_finite():raise ValueError('非有限金额')
    return x
def read(path='data/source.json'):
    value=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(value,dict):raise ValueError('资料根节点应为对象')
    return value
def latest(rows,key,asof,known='known',revision='revision'):
    selected={}
    for source in rows:
        if source[known]>asof:continue
        r=deepcopy(source);ident=r[key];rev=r.get(revision,1)
        if type(rev) is not int or rev<1:raise ValueError('修订号非法')
        old=selected.get((ident,rev))
        if old is not None and canonical(old)!=canonical(r):raise ValueError('同一修订内容冲突')
        selected[(ident,rev)]=r
    out={}
    for (ident,rev),row in selected.items():
        if ident not in out or rev>out[ident].get(revision,1):out[ident]=row
    return [out[k] for k in sorted(out)]

class Releases:
    def __init__(self,root):self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
    def publish(self,payload):
        raw=canonical(payload);key=hashlib.sha256(raw).hexdigest();p=self.root/key
        if p.exists():self.open(key);return key
        fd,tmp=tempfile.mkstemp(dir=self.root)
        try:
            with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
            os.replace(tmp,p)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
        return key
    def open(self,key):
        if len(key)!=64 or any(c not in '0123456789abcdef' for c in key):raise ValueError('报告身份非法')
        raw=(self.root/key).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=key:raise ValueError('报告正文损坏')
        return json.loads(raw)
