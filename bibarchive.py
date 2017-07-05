#!/usr/bin/env python

"""
Add this to /usr/local/bin/webkit2png:422:

AppKit.NSBundle.mainBundle().infoDictionary()['NSAppTransportSecurity'] = dict(NSAllowsArbitraryLoads = True)

Cannot be included in this file, because AppKit
is not visible from within this virtualenv.
"""

import distutils.spawn
import glob
import os
import re
import subprocess


DIR = 'Quellenarchiv'


program = distutils.spawn.find_executable('webkit2png')
if not program:
    raise RuntimeError('I need webkit2png.')

if not os.path.isdir(DIR):
    os.makedirs(DIR)

bibstr = '\n'.join([open(bib, 'r').read() for bib in glob.glob('*.bib')])
is_online = False
names = []
urls = []
for line in bibstr.splitlines():
    match = re.match(r'\@online.*\{(\S+),', line)
    if match:
        names.append(match.group(1))
        is_online = True
    match = re.match(r'\s+url[^date].*\{(\S+)\}', line)
    if match and is_online:
        urls.append(match.group(1))

assert len(names) == len(urls)

for name, url in zip(names, urls):
    if len(glob.glob(f'{DIR}{os.sep}*{name}*')) > 0:
        # Skip if file (with some unkown/not-relevant date) exists.
        continue

    subprocess.check_call([
        'webkit2png',
        f'--dir={DIR}',
        f'--filename={name}',
        '--datestamp',
        '--fullsize',
        '--ignore-ssl-check',
        url,
    ])

