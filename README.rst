===========
MAS2ROcrate
===========

Library and command-line tool to convert Sigma2 Metacenter projects to ro-crates.

Running
=======

Can be run even without installing, by first downloading the code, then doing oine of:

1. entering the src-directory and executing ``python -m mas2rocrate``
2. adding src to $PYTHONPATH then executing ``python -m mas2rocrate``

If installed it can be executed with both ``python -m mas2rocrate`` as well as ``mas2rocrate``.

Installation
============

Install with pip: ``pip install mas2rocrate``

Configuration
=============

The endpoint is not included with the script. It needs authentication via
a username and token. These can be put in a config-file or directly as
arguments to the script.

Example config file::

    endpoint = https://WHATEVER_URL
    username = USERNAME
    token = TOKEN

The config is searched for in the following files, in prioritized order::

    $PWD/.mas2rocrate.toml
    $HOME/.mas2rocrate.toml
    $XDG_CONFIG_HOME/mas2rocrate.toml
    /usr/local/etc/mas2rocrate.toml
    /etc/mas2rocrate.toml

Trivia
======

Names of persons are encoded in base 32 to serve as an identifier, since the
Sigma2 Metacenter do not use ORCID or similar identification standards.
