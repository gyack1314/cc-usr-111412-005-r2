"""用途类别版本与可审查的多对一归并。"""
def mapping(source,target,pairs):
    if set(pairs)-set(source):raise ValueError('映射引用未知来源类别')
    if set(pairs.values())-set(target):raise ValueError('映射引用未知目标类别')
    return dict(pairs)

def reclassify(rows,pairs):
    out=[];unmapped=[]
    for r in rows:
        if r['category'] not in pairs:unmapped.append(dict(r));continue
        out.append(dict(r,category=pairs[r['category']]))
    return out,unmapped
