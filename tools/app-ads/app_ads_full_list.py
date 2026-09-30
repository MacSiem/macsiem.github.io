#!/usr/bin/env python3
"""Merge/validate a full authorized seller list captured from Unity's documented UI.

The source is an explicit file supplied by the operator; no partial/stale fallback.
Never deploys. A dated provenance comment records the source file SHA-256.
"""
import argparse
from datetime import date
import hashlib
from pathlib import Path
import re

def directive(line):
    body=line.split('#',1)[0].strip()
    # IAB ads.txt 1.1 variable records (e.g. OWNERDOMAIN) are not seller rows.
    return bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*\s*=\s*\S.*',body))

def seller_rows(text):
    result={}
    for number,line in enumerate(text.splitlines(),1):
        body=line.split('#',1)[0].strip()
        if not body or directive(line):continue
        cells=[x.strip() for x in body.split(',')]
        if len(cells) not in (3,4) or not re.fullmatch(r'[A-Za-z0-9.-]+\.[A-Za-z]{2,}',cells[0]) or not cells[1] or cells[2].upper() not in ('DIRECT','RESELLER'):
            raise ValueError(f'Invalid app-ads.txt seller row at line {number}')
        key=(cells[0].lower(),cells[1],cells[2].upper(),cells[3] if len(cells)==4 else '')
        result[key]=', '.join(key[:3]+((key[3],) if key[3] else ()))
    return result

def merge(existing,full_list,observed_date):
    date.fromisoformat(observed_date)
    expected=seller_rows(full_list)
    if not expected:raise ValueError('Unity full list is empty')
    seller_rows(existing)
    header=f'# Unity full authorized sellers; observed {observed_date}; source sha256 {hashlib.sha256(full_list.encode()).hexdigest()}'
    comments=[s for s in existing.splitlines() if s.lstrip().startswith('#') and not s.startswith('# Unity full authorized sellers;')]
    directives=list(dict.fromkeys(s.strip() for s in existing.splitlines() if directive(s)))
    rows=seller_rows(existing);rows.update(expected)
    return '\n'.join([header,*comments,*directives,*[rows[k] for k in sorted(rows)]])+'\n'

def validate(actual,full_list):
    expected=seller_rows(full_list)
    if not expected:raise ValueError('Unity full list is empty')
    rows=seller_rows(actual)
    return sorted(set(expected)-set(rows))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['merge','check']);p.add_argument('--source',required=True,type=Path)
    p.add_argument('--target',required=True,type=Path);p.add_argument('--observed-date',required=True)
    args=p.parse_args();source=args.source.read_text();actual=args.target.read_text()
    if args.mode=='merge':args.target.write_text(merge(actual,source,args.observed_date))
    missing=validate(args.target.read_text(),source)
    print(f'expected={len(seller_rows(source))} missing={len(missing)}')
    return int(bool(missing))

if __name__=='__main__':raise SystemExit(main())
