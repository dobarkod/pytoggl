# Python wrapper for Toggl API

[![Build Status](https://travis-ci.org/dobarkod/pytoggl.png?branch=master)](https://travis-ci.org/dobarkod/pytoggl)

This is a Python wrapper for the
[Toggl API (v8)](https://github.com/toggl/toggl_api_docs/blob/master/toggl_api.md)
and the
[Toggl Reports API (v2)](https://github.com/toggl/toggl_api_docs/blob/master/reports.md).

This is work in progress but is already used for internal reporting tools
at [Good Code](http://goodcode.io/). Patches to improve the functionality
coverage and quality are welcome!

## Installation

Install via pip:

    pip install git+git://github.com/dobarkod/pytoggl.git

The requirements (requests and iso8601 packages) will be automatically
installed.

## Quickstart

First, prepare the API wrapper with your Toggl API token:

    from toggl.api import Api
    api = Api('YOUR-TOGGL-API-KEY')

Iterate through all the workspaces and print their names and IDs:

    for ws in api.workspaces:
        print ws.name, ws.id

Get workspace by its ID:

    ws = api.workspaces[42]

Iterate through workspace projects and users and print their names and IDs:

    for project in ws.projects:
        print project.name, project.id

    for user in ws.users:
        print user.name, user.id

Projects and users can also be directly retrieved by their ID, the same as
for workspaces.

More thorough documentation is comming soon.

The API is currently missing any methods to create, modify or delete objects
in Trello workspaces (only listing/retrieval works).

## Tests

To run the tests, first ensure you have the `pytest` tool installed:

    pip install pytest

Then run the tests with:

    PYTHONPATH=. py.test


## License and copyright

Copyright (C) 2013 Good Code.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
