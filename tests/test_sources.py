"""当前来源接口的核心和错误路径。"""
import unittest,tempfile
from pathlib import Path
from common import read,Releases,money,digest

class CommonTests(unittest.TestCase):
    def test_snapshot_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            store=Releases(d);raw={'value':'20.10'};key=store.publish(raw)
            self.assertEqual(store.open(key),raw);self.assertEqual(store.publish(raw),key)
            Path(d,key).write_bytes(b'changed')
            with self.assertRaises(ValueError):store.open(key)
    def test_exact_money(self):
        self.assertEqual(str(money('0.1')+money('0.2')),'0.3')
        with self.assertRaises(ValueError):money(float('nan'))

from counts import panels
from taxonomy import mapping,reclassify
class DomainTests(unittest.TestCase):
    def test_scale_and_missing(self):
        d=read();a,b=panels(d);self.assertEqual(a['proportions'],b['proportions']);self.assertNotEqual(a['total'],b['total'])
        d['counts'][0]['observed']=False;self.assertIsNone(panels(d)[0]['proportions'])
    def test_unmapped_not_zero(self):
        rows,unknown=reclassify(read()['counts'],{'office':'text'})
        self.assertEqual(len(rows),2);self.assertEqual(len(unknown),4)
        with self.assertRaises(ValueError):mapping(['a'],['b'],{'a':'c'})
