"""Regression checks for matching scope and exported client formats (no network calls)."""
from pathlib import Path
import ipaddress

ROOT = Path(__file__).resolve().parents[1]
NAME = 'ByteDanceCN'
CORE = 'ByteDanceCN'
SAMPLES = ['douyin.com', 'jimeng.jianying.com', 'doubao.com', 'feishu.cn']

def load(path):
    return [line.strip().removeprefix('- ').strip("'\"") for line in path.read_text().splitlines()
            if line.strip() and not line.strip().startswith('#') and line.strip() != 'payload:']

def matches(host, rule):
    kind, value = rule.split(',', 1)
    if kind == 'DOMAIN': return host == value
    if kind == 'DOMAIN-SUFFIX': return host == value or host.endswith('.' + value)
    if kind == 'DOMAIN-KEYWORD': return value in host
    raise AssertionError(rule)

shadow = ROOT / 'rule/Shadowrocket' / NAME
core = load(shadow / (CORE + '.list'))
full = load(shadow / (NAME + '.list'))
domains = load(shadow / (NAME + '_Domain.list'))
assert len(full) == len(set(full)), 'duplicate rules'
expected = set()
for rule in core:
    kind, value = rule.split(',', 1)
    if kind == 'DOMAIN': expected.add(value)
    elif kind == 'DOMAIN-SUFFIX': expected.add('.' + value)
    elif kind != 'DOMAIN-KEYWORD': raise AssertionError(rule)
# An exact rule is redundant if the SAME name already has a suffix rule.
expected = {entry for entry in expected if entry.startswith('.') or '.' + entry not in expected}
assert set(domains) == expected, ('Domain Set changes exact/suffix semantics', set(domains) ^ expected)
for host in SAMPLES:
    assert any(matches(host, r) for r in full), host
for host in ['not-' + h for h in SAMPLES if h.count('.') == 1] + [h + '.example.invalid' for h in SAMPLES]:
    assert not any(matches(host, r) for r in full), ('overmatch', host)
mihomo = load(ROOT / 'rule/Mihomo' / NAME / (NAME + '.yaml'))
if NAME == 'Pinterest':
    converted = {('DOMAIN-SUFFIX,' + x[2:]) if x.startswith('+.') else 'DOMAIN,' + x for x in mihomo}
    assert converted == set(full), 'Mihomo domain provider parity'
else:
    assert set(mihomo) == set(full), 'Mihomo classical provider parity'
print(f'PASS: {NAME} matching, exact/suffix semantics, and client parity')
