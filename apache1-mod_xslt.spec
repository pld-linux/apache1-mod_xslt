%define		mod_name	xslt
Summary:	Module to serve XML based content
Summary(pl):	Moduł do udostępniania dokumentów XML
Name:		apache-mod_%{mod_name}
Version:	1.1
Release:	2
License:	GPL
URL:		http://modxslt.userworld.com/
Source0:	http://prdownloads.sourceforge.net/mod%{mod_name}/mod_%{mod_name}-%{version}.tar.gz
Source1:	mod_%{mod_name}.conf
Patch0:		mod_%{mod_name}-includes.patch
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	expat
Requires:	sablotron
BuildRequires:	apache-devel
BuildRequires:	sablotron-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{_sbindir}/apxs -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

%description
mod_xslt is a simple Apache module to serve XML based content. Data is
stored in XML files on the server. The user requests the XML file and
the translation method via a url such as this:
http://localhost/sourcefile.html The module will parse this URL into a
XML source file and an XSL source file. In the example above, the XML
file will be sourcefile.xml. The module will open sourcefile.xml and
determine its DOCTYPE. Based on the DOCTYPE, the XSL file will be
opened. Should the DOCTYPE be "tutorial", the XSL file opened would be
tutorial_html.xsl. The content-type returned to the browser is
text/html. The translation occurs transparently to the user.

%prep
%setup -q -n mod%{mod_name}
%patch0 -p1

%build
CFLAGS="%{rpmcflags}"; export CFLAGS
%{__make} APXS=%{_sbindir}/apxs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mod_xslt.conf

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*mod_%{mod_name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/mod_%{mod_name}.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	grep -v -q "^Include.*mod_%{mod_name}.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mod_%{mod_name}.conf
