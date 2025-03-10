#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_without	tests		# unit tests
%bcond_with	bootstrap	# bootstraping for python-rpm-packaging (rpm-pythonprov)

%if %{with bootstrap}
%undefine	with_doc
%undefine	with_tests
%endif

%define		module	pyparsing
Summary:	pyparsing - Python 3 module for creating executing simple grammars
Summary(pl.UTF-8):	pyparsing - moduł Pythona 3 umożliwiający tworzenie i parsowanie prostych gramatyk
Name:		python3-%{module}
Version:	3.0.7
Release:	3.1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyparsing/
Source0:	https://files.pythonhosted.org/packages/source/p/pyparsing/%{module}-%{version}.tar.gz
# Source0-md5:	9d38774991175444e21a3dfa865876cc
URL:		https://github.com/pyparsing/pyparsing/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-jinja2
BuildRequires:	python3-pytest
BuildRequires:	python3-railroad-diagrams
%endif
%{!?with_bootstrap:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg-3}
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The parsing module is an alternative approach to creating and
executing simple grammars, vs. the traditional lex/yacc approach, or
the use of regular expressions. The parsing module provides a library
of classes that client code uses to construct the grammar directly in
Python code.

%description -l pl.UTF-8
Moduł pyparsing umożliwia tworzenie i parsowanie prostych gramatyk w
sposób odmienny od podejścia tradycyjnego, jakim jest zwykle użycie
pary lex/yacc lub wyrażeń regularnych. Moduł ten udostępnia bibliotekę
klas, przy pomocy których gramatyka tworzona jest wprost w kodzie
Pythona.

%package doc
Summary:	Documentation for pyparsing module
Summary(pl.UTF-8):	Dokumentacja do modułu pyparsing
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains documentation files for pyparsing Python module.

%description doc -l pl.UTF-8
Pakiet zawierający dokumentację dla modułu Pythona pyparsing.

%package examples
Summary:	Examples for pyparsing module
Summary(pl.UTF-8):	Przykłady do modułu pyparsing
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
This package contains example files for pyparsing Python module.

%description examples -l pl.UTF-8
Pakiet zawierający przykładowe skrypty dla modułu Pythona pyparsing.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py3_install

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.rst
%{py3_sitescriptdir}/pyparsing
%{py3_sitescriptdir}/pyparsing-*.egg-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
