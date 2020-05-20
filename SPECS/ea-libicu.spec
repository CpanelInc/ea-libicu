%define ns_prefix ea
%define pkg_base  libicu
%define pkg_name  %{ns_prefix}-%{pkg_base}
%define _prefix   /opt/cpanel/%{ns_prefix}-%{pkg_base}
%define prefix_dir /opt/cpanel/%{ns_prefix}-%{pkg_base}
%define prefix_lib %{prefix_dir}/lib
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
%define release_prefix 2
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
./configure --prefix=/opt/cpanel/ea-libicu --enable-rpath
make -j8

%install

mkdir -p %{buildroot}%{prefix_dir}
mkdir -p %{buildroot}%{prefix_lib}
mkdir -p %{buildroot}%{prefix_bin}
mkdir -p %{buildroot}%{prefix_inc}
mkdir -p %{buildroot}%{prefix_lib}/pkgconfig

install icu4c/readme.html %{buildroot}%{prefix_dir}
install icu4c/license.html %{buildroot}%{prefix_dir}

cd icu4c/source

install lib/libicuuc.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}
install lib/libicui18n.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}
install lib/libicuio.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}
install lib/libicutu.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}
install lib/libicudata.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}
install lib/libicudata.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}

cd lib
ln -s libicuuc.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicuuc.so.%{version_major}
ln -s libicuuc.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicuuc.so
ln -s libicui18n.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicui18n.so.%{version_major}
ln -s libicui18n.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicui18n.so
ln -s libicuio.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicuio.so.%{version_major}
ln -s libicuio.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicuio.so
ln -s libicutu.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicutu.so.%{version_major}
ln -s libicutu.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicutu.so
ln -s libicudata.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicudata.so.%{version_major}
ln -s libicudata.so.%{version_major}.%{version_minor} %{buildroot}%{prefix_lib}/libicudata.so
cd ..

for f in config/*.pc; do
    file=`basename $f`
    install $f %{buildroot}%{prefix_lib}/pkgconfig/$file;
done

# install the devel files

install config/icu-config %{buildroot}%{prefix_bin}/icu-config
install tools/icuinfo/icuinfo %{buildroot}%{prefix_bin}/icuinfo

mkdir -p %{buildroot}%{prefix_inc}/layout
mkdir -p %{buildroot}%{prefix_inc}/unicode

for f in `find . -name '*.h'`; do
    install -D $f %{buildroot}%{prefix_inc}/$f;
done

mv -f %{buildroot}%{prefix_inc}/layoutex/layout/*.h %{buildroot}%{prefix_inc}/layout/
mv -f %{buildroot}%{prefix_inc}/samples/layout/*.h %{buildroot}%{prefix_inc}/layout/

cp -f %{buildroot}%{prefix_inc}/tools/ctestfw/unicode/*.h %{buildroot}%{prefix_inc}/unicode/
cp -f %{buildroot}%{prefix_inc}/common/unicode/*.h %{buildroot}%{prefix_inc}/unicode/
cp -f %{buildroot}%{prefix_inc}/extra/uconv/unicode/*.h %{buildroot}%{prefix_inc}/unicode/
cp -f %{buildroot}%{prefix_inc}/i18n/unicode/*.h %{buildroot}%{prefix_inc}/unicode/
cp -f %{buildroot}%{prefix_inc}/io/unicode/*.h %{buildroot}%{prefix_inc}/unicode/

%files
%defattr(755,root,root,755)
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
%defattr(644,root,root,755)
%doc %{prefix_dir}/readme.html
%doc %{prefix_dir}/license.html

%files -n %{pkg_name}-devel
%defattr(755,root,root,755)
%{prefix_bin}/icu-config
%{prefix_bin}/icuinfo
%{prefix_inc}/common/*.h
%{prefix_inc}/common/unicode/*.h
%{prefix_inc}/extra/scrptrun/*.h
%{prefix_inc}/extra/uconv/unicode/*.h
%{prefix_inc}/i18n/*.h
%{prefix_inc}/i18n/unicode/*.h
%{prefix_inc}/io/*.h
%{prefix_inc}/io/unicode/*.h
%{prefix_inc}/layoutex/*.h
%{prefix_inc}/layout/*.h
%{prefix_inc}/samples/*/*/*.h
%{prefix_inc}/samples/*/*.h
%{prefix_inc}/test/*/*/*/*.h
%{prefix_inc}/test/*/*/*.h
%{prefix_inc}/test/*/*.h
%{prefix_inc}/tools/*/*/*.h
%{prefix_inc}/tools/*/*.h
%{prefix_lib}/pkgconfig/*.pc
%{prefix_inc}/unicode/*.h

%changelog
* Wed May 20 2020 Julian Brown <julian.brown@cpanel.net> - 66-2
- ZC-6843: Fix problems on CentOS 8

* Tue Mar 17 2020 Julian Brown <julian.brown@cpanel.net> - 66.1-1
- ZC-6349: Initial rpm creation

