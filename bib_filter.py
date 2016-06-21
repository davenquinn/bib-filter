#!/usr/bin/env python

import click
import bibtexparser
from shutil import copy
from os import path
from re import compile

file_ = click.File('r')
pattern = compile(r'(?<=^\\citation\{)(.+)(?=\})')

def parse_list(keyfile):
    return (k.strip() for k in keyfile.readlines())

def parse_aux(auxfile):
    """
    Gets citations from aux file. Doesn't work with
    biblatex as yet.
    """
    for l in auxfile.readlines():
        key = pattern.search(l)
        if key is None: continue
        yield key.group(0)

@click.command()
@click.argument('library',type=file_)
@click.argument('outfile',type=click.File('w', encoding='utf-8'))
@click.option('--keys','-k', type=file_)
@click.option('--aux','-a', type=file_)
@click.option('--clean', is_flag=True, default=False)
def cli(library,outfile,keys=None,aux=None, clean=False):

    db = bibtexparser.load(library)

    _keys = []
    if keys is not None:
        _keys += list(parse_list(keys))
    if aux is not None:
        _keys += list(parse_aux(aux))
    _keys = set(_keys)
    click.echo(" ".join(_keys))

    db.entries = [e for e in db.entries
        if e['ID'] in _keys]

    if clean:
        for entry in db.entries:
            entry.pop('file', None)

    bibtexparser.dump(db, outfile)

if __name__ == '__main__':
    cli()
