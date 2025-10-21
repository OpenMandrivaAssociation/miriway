Name:           miriway
Version:        25.11
Release:        1
Summary:        Simple Wayland compositor built on Mir
License:        GPL-3.0-only
URL:            https://miriway.github.io/
Source0:        https://github.com/Miriway/Miriway/archive/v%{version}/Miriway-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  git-core
BuildRequires:  pkgconfig(miral)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  boost-exception-devel
BuildRequires:  boost-devel
Requires:       inotify-tools
Requires:       swaybg
Requires:       xkeyboard-config
Requires:       xwayland

%description
Miriway is a starting point for creating a Wayland based
desktop environment using Mir.

%package        session
Summary:        Miriway desktop session
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    session
This package contains configuration and dependencies for
the basic Miriway session.


%package -n sddm-wayland-%{name}
Summary:        Miriway SDDM greeter configuration
Provides:       sddm-greeter-displayserver
Conflicts:      sddm-greeter-displayserver
Requires:       %{name} = %{version}-%{release}
Requires:       layer-shell-qt
Supplements:    (sddm and %{name})
BuildArch:      noarch

%description -n sddm-wayland-%{name}
This package contains configuration and dependencies for SDDM
to use Miriway for the Wayland compositor for the greeter.


%package -n initial-setup-gui-wayland-%{name}
Summary:        Run initial-setup GUI on Miriway
Provides:       firstboot(gui-backend)
Conflicts:      firstboot(gui-backend)
Requires:       %{name} = %{version}-%{release}
Requires:       initial-setup-gui >= 0.3.99
Supplements:    ((initial-setup or initial-setup-gui) and %{name})
Enhances:       (initial-setup-gui and %{name})
BuildArch:      noarch

%description -n initial-setup-gui-wayland-%{name}
This package contains configuration and dependencies for
the initial-setup GUI to use Miriway for the Wayland
compositor.


%prep
%autosetup -n Miriway-%{version} -S git_am

# Drop -Werror
sed -e "s/-Werror//g" -i CMakeLists.txt


%build
# Deal with some goofiness around sysconfdir
%cmake -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} -DSDDM=ON
%make_build


%install
%make_install -C build

# Remove miriway-unsnap as it's kind of pointless
rm -f %{buildroot}%{_bindir}/%{name}-{unconfine,unsnap}

# move sddm configuration snippet to the right place
mkdir -p %{buildroot}%{_prefix}/lib/sddm
mv %{buildroot}%{_sysconfdir}/sddm.conf.d %{buildroot}%{_prefix}/lib/sddm

# install initial-setup-gui backend script
#mkdir -p %{buildroot}%{_libexecdir}/initial-setup
#install -pm 0755 %{S:1} %{buildroot}%{_libexecdir}/initial-setup/run-gui-backend


%files
%doc README.md CONFIGURING_MIRIWAY.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-background
%{_bindir}/%{name}-run
%{_bindir}/%{name}-run-shell
%{_bindir}/%{name}-shell
%{_bindir}/%{name}-terminal
%dir %{_sysconfdir}/xdg/xdg-%{name}
%config(noreplace) %{_sysconfdir}/xdg/xdg-%{name}/%{name}-shell.config

%files session
%doc example-configs
%{_bindir}/%{name}-session
%{_libexecdir}/%{name}-session*
%{_datadir}/wayland-sessions/%{name}.desktop
%{_userunitdir}/%{name}-session.target

%files -n sddm-wayland-%{name}
%{_prefix}/lib/sddm/sddm.conf.d/%{name}.conf
