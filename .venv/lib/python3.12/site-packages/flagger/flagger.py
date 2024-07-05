# -*- coding: utf-8 -*-

import ctypes
import json
import os
import sys
from ctypes import cdll
from sys import platform

# read __flagger_version__
dir_path = os.path.dirname(os.path.realpath(__file__))
exec(open(dir_path+'/version.py').read())

def __load_lib(f, name):
    path = os.path.dirname(__file__)
    path = os.path.abspath(path)

    arch = 'amd64' if sys.maxsize > 2 ** 32 else '386'

    if platform in ('win32', 'cygwin'):
        name = name + '-' + arch + '.dll'
    elif platform in ('linux', 'linux2'):
        name = 'lib' + name + '-' + arch + '.so'
    elif platform == 'darwin':
        name = 'lib' + name + '.dylib'
    else:
        raise RuntimeError('unsupported platform: ' + platform)

    return f(os.path.join(path, name))


native = __load_lib(cdll.LoadLibrary, 'flagger')

native.Init.argtypes = [ctypes.c_char_p]
native.Init.restype = ctypes.POINTER(ctypes.c_char)

def init(api_key="", source_url=None, backup_url=None, sse_url=None, ingestion_url=None,
         log_lvl="error"):
    """
    init method gets FlaggerConfiguration, establishes and maintains SSE connections and initialize Ingester
    :param api_key: API key to an environment
    :param source_url: URL to get FlaggerConfiguration
    :param backup_url: backup URL to get FlaggerConfiguration
    :param sse_url: URL for real-time updates of FlaggerConfiguration via sse
    :param ingestion_url: URL for ingestion
    :param log_lvl: log level: ERROR, WARN, DEBUG. Debug is the most verbose level and includes all Network requests
    """
    __call_native(native.Init,
                  __dict_to_c_char_p({
                      "apiKey": api_key,
                      "sdkName": "python",
                      "sdkVersion": __flagger_version__,
                      "sourceURL": source_url,
                      "backupSourceURL": backup_url,
                      "sseURL": sse_url,
                      "ingestionURL": ingestion_url,
                      "logLevel": log_lvl,
                  }))


native.Publish.argtypes = [ctypes.c_char_p]
native.Publish.restype = ctypes.POINTER(ctypes.c_char)


def publish(entity):
    __call_native(native.Publish,
                  __dict_to_c_char_p({
                      "entity": entity,
                  }))


native.Track.argtypes = [ctypes.c_char_p]
native.Track.restype = ctypes.POINTER(ctypes.c_char)


def track(event_name, event_props, entity=None):
    """
    Simple event tracking API. Entity is an optional parameter if it was set before.
    """
    __call_native(native.Track,
                  __dict_to_c_char_p({
                      "event": {
                          "name": event_name,
                          "eventProperties": event_props,
                          "entity": entity,
                      }
                  }))


native.SetEntity.argtypes = [ctypes.c_char_p]
native.SetEntity.restype = ctypes.POINTER(ctypes.c_char)


def set_entity(entity):
    """
    set_entity stores an entity in Flagger, which allows omission of entity in other API methods.

    If you don't provide any entity to Flagger:
    - flag functions always resolve with the default variation
    - track method doesn't record an event

     Rule of thumb: make sure you provided an entity to the Flagger
    """
    __call_native(native.SetEntity,
                  __dict_to_c_char_p({
                      "entity": entity,
                  }))


native.FlagIsEnabled.argtypes = [ctypes.c_char_p]
native.FlagIsEnabled.restype = ctypes.POINTER(ctypes.c_char)


def is_enabled(codename, entity=None):
    """
     Determines if flag is enabled for entity
    """
    return __call_native(native.FlagIsEnabled,
                         __dict_to_c_char_p({
                             "codename": codename,
                             "entity": entity,
                         }))


native.FlagIsSampled.argtypes = [ctypes.c_char_p]
native.FlagIsSampled.restype = ctypes.POINTER(ctypes.c_char)


def is_sampled(codename, entity=None):
    """
     Determines if entity is within the targeted subpopulations
    """
    return __call_native(native.FlagIsSampled,
                         __dict_to_c_char_p({
                             "codename": codename,
                             "entity": entity,
                         }))


native.FlagGetVariation.argtypes = [ctypes.c_char_p]
native.FlagGetVariation.restype = ctypes.POINTER(ctypes.c_char)


def get_variation(codename, entity=None):
    """
     Returns the variation assigned to the entity in a multivariate flag
    """
    return __call_native(native.FlagGetVariation,
                         __dict_to_c_char_p({
                             "codename": codename,
                             "entity": entity,
                         }))


native.FlagGetPayload.argtypes = [ctypes.c_char_p]
native.FlagGetPayload.restype = ctypes.POINTER(ctypes.c_char)


def get_payload(codename, entity=None):
    """
     Returns the payload associated with the treatment assigned to the entity
    """
    return __call_native(native.FlagGetPayload,
                         __dict_to_c_char_p({
                             "codename": codename,
                             "entity": entity,
                         }))


native.Shutdown.argtypes = [ctypes.c_char_p]
native.Shutdown.restype = ctypes.POINTER(ctypes.c_char)


def shutdown(timeout):
    """
    shutdown ingests data(if any), stop ingester and closes SSE connection. shutdown waits to finish current ingestion
    request, but no longer than a timeoutMillis.

    returns true if closed by timeout
    """
    return __call_native(native.Shutdown,
                         __dict_to_c_char_p({
                             "timeout": timeout
                         }))


def __call_native(f, *args, **kwargs):
    v = f(*args, **kwargs)
    if v:
        v = __c_char_p_to_dict(v)

        if 'error' in v:
            raise RuntimeError(v['error'])

        if 'data' in v:
            return v['data']


def __dict_to_c_char_p(v):
    v = cleanup_none(v)
    v = json.dumps(v)
    v = bytes(v, encoding='utf-8')
    return ctypes.c_char_p(v)


def __c_char_p_to_dict(v):
    v = ctypes.c_char_p.from_buffer(v).value
    return json.loads(v.decode('utf-8'))


def __str_to_c_char_p(v):
    return bytes(v, encoding='utf-8')


def cleanup_none(d):
    for k, v in list(d.items()):
        if v is None:
            del d[k]
        elif isinstance(v, dict):
            cleanup_none(v)
    return d
