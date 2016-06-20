# bib-filter
A simple script to subset a .bib file based on a document or list of citation keys.

This can be useful to subset an global BibTeX library, for example to create a list
of citations to check into a paper's individual repository.

## Installation

> pip install -e https://github.com/davenquinn/bib-filter.git

## CLI usage

> bib-filter <library> <outfile> [--keys/-k <keyfile>] [--aux/-a <auxfile> ] [--clean]
