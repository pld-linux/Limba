%include	/usr/lib/rpm/macros.perl
Summary:	Experimental software installation system
Summary(pl.UTF-8):	Eksperymentalny system do instalowania oprogramowania
Name:		Limba
Version:	0.5.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://people.freedesktop.org/~mak/limba/releases/%{name}-%{version}.tar.xz
# Source0-md5:	b59a4a3d2cbde2e34318da3ceed43fac
URL:		http://people.freedesktop.org/~mak/limba/
BuildRequires:	AppStream-devel >= 0.8.6
BuildRequires:	cmake >= 2.8.6
BuildRequires:	curl-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel
BuildRequires:	gpgme-devel
BuildRequires:	libarchive-devel
BuildRequires:	libuuid-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.104
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xz
BuildRequires:	yaml-devel >= 0.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	AppStream >= 0.8.6
Requires:	polkit >= 0.104
# requires overlayfs
Requires:	uname(release) >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Limba provides developers with a way to easily create software bundles
for their applications which run on multiple Linux distributions. It
provides atomic upgrades of software, simultaneous installation of
multiple software versions and a simple way to obtain and upgrade
software.

It is based on ideas of Glick2 and Listaller, and uses modern Linux
kernel features to allow applications to share libraries and other
components, reducing the amount of duplicate software components
running on a Linux system.

%description -l pl.UTF-8
Limba udostępnia programistom metodę łatwego tworzenia zestawów
oprogramowania dla ich aplikacji, działających nawielu dystrybucjach
Linuksa. Udostępnia atomowe uaktualnianie oprogramowania, jednoczesną
instalację wielu wersji oprogramowania oraz prosty sposób pobierania i
uaktualniania oprogramowania.

System jest oparty na ideach narzędzi Glick2 oraz Linstaller;
wykorzystuje nowoczesne możliwości jądra Linuksa, aby pozwolić
aplikacjom na współdzielenie bibliotek i innych komponentów,
zmniejszając ilość zduplikowanych składników oprogramowania
działających w systemie.

%package compile
Summary:	LiCompile tools
Summary(pl.UTF-8):	Narzędzia LiCompile
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description compile
LiCompile tools.

%description compile -l pl.UTF-8
Narzędzia LiCompile.

%package libs
Summary:	Limba library
Summary(pl.UTF-8):	Biblioteka Limba
Group:		Libraries
Requires:	glib2 >= 1:2.44

%description libs
Limba library.

%description libs -l pl.UTF-8
Biblioteka Limba.

%package devel
Summary:	Header files for Limba library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Limba
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44

%description devel
Header files for Limba library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Limba.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env perl,/usr/bin/perl,' contrib/licompile/{lig++,ligcc}

%build
install -d build
cd build
# note: .pc file creation expects CMAKE_INSTALL_LIBDIR relative to CMAKE_INSTALL_PREFIX
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DDOCUMENTATION=ON \
	-DLICOMPILE=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang limba

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f limba.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/limba
%attr(755,root,root) %{_bindir}/limba-build
%attr(755,root,root) %{_bindir}/lipkgen
%attr(755,root,root) %{_bindir}/runapp
%dir %{_libdir}/limba
%attr(755,root,root) %{_libdir}/limba/limba-daemon
/etc/dbus-1/system.d/org.freedesktop.Limba.conf
%{systemdunitdir}/limba.service
%{systemdunitdir}/limba-cleanup.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Limba.service
%{_datadir}/limba
%{_datadir}/mime/packages/x-ipk.xml
%{_datadir}/polkit-1/actions/org.freedesktop.limba.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.limba.rules
%{_mandir}/man1/limba.1*
%{_mandir}/man1/limba-build.1*
%{_mandir}/man1/lipkgen.1*
%{_mandir}/man1/runapp.1*
%dir /opt/bundle
%dir /opt/software

%files compile
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lig++
%attr(755,root,root) %{_bindir}/ligcc
%attr(755,root,root) %{_bindir}/relaytool
%dir %{_prefix}/lib/licompile
%attr(755,root,root) %{_prefix}/lib/licompile/buildlist
%{_includedir}/licompile
%{_aclocaldir}/relaytool.m4
%{_datadir}/licompile
%{_mandir}/man1/lig++.1*
%{_mandir}/man1/ligcc.1*
%{_mandir}/man1/relaytool.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblimba.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblimba.so.0
%{_libdir}/girepository-1.0/Limba-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblimba.so
%{_includedir}/Limba
%{_datadir}/gir-1.0/Limba-1.0.gir
%{_pkgconfigdir}/limba.pc
