# almost-universal-installer
Python script for automagically handling package installation in Arch Linux, Debian, Ubuntu and Fedora. 
Build with ❤️ for simsid66 to use with SDE

# How to use:

- Download the script, toss it somewhere, `import uni_install`. Dead simple!

# What it does:

There're a few notable functions:
- `getOS()`: Returns the ID of the **distro** or **base distro**, depending on `ID` or `ID_LIKE` in **/etc/os-release**
- `systemInstall()`: Install packages from a **Python list**, using the distro got from `getOS()`
- `systemUpdate()`: Same as `systemInstall()`, except for updating the system
- `checkRoot()`: A simple root access check. Used to stop `AURBuild()` and `gitBuild()` from running while having root access
- `AURBuild()`: Builds a package from AUR git link
- `gitBuild()`: `git clone`, `make` and `sudo make install` a git link
- `chkBuildEnvArch()`: Check if `makepkg` and `git` is present for AUR builds
- `setupBuildEnvArch()`: Setup build utils for AUR builds
- `chkBuildEnvGit()`: Check if `git`, `make` and build dependencies are present for git source builds
- `setupBuildEnvGit()`: Setup build utils for git source builds
- `netTest()`: Make a quick request to a server and report if it succeded or fails

# Things to watch out!

-  This script can only install the bare minimum for building Git packages. Packages that have other/optional dependencies must be installed with `systemInstall()`. `gitBuild()` won't try to install dependencies for you
