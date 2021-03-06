"""
content.py: routes related to content

Copyright 2014, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os
import stat
import math
import json
import shutil
import logging
import subprocess

from bottle import (
    request, view, abort, default_app, static_file, redirect, response,
    template)

from ..lib import archive
from ..lib import downloads
from ..lib import send_file
from ..lib import files
from ..lib import i18n
from ..lib.ajax import roca_view
from ..lib.i18n import lazy_gettext as _


app = default_app()


@roca_view('content_list', '_content_list')
def content_list():
    """ Show list of content """
    try:
        f_per_page = int(request.params.get('c', 1))
    except ValueError as e:
        f_per_page = 1
    f_per_page = max(1, min(4, f_per_page))
    try:
        page = int(request.params.get('p', 1))
    except ValueError:
        page = 1
    try:
        tag = int(request.params.get('t'))
    except (TypeError, ValueError):
        tag = None
        tag_name = None

    if tag:
        try:
            tag_name = archive.get_tag_name(tag)['name']
        except (IndexError, KeyError):
            abort(404, _('Specified tag was not found'))

    query = request.params.getunicode('q', '').strip()

    per_page = f_per_page * 20

    if query:
        total_items = archive.get_search_count(query, tag=tag)
    else:
        total_items = archive.get_count(tag=tag)

    total_pages = math.ceil(total_items / per_page)
    page = max(1, min(total_pages, page))
    offset = (page - 1) * per_page

    if query:
        metadata = archive.search_content(query, offset, per_page, tag=tag)
    else:
        metadata = archive.get_content(offset, per_page, tag=tag)

    return {
        'metadata': [downloads.Meta(m) for m in metadata],
        'total_items': total_items,
        'total_pages': total_pages,
        'per_page': per_page,
        'f_per_page': f_per_page,
        'page': page,
        'vals': request.params.decode(),
        'query': query,
        'tag': tag_name,
        'tag_id': tag,
        'tag_cloud': archive.get_tag_cloud()
    }


@view('remove_error')
@archive.with_content
def remove_content(meta):
    """ Delete a single piece of content from archive """
    success, failed = archive.remove_from_archive([meta.md5])
    if failed:
        return dict(meta=meta)
    redirect(i18n.i18n_path('/'))


def content_file(content_id, filename):
    """ Serve file from zipball with specified id """
    zippath = downloads.get_zip_path(content_id)
    try:
        metadata, content = downloads.get_file(zippath, filename)
    except KeyError:
        logging.debug("File '%s' not found in '%s'" % (filename, zippath))
        abort(404, 'Not found')
    size = metadata.file_size
    timestamp = os.stat(zippath)[stat.ST_MTIME]
    if filename.endswith('.html'):
        logging.debug("Patching HTML file '%s' with Librarian stylesheet" % (
                      filename))
        # Patch HTML with link to stylesheet
        size, content = downloads.patch_html(content)
    return send_file.send_file(content, filename, size, timestamp)


@view('reader')
@archive.with_content
def content_reader(meta):
    """ Loads the reader interface """
    archive.add_view(meta.md5)
    return dict(meta=meta)


def cover_image(path):
    config = request.app.config
    covers = config['content.covers']
    return static_file(path, root=covers, download=os.path.basename(path))


def dictify_file_list(file_list):
    return [{
        'path': f[0],
        'name': f[1],
        'size': f[2],
    } for f in file_list]


@view('file_list')
def show_file_list(path='.'):
    path = request.params.get('p', path)
    resp_format = request.params.get('f', '')
    try:
        path, relpath, dirs, file_list, readme = files.get_dir_contents(path)
    except files.DoesNotExist:
        if path == '.':
            if resp_format == 'json':
                response.content_type = 'application/json'
                return json.dumps(dict(
                    dirs=dirs,
                    files=dictify_file_list(file_list),
                    readme=readme
                ))
            return dict(path='.', dirs=[], files=[], up='.', readme='')
        abort(404)
    except files.IsFileError as err:
        if resp_format == 'json':
            fstat = os.stat(path)
            response.content_type = 'application/json'
            return json.dumps(dict(
                name=os.path.basename(path),
                size=fstat[stat.ST_SIZE],
            ))
        return static_file(err.path, root=files.get_file_dir())
    up = os.path.normpath(os.path.join(path, '..'))
    if resp_format == 'json':
        response.content_type = 'application/json'
        return json.dumps(dict(
            dirs=dirs,
            files=dictify_file_list(file_list),
            readme=readme
        ))
    return dict(path=relpath, dirs=dirs, files=file_list, up=up, readme=readme)


def go_to_parent(path):
    filedir= files.get_file_dir()
    redirect(i18n.i18n_path('/files/') + os.path.relpath(
        os.path.dirname(path), filedir))


def delete_path(path):
    filedir= files.get_file_dir()
    if not os.path.exists(path):
        abort(404)
    if os.path.isdir(path):
        if path == filedir:
            # FIXME: handle this case
            abort(400)
        shutil.rmtree(path)
    else:
        os.unlink(path)
    go_to_parent(path)


def rename_path(path):
    filedir= files.get_file_dir()
    new_name = request.forms.get('name')
    if not new_name:
        go_to_parent(path)
    new_name = os.path.normpath(new_name)
    new_path =  os.path.join(os.path.dirname(path), new_name)
    os.rename(path, new_path)
    go_to_parent(path)


def run_path(path):
    callargs = [path]
    proc = subprocess.Popen(callargs, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    ret = proc.returncode
    return ret, out, err


def handle_file_action(path):
    action = request.forms.get('action')
    path = files.get_full_path(path)
    if action == 'delete':
        delete_path(path)
    elif action == 'rename':
        rename_path(path)
    elif action == 'exec':
        if os.path.splitext(path)[1] != '.sh':
            # For now we only support running BASH scripts
            abort(400)
        logging.info("Running script '%s'", path)
        ret, out, err = run_path(path)
        logging.debug("Script '%s' finished with return code %s", path, ret)
        return template('exec_result', ret=ret, out=out, err=err)
    else:
        abort(400)
