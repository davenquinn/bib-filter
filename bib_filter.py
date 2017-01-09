#!/usr/bin/env python

import click
import bibtexparser
from os import path
from re import compile

file_ = click.File('r')
patterns = {
    'natbib': r'(?<=^\\citation\{)(.+)(?=\})',
    'biblatex': r'(?<=\\abx@aux@cite\{)(.+)(?=\})'
}

def parse_list(keyfile):
    return (k.strip() for k in keyfile.readlines())

def parse_aux(auxfile, backend='natbib'):
    """
    Gets citations from aux file. Doesn't work with
    biblatex as yet.
    """
    pattern = compile(patterns[backend])
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
@click.option('--natbib','backend',flag_value='natbib', default=True)
@click.option('--biblatex', 'backend',flag_value='biblatex')
def cli(library,outfile,keys=None,aux=None, clean=False, backend='natbib'):

    db = bibtexparser.load(library)

    _keys = []
    if keys is not None:
        _keys += list(parse_list(keys))
    if aux is not None:
        _keys += list(parse_aux(aux, backend=backend))
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
