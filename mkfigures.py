#!/usr/bin/env python3

import distutils.spawn
import os
import subprocess
import sys

import utils


SVG_CONVERT = distutils.spawn.find_executable('rsvg-convert')
DOKU_REPO = '../mes.wiki'
DOKU_DIR = os.path.join(DOKU_REPO, 'doku')


if not os.path.exists(DOKU_REPO):
    print(f'No such file or directory: {DOKU_REPO}')
    print(f'git clone https://gitlab.com/kaikuehne/mes.wiki {DOKU_REPO}')
    sys.exit(1)


if not SVG_CONVERT:
    subprocess.call(
        'brew install librsvg &> /dev/null || \\'
        'sudo apt-get install librsvg2-bin',
        shell=True
    )
    SVG_CONVERT = distutils.spawn.find_executable('rsvg-convert')


if SVG_CONVERT:
    with utils.ModDB('.mkfigures') as db:
        svg_files = subprocess.check_output(f'find {DOKU_DIR} -name "*.svg"', shell=True)
        svg_files = [svg.decode('utf-8') for svg in svg_files.strip().split(bytes(os.linesep, 'utf-8'))]
        svg_files = filter(db.has_changed, svg_files)
        for svg in svg_files:
            target = str(svg).replace(DOKU_DIR + os.sep, '').replace('.svg', '.pdf')
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            cmd = f'rsvg-convert -f pdf -o {target} {svg}'
            print(cmd)
            subprocess.call(cmd, shell=True)

