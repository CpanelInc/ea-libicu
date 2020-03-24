%define ns_prefix ea
%define pkg_base  libicu
%define pkg_name  %{ns_prefix}-%{pkg_base}
%define _prefix   /opt/cpanel/%{ns_prefix}-%{pkg_base}
%define prefix_dir /opt/cpanel/%{ns_prefix}-%{pkg_base}
%define prefix_lib %{prefix_dir}/%{_lib}
%define prefix_bin %{prefix_dir}/bin
%define prefix_inc %{prefix_dir}/include

# For whatever reason I cannot execute code in the define's here as
# when the macro is invoked in the files section, they do not execute
# and the information is critical, so unless someone can figure out a
# way to get this extracted from {version} I am listening.

%define version_major 66
%define version_minor 1

Summary: International Components for Unicode.
Name: %{pkg_name}
Version: %{version_major}.%{version_minor}
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: https://github.com/unicode-org/icu/blob/master/icu4c/LICENSE
Vendor: cPanel, Inc.
Group: Applications/Internet
Source: release-%{version_major}-%{version_minor}.tar.gz
URL: https://github.com/unicode-org/icu
BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-root

%if 0%{rhel} < 7
BuildRequires: python34
BuildRequires: devtoolset-7-toolchain
BuildRequires: devtoolset-7-libatomic-devel
BuildRequires: devtoolset-7-gcc
BuildRequires: devtoolset-7-gcc-c++
%else
BuildRequires: python3
BuildRequires: gcc
%endif

%description
Today's software market is a global one in which it is desirable to
develop and maintain one application (single source/single binary) that
supports a wide variety of languages. The International Components for
Unicode (ICU) libraries provide robust and full-featured Unicode
services on a wide variety of platforms to help this design goal.

%package devel
Summary: Files for development of applications which will use ea-libicu
Group: Development/Libraries

%description devel
The files needed for developing applications with ea-libicu.

%prep
%setup -q -n icu-release-%{version_major}-%{version_minor}

%build

%if 0%{?rhel} < 7
. /opt/rh/devtoolset-7/enable
%endif

cd icu4c/source
./configure
make -j8

%install

mkdir -p %{buildroot}%{prefix_dir}
mkdir -p %{buildroot}%{prefix_lib}
mkdir -p %{buildroot}%{prefix_bin}
mkdir -p %{buildroot}%{prefix_inc}
mkdir -p %{buildroot}%{prefix_lib}/pkgconfig

cd icu4c

install -m 644 readme.html %{buildroot}%{prefix_dir}
install -m 644 license.html %{buildroot}%{prefix_dir}

cd source

install -m 755 lib/libicuuc.so %{buildroot}%{prefix_lib}
ln -sf lib/libicuuc.so %{buildroot}%{prefix_lib}/libicuuc.so.%{version_major}
ln -sf lib/libicuuc.so %{buildroot}%{prefix_lib}/libicuuc.so.%{version_major}.%{version_minor}

install -m 755 lib/libicui18n.so %{buildroot}%{prefix_lib}
ln -sf lib/libicui18n.so %{buildroot}%{prefix_lib}/libicui18n.so.%{version_major}
ln -sf lib/libicui18n.so %{buildroot}%{prefix_lib}/libicui18n.so.%{version_major}.%{version_minor}

install -m 755 lib/libicuio.so %{buildroot}%{prefix_lib}
ln -sf lib/libicuio.so %{buildroot}%{prefix_lib}/libicuio.so.%{version_major}
ln -sf lib/libicuio.so %{buildroot}%{prefix_lib}/libicuio.so.%{version_major}.%{version_minor}

install -m 755 lib/libicutu.so %{buildroot}%{prefix_lib}
ln -sf lib/libicutu.so %{buildroot}%{prefix_lib}/libicutu.so.%{version_major}
ln -sf lib/libicutu.so %{buildroot}%{prefix_lib}/libicutu.so.%{version_major}.%{version_minor}

install -m 755 lib/libicudata.so %{buildroot}%{prefix_lib}
ln -sf lib/libicudata.so %{buildroot}%{prefix_lib}/libicudata.so.%{version_major}
ln -sf lib/libicudata.so %{buildroot}%{prefix_lib}/libicudata.so.%{version_major}.%{version_minor}

