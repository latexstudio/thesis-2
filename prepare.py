#!/usr/bin/env python3

import distutils.spawn
import glob
import os
import subprocess
import sys

import utils

from typing import Callable, List, Tuple


DIR_CHAPTERS = os.path.join(os.getcwd(), 'Kapitel')
DOKU_REPO = '../mes.wiki'
DOKU_DIR = os.path.join(DOKU_REPO, 'doku')
PROGRAMS = (
    ('pandoc', 'pandoc', 'pandoc'),
    ('rsvg-convert', 'librsvg', 'librsvg2-bin'),
)


def main():
    if not os.path.exists(DOKU_REPO):
        print(f'No such file or directory: {DOKU_REPO}')
        print(f'git clone https://gitlab.com/kaikuehne/mes.wiki {DOKU_REPO}')
        sys.exit(1)

    install_missing_programs(PROGRAMS)
    make_chapters()
    make_figures()


def install_missing_programs(programs: Tuple[Tuple[str, str, str]]):
    for name, brew_pkg, apt_pkg in programs:
        if not distutils.spawn.find_executable(name):
            subprocess.call(
                f'brew install {brew_pkg} &> /dev/null || sudo apt-get install {apt_pkg}',
                shell=True
            )


def make_chapters():
    make(
        glob.glob(f'{DOKU_DIR}/*-*.md'),
        lambda source: '{}.tex'.format(os.path.join(DIR_CHAPTERS, os.path.basename(source))).strip(),
        'pandoc --normalize --smart --top-level-division=chapter {source} -f markdown -t latex -o "{target}"',
    )


def make_figures():
    files = subprocess.check_output(f'find {DOKU_DIR} -name "*.svg"', shell=True)
    files = [svg.decode('utf-8') for svg in files.strip().split(bytes(os.linesep, 'utf-8'))]
    make(
        files,
        lambda source: str(source).replace(DOKU_DIR + os.sep, '').replace('.svg', '.pdf').strip(),
        'rsvg-convert -f pdf -o {target} {source}',
    )


def make(sources: List[str], targetfn: Callable[[str], str], cmd_tpl: str):
    with utils.ModDB('.prepare.cache') as mdb:
        sources = filter(mdb.has_changed, filter(lambda x: len(x) > 0, sources))
        for source in sources:
            target = targetfn(source)

            if (os.path.exists(target) and
                os.stat(target).st_mtime > os.stat(source).st_mtime):
                print('CONFLICT: Source file was changed since last run, but target file is newer.')
                print(f'Source: {source}')
                print(f'Target: {target}')
                print('Will not override target... skipping.')
                continue

            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            target_rel = os.path.relpath(target, start=os.getcwd())
            print(f'Generating {target_rel}...')

            cmd = cmd_tpl.format(source=source, target=target)
            subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    main()
