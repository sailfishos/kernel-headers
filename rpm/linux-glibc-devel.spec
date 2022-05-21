Summary: Headers describing the kernel ABI
Name: linux-glibc-devel
License: GPLv2
URL: http://www.kernel.org/

%define kversion 5.4.297
Version: %{kversion}
Release: 1
Provides: kernel-headers = %{kversion}
Obsoletes: kernel-headers < %{kversion}

%{lua:
function cross_archs()
  return "aarch64", "arm", "i486", "x86_64"
end

function kernel_arch(arch)
  local map = {
     ["aarch64"] = "arm64",
     ["armv6hl"] = "arm",
     ["armv7hl"] = "arm",
     ["i386"] = "x86",
     ["i486"] = "x86",
     ["i586"] = "x86",
     ["i686"] = "x86",
     ["x86_64"] = "x86",
  }
  return map[arch] or arch
end

function gcc_target(arch)
  local map = {
    ["arm"] = "armv7hl-meego-linux-gnueabi",
  }
  return map[arch] or arch.."-meego-linux"
end
}

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
Patch0: sed.patch
Source0: %{name}-%{version}.tar.xz

BuildRequires:  findutils,  make >= 3.78, diffutils, gawk, flex, bison, rsync

%description
The linux-glibc-devel package contains the header files that describe
the kernel ABI. This package is mostly used by the C library and some
low level system software, and is only used indirectly by regular
applications.

%ifarch %{ix86} x86_64

%{lua:
  for i,arch in ipairs({cross_archs()}) do
    print(rpm.expand([[

%package -n cross-]]..arch..[[-linux-glibc-devel
Summary:        Linux headers for ]]..arch..[[ userspace cross development
BuildArch:      noarch
Provides:       cross-]]..arch..[[-kernel-headers = %{kversion}

%description -n cross-]]..arch..[[-linux-glibc-devel
This package provides Linux kernel headers for ]]..arch..[[, the kernel API description
required for compilation of almost all programs.
]]))
  end}

%endif

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build

%install

#cd %{lua:print(kernel_arch(rpm.expand("%_target_cpu")))}
#cp -a usr %{buildroot}/
#cp -a version.h %{buildroot}%{_includedir}/linux/
#cd ..
make INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

%ifarch %{ix86} x86_64

%{lua:
  for i,arch in ipairs({cross_archs()}) do
    print(rpm.expand([[
sysroot=/opt/cross/]]..gcc_target(arch)..[[/sys-root
mkdir -p %{buildroot}${sysroot}/%{_includedir}/linux/
make ARCH=]]..kernel_arch(arch)..[[ INSTALL_HDR_PATH=$RPM_BUILD_ROOT/${sysroot}/usr headers_install
rm -rf $RPM_BUILD_ROOT/${sysroot}/usr/include/drm
rm -rf $RPM_BUILD_ROOT/${sysroot}/usr/include/scsi
]]))
  end}

%endif

rm -rf $RPM_BUILD_ROOT/usr/include/drm
# glibc provides scsi headers for itself, for now
find  $RPM_BUILD_ROOT -name ".install" | xargs rm -f
find  $RPM_BUILD_ROOT -name "..install.cmd" | xargs rm -f
rm -rf $RPM_BUILD_ROOT/usr/include/scsi

%files
%license COPYING
%{_includedir}/*

%ifarch %{ix86} x86_64

%{lua:
  for i,arch in ipairs({cross_archs()}) do
    print(rpm.expand([[

%files -n cross-]]..arch..[[-linux-glibc-devel
%license COPYING
/opt/cross/]]..gcc_target(arch).."\n"))
  end}

%endif
