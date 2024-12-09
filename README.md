# sdncheck

[![PyPI - Version](https://img.shields.io/pypi/v/sdncheck.svg)](https://pypi.org/project/sdncheck)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sdncheck.svg)](https://pypi.org/project/sdncheck)

`sdncheck` is a tool for checking mboxes and similar text-based files for the
presence of known bad email addresses and domains, in case you might not want to
communicate with those places.

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

For now, `sdncheck` can only be installed via the repository with `pip`:

```console
pip install .
```

## Examples

Check a patch series (e.g. one downloaded with [git-pw](https://github.com/getpatchwork/git-pw)) for domains based on email addresses stored in a matchfile:

```console
sdncheck --patch my_bad.patch --match-list testfile.txt

Patch '[PATCH v5 01/16] subsystem: add basic support for stuff' contained:
- authors: []
- to: []
- cc: ['\n  Bad Actor Guy <bad@actor.tv>']

Patch '[PATCH v5 02/16] subsystem: part: add more specific support' contained:
- authors: ["My Evil Twin <myname@badplace.fake>"]
- to: []
- cc: []

Patch '[PATCH v5 06/16] subsystem: get really deep into the weeds' contained:
- authors: []
- to: ['\n Bad Actor Guy 2 <badder@actor.tv>']
- cc: []

Patch '[PATCH v5 16/16] docs: subsystem: describe what I did' contained:
- authors: []
- to: ['\n  Kinda Mean <admin@hacks.world>']
- cc: ['\n  Really Not Friendly <hacker@hacks.world>']
```

## License

`sdncheck` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
