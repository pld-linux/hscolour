%define		pkgname	hscolour
Summary:	Colourise Haskell code
Summary(pl.UTF-8):	Kolorowanie kodu w Haskellu
Name:		hscolour
Version:	1.24.4
Release:	1
License:	GPL
Group:		Development/Languages
#SourceDownload: http://hackage.haskell.org/package/hscolour
Source0:	http://hackage.haskell.org/package/hscolour-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3b071820df13cbee7e90199e8e598007
URL:		http://www.cs.york.ac.uk/fp/darcs/hscolour/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Obsoletes:	hscolour-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
hscolour is a small Haskell script to colourise Haskell code. It
currently has six output formats: ANSI terminal codes, HTML 3.2 with
font tags, HTML 4.01 with CSS, XHTML 1.0 with inline CSS styling,
LaTeX, and mIRC chat codes.

%description -l pl.UTF-8
hscolour to mały skrypt Haskella służący do kolorowania kodu w
Haskellu. Obecnie ma sześć formatów wyjściowych: kody terminala ANSI,
HTML 3.2 ze znacznikami fontów, HTML 4.01 z CSS, XHTML 1.0 z
osadzonymi stylami CSS, LaTeX oraz kody mIRC-a.

%prep
%setup -q

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%attr(755,root,root) %{_bindir}/HsColour
%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf
%{_libdir}/%{ghcdir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}