install -m 755 lib/libicudata.so %{buildroot}%{prefix_lib}
ln -sf lib/libicudata.so %{buildroot}%{prefix_lib}/libicudata.so.%{version_major}
ln -sf lib/libicudata.so %{buildroot}%{prefix_lib}/libicudata.so.%{version_major}.%{version_minor}

mkdir -p %{buildroot}%{prefix_lib}/pkgconfig
for f in config/*.pc; do
    file=`basename $f`
    install -m 755 $f %{buildroot}%{prefix_lib}/pkgconfig/$file;
done

# install the devel files

install -m 755 config/icu-config %{buildroot}%{prefix_bin}/icu-config
install -m 755 tools/icuinfo/icuinfo %{buildroot}%{prefix_bin}/icuinfo

mkdir -p %{buildroot}%{prefix_inc}/common
for f in common/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/common/unicode
for f in common/unicode/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/i18n
for f in i18n/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/i18n/unicode
for f in i18n/unicode/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/io
for f in io/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/layout
cd layoutex
for f in layout/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done
cd ..
cd samples
for f in layout/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done
cd ..

mkdir -p %{buildroot}%{prefix_inc}/tools/ctestfw/unicode
for f in tools/ctestfw/unicode/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/escapesrc
for f in tools/escapesrc/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/gennorm2
for f in tools/gennorm2/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/genrb
for f in tools/genrb/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/gensprep
for f in tools/gensprep/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/gentest
for f in tools/gentest/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/makeconv
for f in tools/makeconv/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/pkgdata
for f in tools/pkgdata/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/toolutil
for f in tools/toolutil/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

mkdir -p %{buildroot}%{prefix_inc}/tools/tzcode
for f in tools/tzcode/*.h; do
    install -m 755 $f %{buildroot}%{prefix_inc}/$f;
done

%files -n %{pkg_name}
%defattr(-,root,root,-)
%{prefix_lib}/libicuuc.so
%{prefix_lib}/libicuuc.so.%{version_major}
%{prefix_lib}/libicuuc.so.%{version_major}.%{version_minor}
%{prefix_lib}/libicui18n.so
%{prefix_lib}/libicui18n.so.%{version_major}
%{prefix_lib}/libicui18n.so.%{version_major}.%{version_minor}
%{prefix_lib}/libicuio.so
%{prefix_lib}/libicuio.so.%{version_major}
%{prefix_lib}/libicuio.so.%{version_major}.%{version_minor}
%{prefix_lib}/libicutu.so
%{prefix_lib}/libicutu.so.%{version_major}
%{prefix_lib}/libicutu.so.%{version_major}.%{version_minor}
%{prefix_lib}/libicudata.so
%{prefix_lib}/libicudata.so.%{version_major}
%{prefix_lib}/libicudata.so.%{version_major}.%{version_minor}
%{prefix_dir}/readme.html
%{prefix_dir}/license.html

%files -n %{pkg_name}-devel
%defattr(-,root,root,-)
%{prefix_bin}/icu-config
%{prefix_bin}/icuinfo
%{prefix_inc}/common/*.h
%{prefix_inc}/common/unicode/*.h
%{prefix_inc}/i18n/*.h
%{prefix_inc}/i18n/unicode/*.h
%{prefix_inc}/io/*.h
%{prefix_inc}/layout/*.h
%{prefix_inc}/tools/ctestfw/unicode/*.h
%{prefix_inc}/tools/escapesrc/*.h
%{prefix_inc}/tools/gennorm2/*.h
%{prefix_inc}/tools/genrb/*.h
%{prefix_inc}/tools/gensprep/*.h
%{prefix_inc}/tools/gentest/*.h
%{prefix_inc}/tools/makeconv/*.h
%{prefix_inc}/tools/pkgdata/*.h
%{prefix_inc}/tools/toolutil/*.h
%{prefix_inc}/tools/tzcode/*.h
%{prefix_lib}/pkgconfig/*.pc

%changelog
* Tue Mar 17 2020 Julian Brown <julian.brown@cpanel.net> - 66.1-1
- ZC-6349: Initial rpm creation

