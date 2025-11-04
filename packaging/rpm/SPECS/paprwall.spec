Name:           paprwall
Version:        1.0.2
Release:        1%{?dist}
Summary:        Modern Desktop Wallpaper Manager with Motivational Quotes

License:        MIT
URL:            https://github.com/riturajprofile/paprwall
Source0:        paprwall-%{version}.tar.gz

BuildArch:      x86_64
Requires:       python3 >= 3.8
Requires:       python3-tkinter
Requires:       python3-pillow
Requires:       python3-requests

%description
PaprWall is a modern desktop application that helps you manage your
wallpapers with embedded motivational quotes. Features include auto-rotation,
6 quote categories, large preview panel, history gallery, and support for
GNOME, KDE, XFCE, MATE, and Cinnamon desktop environments.

%prep
%setup -q

%build
# Binary already built

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps
mkdir -p $RPM_BUILD_ROOT/usr/share/paprwall

install -m 755 paprwall-gui $RPM_BUILD_ROOT/usr/local/bin/
install -m 644 paprwall.desktop $RPM_BUILD_ROOT/usr/share/applications/
install -m 644 paprwall.svg $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps/

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || :
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database /usr/share/applications 2>/dev/null || :
fi
echo ""
echo "=========================================="
echo "  PaprWall v1.0.2 Installed Successfully!"
echo "=========================================="
echo ""
echo "You can now:"
echo "  • Find 'PaprWall' in your application menu"
echo "  • Run: paprwall-gui"
echo ""
echo "To uninstall:"
echo "  sudo dnf remove paprwall"
echo "  # or: sudo yum remove paprwall"
echo ""

%postun
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || :
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database /usr/share/applications 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
/usr/local/bin/paprwall-gui
/usr/share/applications/paprwall.desktop
/usr/share/icons/hicolor/scalable/apps/paprwall.svg

%changelog
* Mon Nov 04 2025 riturajprofile <riturajprofile@example.com> - 1.0.2-1
- Added auto-install prompt on first run
- Added --install and --uninstall command-line options
- Added GUI uninstall button
- Improved desktop integration

* Sun Nov 03 2025 riturajprofile <riturajprofile@example.com> - 1.0.0-1
- Initial release
