#!/usr/bin/env python

import click
import bibtexparser
from os import path
from re import compile
import csv

file_ = click.File('r')
patterns = {
    'natbib': r'\\citation{([\w,]+)}',
    'biblatex': r'\\abx@aux@cite\{(.+)}'
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
        key = pattern.match(l)
        if key is None: continue
        st = key.group(1).strip()
        for s in st.split(','):
            yield s.strip()

def create_abbreviator(journal_abbreviations):
    # Read as tsv file
    r = csv.reader(journal_abbreviations, dialect="excel-tab")
    _ = (i for i in r if len(i)==2)
    abbrevs = {k:v for k,v in _}
    def fn(entry):
        try:
            _ = entry['journal']
            _ = abbrevs[_]
            entry['journal'] = _
        except KeyError:
            pass
        return entry
    return fn


@click.command()
@click.argument('library',type=file_)
@click.argument('outfile',type=click.File('w', encoding='utf-8'))
@click.option('--keys','-k', type=file_)
@click.option('--aux','-a', type=file_)
@click.option('--journal-abbreviations', type=file_)
@click.option('--clean', is_flag=True, default=False)
@click.option('--natbib','backend',flag_value='natbib', default=True)
@click.option('--biblatex', 'backend',flag_value='biblatex')
def cli(library,outfile,keys=None,aux=None, journal_abbreviations=None, clean=False, backend='natbib'):

    db = bibtexparser.load(library)

    _keys = []
    if keys is not None:
        _keys += list(parse_list(keys))
    if aux is not None:
        _keys += list(parse_aux(aux, backend=backend))
    _keys = sorted(set(_keys))
    click.echo(" ".join(_keys))

    # If we don't have any keys, we just keep going with
    # all keys
    if len(_keys) > 0:
        db.entries = [e for e in db.entries
            if e['ID'] in _keys]

    if journal_abbreviations is not None:
        abbreviate_matching = create_abbreviator(journal_abbreviations)
        db.entries = [abbreviate_matching(e) for e in db.entries]

    if clean:
        for entry in db.entries:
            entry.pop('file', None)

    bibtexparser.dump(db, outfile)

if __name__ == '__main__':
    cli()
