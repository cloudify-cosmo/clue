import os
import json

import sh
from path import path

from cloudify import ctx
from cloudify.decorators import operation
from cloudify import exceptions

from common import bake


@operation
def makedirs(location, **_):
    location = os.path.expanduser(location)
    if not os.path.isdir(location):
        os.makedirs(location)


@operation
def nose_run(virtualenv_location, test_path, **_):
    nose = bake(sh.Command(os.path.join(virtualenv_location, 'bin',
                                        'nosetests')))
    try:
        nose(test_path,
             nocapture=True,
             nologcapture=True,
             verbose=True).wait()
    except:
        raise exceptions.NonRecoverableError()


@operation
def configure_docs_getcloudify_source(docs_getcloudify_repo_location, **_):
    repo_location = path(
        ctx.source.instance.runtime_properties['repo_location'])
    dev_directory = repo_location / 'dev'
    config_path = dev_directory / 'config.json'

    if not dev_directory.exists():
        dev_directory.mkdir()

    config_path.write_text(json.dumps({
        'content': {
            'root': docs_getcloudify_repo_location
        }
    }))
