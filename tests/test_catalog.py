import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog import load
from validate import validate

class CatalogTests(unittest.TestCase):
    def test_catalog_valid(self):
        self.assertEqual(validate(),[])
    def test_seed_import(self):
        self.assertEqual(len(load()),20)
    def test_no_unverified_enterprise_claims(self):
        for t in load():
            if t['verification']!='verified':
                self.assertEqual(t['enterprise_readiness'],'not-assessed')
    def test_unique_ids(self):
        ids=[t['id'] for t in load()]
        self.assertEqual(len(ids),len(set(ids)))

if __name__=='__main__': unittest.main()
