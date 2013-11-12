#!/usr/bin/python
# -*- coding: utf-8 -*-
#    Copyright (C) 2013  bohai  <boh.ricky@gmail.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import stat
import errno
import os
# pull in some spaghetti to make this stuff work without
# fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse
import json
from baidupan.baidupan import BaiduPan
import logging
from baidufuseconf import Baidufuseconf

if not hasattr(fuse, '__version__'):
    raise RuntimeError(
        "your fuse-py doesn't know of fuse.__version__, \
        probably it's too old.")

fuse.fuse_python_api = (0, 2)

logger = logging.getLogger("BaiduFS")
formatter = logging.Formatter(
    '%(name)-12s %(asctime)s %(levelname)-8s %(message)s',
    '%a, %d %b %Y %H:%M:%S')
file_handler = logging.FileHandler("baidufs.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class BaiduFS(Fuse):
    '''Baidu netdisk filesystem'''

    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        self.disk = BaiduPan(Baidufuseconf.baidu_token)

    def get_abs_path(self, path):
        return "%s%s" % (Baidufuseconf.baidu_rootdir, path)

    def getattr(self, path):
        logger.error("getattr is: " + path)
        abs_path = self.get_abs_path(path)
        st = MyStat()
        jdata = json.loads(self.disk.meta(abs_path))
        if 'list' not in jdata:
            logger.error("getattr is None")
            return -errno.ENOENT
        st.st_ctime = jdata['list'][0]['ctime']
        st.st_mtime = jdata['list'][0]['mtime']
        st.st_mode = (stat.S_IFDIR | 0755) if jdata['list'][0]['isdir']\
            else (stat.S_IFREG | 0755)
        st.st_nlink = 2 if jdata['list'][0]['isdir'] else 1
        st.st_size = jdata['list'][0]['size']
        return st

    def readdir(self, path, offset):
        logger.error("readdir is: " + path)
        abs_path = self.get_abs_path(path)
        jdata = json.loads(self.disk.ls(abs_path))
        files = ['.', '..']
        for r in jdata['list']:
            files.append(r['path'].encode('ascii', 'ignore')[len(abs_path):])
        logger.error(files)
        for r in files:
            yield fuse.Direntry(r)

    def open(self, path, flags):
        logger.error("open is: " + path)
        pass
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

    def mkdir(self, path, mode):
        logger.error("mkdir is:" + path)
        abs_path = self.get_abs_path(path)
        self.disk.mkdir(abs_path)

    def rmdir(self, path):
        logger.error("rmdir is:" + path)
        abs_path = self.get_abs_path(path)
        self.disk.rm(abs_path)

    def read(self, path, size, offset):
        logger.error("read is: " + path)
        abs_path = self.get_abs_path(path)
        paras = {'Range': 'Range: bytes=%s-%s' % (offset, offset + size)}
        return self.disk.download(abs_path, headers = paras)


