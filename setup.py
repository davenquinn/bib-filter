from setuptools import setup

setup(
    name='bib-filter',
    version=0.1,
    description="Filters a BibTeX bibliography.",
    license='MIT',
    install_requires=['Click','bibtexparser'],
    packages=['.'],
    entry_points="""
        [console_scripts]
        bib-filter=bib_filter:cli
    """)
