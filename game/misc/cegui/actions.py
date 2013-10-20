#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "CEGUI-%s" % get.srcVERSION()

def setup():
    pisitools.touch("NEWS")
    pisitools.touch("README")
    pisitools.touch("AUTHORS")
    pisitools.touch("ChangeLog")
    autotools.autoreconf("-vfi")
    autotools.configure("--enable-xerces-c \
                         --enable-libxml \
                         --enable-expat \
                         --enable-tinyxml \
                         --enable-opengl-renderer \
                         --enable-toluacegui \
                         --enable-freeimage \
                         --enable-silly \
                         --enable-lua-module \
                         --with-x \
                         --with-gtk2 \
                         --with-default-xml-parser=TinyXMLParser \
                         --with-default-image-codec=STBImageCodec \
                         --disable-devil \
                         --disable-samples")
    
    # for fix unused dependency
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("doc/COPYING", "doc/GLEW-LICENSE", "doc/PCRE-LICENSE", "doc/TinyXML-License", "doc/stringencoders-license", "doc/README")
