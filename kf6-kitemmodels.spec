#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.3
%define		qtver		5.15.2
%define		kfname		kitemmodels

Summary:	Set of item models extending the Qt model-view framework
Name:		kf6-%{kfname}
Version:	6.3.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	9309595d5c8199be1166934a9d97d512
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KItemModels provides the following models:

- KBreadcrumbSelectionModel - Selects the parents of selected items to
  create breadcrumbs
- KCheckableProxyModel - Adds a checkable capability to a source model
- KDescendantsProxyModel - Proxy Model for restructuring a Tree into a
  list
- KLinkItemSelectionModel - Share a selection in multiple views which
  do not have the same source model
- KModelIndexProxyMapper - Mapping of indexes and selections through
  proxy models
- KRecursiveFilterProxyModel - Recursive filtering of models
- KSelectionProxyModel - A Proxy Model which presents a subset of its
  source model to observers

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6ItemModels.so.6
%attr(755,root,root) %{_libdir}/libKF6ItemModels.so.*.*
%dir %{qt6dir}/qml/org/kde/kitemmodels
%attr(755,root,root) %{qt6dir}/qml/org/kde/kitemmodels/libitemmodelsplugin.so
%{qt6dir}/qml/org/kde/kitemmodels/qmldir
%{_datadir}/qlogging-categories6/kitemmodels.categories
%{_datadir}/qlogging-categories6/kitemmodels.renamecategories
%{_libdir}/qt6/qml/org/kde/kitemmodels/itemmodelsplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/kitemmodels/kde-qmlmodule.version

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KItemModels
%{_libdir}/cmake/KF6ItemModels
%{_libdir}/libKF6ItemModels.so
