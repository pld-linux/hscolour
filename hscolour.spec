%define		pkgname	hscolour
Summary:	Colourise Haskell code
Name:		hscolour
Version:	1.19
Release:	3
License:	GPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/hscolour/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a5203dc75fb759aaee29f73491fb55f8
URL:		http://www.cs.york.ac.uk/fp/darcs/hscolour/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Obsoletes:	hscolour-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
hscolour is a small Haskell script to colourise Haskell code. It
currently has six output formats: ANSI terminal codes, HTML 3.2 with
font tags, HTML 4.01 with CSS, XHTML 1.0 with inline CSS styling,
LaTeX, and mIRC chat codes.

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
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

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
