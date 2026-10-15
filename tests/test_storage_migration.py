#!/usr/bin/env python3
"""Offline proof: all legacy bytes preserved; one primary record source wins."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_state as bs

class StorageCutover(unittest.TestCase):
    def test_every_legacy_file_survives_with_its_sha256(self):
        m=json.loads((ROOT/'migrations/2026-10-15-storage-unification.json').read_text())
        self.assertEqual(m['primary'],'dreamer2664/storagecode')
        self.assertEqual(len(m['files']),m['census_before_cutover']['storage']['tracked_files'])
        for row in m['files']:
            p=ROOT/row['snapshot']
            self.assertTrue(p.is_file(),row['source'])
            self.assertEqual(p.stat().st_size,row['bytes'],row['source'])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'],row['source'])
            if row['canonical']:
                self.assertTrue((ROOT/row['canonical']).is_file(),row['canonical'])

    def test_final_server_frozen_snapshot_and_all_late_records_are_preserved(self):
        m=json.loads((ROOT/'migrations/2026-10-15-storage-unification.json').read_text())
        self.assertTrue(m['legacy_server_archived'])
        self.assertTrue(m['freeze_snapshots'])
        for snap in m['freeze_snapshots']:
            self.assertGreaterEqual(len(snap['files']),len(m['files']))
            for row in snap['files']:
                p=ROOT/row['snapshot']
                self.assertEqual(p.stat().st_size,row['bytes'])
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'],row['source'])
                if row['source']=='PUSHES.md':
                    canonical=(ROOT/'PUSHES.md').read_text()
                    for line in p.read_text().splitlines():
                        if line.startswith('| '):self.assertIn(line,canonical)

    def test_unmerged_legacy_proposals_survive_without_becoming_accepted_code(self):
        m=json.loads((ROOT/'migrations/2026-10-15-storage-unification.json').read_text())
        for snap in m['freeze_snapshots']:
            for pr in snap['pending_prs']:
                meta=json.loads((ROOT/pr['preserved_at']).read_text())
                self.assertEqual(meta['head_sha'],pr['head_sha'])
                self.assertIn('NOT approved',meta['acceptance'])
                self.assertEqual(hashlib.sha256((ROOT/pr['patch_path']).read_bytes()).hexdigest(),pr['patch_sha256'])
                for row in meta['changed_files']:
                    if row['status']!='D':
                        self.assertEqual(hashlib.sha256((ROOT/row['snapshot']).read_bytes()).hexdigest(),row['sha256'])

    def test_primary_is_the_larger_meaningful_content_snapshot(self):
        m=json.loads((ROOT/'migrations/2026-10-15-storage-unification.json').read_text())
        c=m['census_before_cutover']
        self.assertGreater(c['storagecode']['tracked_files'],c['storage']['tracked_files'])
        self.assertGreater(c['storagecode']['bytes']-c['storagecode']['sections']['app']['bytes'],c['storage']['bytes'])
        self.assertGreater(c['storagecode']['sections']['data']['bytes'],c['storage']['sections']['data']['bytes'])

    def test_existing_primary_index_was_not_replaced(self):
        text=(ROOT/'data/INDEX.md').read_text()
        self.assertIn('pipeline build receipts',text)
        self.assertIn('S57 replay receipts',text)
        self.assertIn('legacy/storage/data/INDEX.md',text)

    def test_primary_wins_over_a_conflicting_legacy_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            p,l=Path(td)/'primary',Path(td)/'legacy'
            p.mkdir();l.mkdir()
            (p/'PUSHES.md').write_text('| 2026-10-15 | new | storagecode | abc | PRIMARY |\n')
            (l/'PUSHES.md').write_text('| 2026-10-15 | old | storage | xyz | LEGACY |\n')
            warnings=[]
            chosen=bs.record_root(p,l,warnings)
            rows=bs.parse_pushes(chosen,warnings)
            self.assertEqual(chosen,p)
            self.assertEqual([r['what'] for r in rows],['PRIMARY'])
            self.assertEqual(warnings,[])

    def test_legacy_fallback_is_visible_and_not_a_second_merge_source(self):
        with tempfile.TemporaryDirectory() as td:
            p,l=Path(td)/'primary',Path(td)/'legacy'
            p.mkdir();l.mkdir();(l/'PUSHES.md').write_text('old ledger')
            warnings=[]
            self.assertEqual(bs.record_root(p,l,warnings),l)
            self.assertTrue(any('legacy storage fallback' in w for w in warnings))

    def test_primary_paths_and_youtube_group_are_live(self):
        self.assertTrue((ROOT/'PUSHES.md').is_file())
        self.assertTrue((ROOT/'shifts/TEMPLATE.md').is_file())
        self.assertTrue((ROOT/'chronicle').is_dir())
        self.assertEqual(bs.group_of({'tags':['video-training','youtube']},{}),'youtube')
        self.assertIn('only writable shared archive',(ROOT/'STORAGE_POLICY.md').read_text())

if __name__=='__main__':unittest.main(verbosity=2)
