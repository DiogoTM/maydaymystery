import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from pipeline import label_date, references, image_hash, sha, RESEARCH, ROOT

class EvidenceTests(unittest.TestCase):
    def test_dates_are_validated(self):
        self.assertEqual(label_date('1989-05-01_page24.jpg'),'1989-05-01')
        self.assertIsNone(label_date('1989-02-30.jpg'))
        self.assertIsNone(label_date('preview.jpg'))

    def test_reference_uncertainty(self):
        r=references('ADW, 5/1/89; ADW, 5/1/06; 99/32/1989')
        self.assertEqual(r[0]['target_date'],'1989-05-01')
        self.assertTrue(r[0]['explicit_adw'])
        self.assertIsNone(r[1]['target_date'])
        self.assertEqual(r[1]['status'],'ambiguous_century')
        self.assertEqual(len(r),2)

    def test_perceptual_hash_not_byte_identity(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.png';b=Path(d)/'b.png'
            im=Image.new('L',(256,256),255);ImageDraw.Draw(im).rectangle((30,70,120,200),fill=0)
            im.save(a);im.resize((512,512)).save(b)
            self.assertNotEqual(sha(a),sha(b))
            self.assertLessEqual((int(image_hash(a)[1],16)^int(image_hash(b)[1],16)).bit_count(),4)

    def test_recovered_scans_match_remote_blobs(self):
        rows=json.loads((RESEARCH/'reports/inventory.json').read_text())
        scans=[r for r in rows if r['local'] and r['collection'] in ('archive_scan','researcher_scan')]
        self.assertGreater(len(scans),0)
        for r in scans:
            b=(ROOT/r['path']).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),r['remote_git_blob'])
            self.assertEqual(hashlib.sha256(b).hexdigest(),r['sha256'])

    def test_every_accessible_scan_has_ocr(self):
        rows=json.loads((RESEARCH/'reports/inventory.json').read_text())
        for r in rows:
            if r['local'] and r['collection'] in ('archive_scan','researcher_scan'):
                p=RESEARCH/'corpus'/(r['sha256']+'.json')
                self.assertTrue(p.exists(),r['path'])
                d=json.loads(p.read_text());self.assertEqual(d['source_sha256'],r['sha256'])
                self.assertIn('words',d);self.assertEqual(d['extraction_status'],'machine_unreviewed')

if __name__=='__main__': unittest.main()
