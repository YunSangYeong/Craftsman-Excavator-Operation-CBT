"""Structural audit only. Does not certify subject-matter correctness."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import unicodedata
import runpy
build = runpy.run_path(str(Path(__file__).with_name('build-bank.py')))['build']

root = Path(__file__).resolve().parents[1]
path = root / 'src/data/questions.json'
bank = json.loads(path.read_text())
normalize = lambda s: re.sub(r'\s+', '', unicodedata.normalize('NFKC', s)).lower()
keys = [normalize('|'.join([q['question'], *sorted(q['choices'])])) for q in bank]
assert len(set(q['id'] for q in bank)) == len(bank)
assert len(set(keys)) == len(bank)
assert len(set(normalize(q['question']) for q in bank)) == len(bank)
assert len(bank) == 1000
assert bank == build(), 'Authored rows do not reproduce the committed JSON'
for q in bank:
    assert q['verificationStatus'] == 'reviewed'
    assert q['year'] is None and q['session'] is None
    assert len(q['choices']) == len(set(map(normalize, q['choices']))) == 4
    assert 1 <= q['answer'] <= 4 and len(q['explanation']) > 30
    assert q['type'] == 'original'
    if q.get('calculation'):
        assert q.get('family') and q['calculation']['precision'] == 2
        assert q['choices'][q['answer']-1].endswith(' '+q['calculation']['unit'])
    else:
        assert not q.get('family')
report = dict(registered=len(bank), internallyReviewed=len(bank), pending=0,
    excludedDuplicates=0, target=1000, shortfall=1000-len(bank),
    types=dict(Counter(q['type'] for q in bank)),
    conceptQuestions=sum(not bool(q.get('calculation')) for q in bank),
    numericVariants=sum(bool(q.get('calculation')) for q in bank),
    numericFamilies=len(set(q['family'] for q in bank if q.get('family'))),
    variantsPerFamily=dict(Counter(q['family'] for q in bank if q.get('family'))),
    subjects=dict(Counter(q['subject'] for q in bank)),
    topics=dict(Counter(q['topic'] for q in bank)),
    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    scope='Structure, exact/normalized duplicates and deterministic reproduction only; not expert review or official syllabus verification')
print(json.dumps(report, ensure_ascii=False, indent=2))
