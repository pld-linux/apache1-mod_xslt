# TODO
# - doesn't build
# mod_xslt.c:212: warning: passing arg 6 of `SablotRunProcessor' from incompatible pointer type
# ...
%define		mod_name	xslt
%define 	apxs		/usr/sbin/apxs1
Summary:	Module to serve XML based content
Summary(pl):	Modu³ do udostêpniania dokumentów XML
Name:		apache1-mod_%{mod_name}
Version:	1.1
Release:	1.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modxslt/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	ce458a48f56cc857c808b71ec27f592d
Source1:	%{name}.conf
Patch0:		%{name}-includes.patch
Patch1:		%{name}-regex.patch
Patch2:		%{name}-make.patch
Patch3:		%{name}-module.patch
URL:		http://modxslt.userworld.com/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sablotron-devel
Requires:	apache1 >= 1.3.33-2
Requires:	expat
Requires:	sablotron
Obsoletes:	apache-mod_xslt <= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_xslt is a simple Apache module to serve XML based content. Data is
stored in XML files on the server. The user requests the XML file and
the translation method via a url such as this:
http://localhost/sourcefile.html. The module will parse this URL into
a XML source file and an XSL source file. In the example above, the
XML file will be sourcefile.xml. The module will open sourcefile.xml
and determine its DOCTYPE. Based on the DOCTYPE, the XSL file will be
opened. Should the DOCTYPE be "tutorial", the XSL file opened would be
tutorial_html.xsl. The content-type returned to the browser is
text/html. The translation occurs transparently to the user.

%description -l pl
mod_xslt jest prostym modu³em Apache do udostêpniania dokumentów XML.
Dane s± zapisane w plikach XML na serwerze. U¿ytkownik ¿±da pliku XML
i t³umaczenia poprzez URL w stylu http://localhost/sourcefile.html.
Modu³ zamienia ten URL na pliki ¼ród³owe XML i XSL. W tym przyk³adzie
plikiem XML bêdzie sourcefile.xml. Modu³ otworzy plik sourcefile.xml i
okre¶li DOCTYPE, na podstawie którego otworzy odpowiedni plik XSL.
Je¿eli DOCTYPE jest "tutorial", plikiem XSL bêdzie tutorial_html.xsl.
Nastêpnie modu³ dokona przetwarzania pliku XML za pomoc± arkusza XSLT
i zwróci przegl±darce powsta³y w ten sposób text/html. Ca³y proces
odbywa siê w sposób niewidoczny dla u¿ytkownika.

%prep
%setup -q -n mod%{mod_name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} \
	APXS=%{apxs} \
	CFLAGS="%{rpmcflags} -DEAPI"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
