#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

KeepSpecial = ["libtool"]

def setup():
    pisitools.dosed(
        "include/ldap_defaults.h",
        "(#define LDAPI_SOCK).*",
        '\\1 "/run/openldap/slapd.sock"'
    )
    pisitools.dosed("servers/slapd/Makefile.in", "(\$\(DESTDIR\))\$\(localstatedir\)(\/run)", r"\1\2")

    pisitools.cflags.add("-D_REENTRANT -D_GNU_SOURCE -fPIC -Wl,--as-needed -DLDAP_CONNECTIONLESS -fpie")
    pisitools.ldflags.add("-pie")

    options = "--prefix=/usr \
               --enable-bdb \
               --enable-hdb=mod \
               --enable-slapd \
               --enable-passwd=mod \
               --enable-dnssrv=mod \
               --enable-ldap \
               --enable-wrappers \
               --enable-meta=mod \
               --enable-monitor=mod \
               --enable-null=mod \
               --enable-shell=mod \
               --enable-rewrite \
               --enable-rlookups \
               --enable-aci \
               --enable-modules \
               --enable-cleartext \
               --enable-lmpasswd \
               --enable-spasswd \
               --enable-slapi \
               --enable-dyngroup \
               --enable-proxycache \
               --enable-perl \
               --enable-syslog \
               --enable-dynamic \
               --enable-local \
               --enable-proctitle \
               --enable-overlays=mod \
               --with-tls=moznss \
               --with-pic \
               --with-cyrus-sasl \
               --with-threads \
               --without-fetch \
               --enable-crypt \
               --enable-ipv6 \
               --enable-dynacl \
               --enable-shared \
               --disable-static \
               --disable-slp \
               --localstatedir=/var/lib"

    if get.buildTYPE() == "emul32":
        options += " --prefix=/emul32 \
                     --libdir=/usr/lib32 \
                     --libexecdir=/emul32/libexec \
                     --disable-bdb \
                     --disable-hdb \
                     --disable-wrappers \
                     --disable-spasswd \
                     --disable-perl \
                     --without-cyrus-sasl"

    shelltools.export("AUTOMAKE", "/bin/true")
    autotools.autoreconf("-fi")
    autotools.configure(options)

def build():
    autotools.make("-j1")

def install():
    if get.buildTYPE() == "emul32":
        autotools.rawInstall("DESTDIR=%s" % get.installDIR())
        pisitools.remove("/usr/lib32/*.a")
        return
    else:
        autotools.rawInstall("DESTDIR=%s" % get.installDIR())


    pisitools.dodir("/run/openldap")
    pisitools.dodir("/etc/openldap/ssl")

    pisitools.dodoc("ANNOUNCEMENT", "CHANGES", "COPYRIGHT", "README", "LICENSE")
