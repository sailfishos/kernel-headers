Summary: Headers describing the kernel ABI
Name: linux-glibc-devel
License: GPLv2
URL: http://www.kernel.org/

%define kversion 4.4.302
Version: %{kversion}
Release: 1
Provides: kernel-headers = %{kversion}
Obsoletes: kernel-headers <= %{kversion}

#
# A note about versions and patches.
# This package is supposed to provide the official, stable kernel ABI, as specified
# by the kernels released by Linus Torvalds. Release candidate kernels do not
# have a stable ABI yet, and should thus not be in this package.
#
# Likewise, if there are distro patches in the kernel package that would have the
# unfortunate side effect of extending the kernel ABI, these extensions are unofficial
# and applications should not depend on these extensions, and hence, these extensions
# should not be part of this package.
#
# Applications that want headers from the kernel that are not in this package need
# to realize that what they are using is not a stable ABI, and also need to include
# a provide a copy of the header they are interested in into their own package/source
# code.
#

Source0: %{name}-%{version}.tar.xz
Patch0001: 0001-net-Update-API-for-VF-vlan-protocol-802.1ad-support.patch
Patch0002: 0002-prctl-Add-speculation-control-prctls.patch
Patch0003: 0003-net-core-Add-support-for-configuring-VF-GUIDs.patch

BuildRequires:  findutils,  make >= 3.78, diffutils, gawk

%description
The linux-glibc-devel package contains the header files that describe
the kernel ABI. This package is mostly used by the C library and some
low level system software, and is only used indirectly by regular
applications.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
make mrproper

%install

make INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# glibc provides scsi headers for itself, for now
find  $RPM_BUILD_ROOT/usr/include -name ".install" | xargs rm -f
find  $RPM_BUILD_ROOT/usr/include -name "..install.cmd" | xargs rm -f
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
rm -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h

%files
%defattr(-,root,root)
%license COPYING
/usr/include/*
