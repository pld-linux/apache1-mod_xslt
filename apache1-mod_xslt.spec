Summary:	Module to serve XML based content
Summary(pl):	Modu³ do udostêpniania dokumentów XML
%define		arname	modxslt
Name:		apache-mod_xslt
Version:	1.0
Release:	1
License:	GPL
URL:		http://modxslt.userworld.com/
Source0:	http://modxslt.userworld.com/%{arname}.tar.gz
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	expat
Requires:	sablotron
BuildRequires:	apache-devel
BuildRequires:	sablotron-devel

%define		_pkglibdir	%(%{_sbindir}/apxs -q LIBEXECDIR)

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
%setup -q -n mod_xslt

%build
CFLAGS="%{rpmcflags}"; export CFLAGS
%{__make} APXS=%{_sbindir}/apxs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}
cp -f *.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
