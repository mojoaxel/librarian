"""
favorites.py: routes related to favorites

Copyright 2014, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import view, default_app

from .. import downloads

__all__ = ('app', 'dashboard',)

PREFIX = '/'


app = default_app()


@app.get(PREFIX)
@view('dashboard')
def dashboard():
    """ Render the dashboard """
    spool, content, total = downloads.free_space()
    count = downloads.zipball_count()
    used = downloads.archive_space_used()
    favorites = downloads.favorite_content(limit=5)
    last_update = downloads.last_update()
    return locals()

