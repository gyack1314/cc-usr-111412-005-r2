"""观测状态和规模组成的未拟合参考摘要。"""
def panels(data):
    cats=data['taxonomy']['categories'];groups={};seen=set()
    for r in data['counts']:
        key=(r['org'],r['week'],r['category'])
        if key in seen or r['category'] not in cats:raise ValueError('计数重复或未知类别')
        seen.add(key)
        if type(r['observed']) is not bool or type(r['available']) is not bool:raise ValueError('状态必须为布尔值')
        if r['observed'] and (type(r['count']) is not int or r['count']<0):raise ValueError('计数非法')
        if not r['available'] and r['count'] not in (None,0):raise ValueError('不可用类别有非零调用')
        groups.setdefault((r['org'],r['week']),{})[r['category']]=r
    out=[]
    for (org,week),rows in sorted(groups.items()):
        complete=all(c in rows and (not rows[c]['available'] or rows[c]['observed']) for c in cats)
        observed=[r for r in rows.values() if r['available'] and r['observed']]
        total=sum(r['count'] for r in observed)
        fractions={r['category']:r['count']/total for r in observed} if complete and total else None
        out.append({'org':org,'week':week,'complete':complete,'total':total if complete else None,'proportions':fractions,'structural_zero':[c for c,r in rows.items() if not r['available']],'missing':[c for c in cats if c not in rows or (rows[c]['available'] and not rows[c]['observed'])]})
    return out
