# MorvaneOS build environment: Artix + artools-iso, plus base-devel for makepkg (pack).
# Built and run by compile; the repo itself is mounted in at run time, not copied.
FROM artixlinux/artixlinux:latest

COPY build-env/mirrorlist /etc/pacman.d/mirrorlist

# Our own repo, above Artix's, so packages can depend on each other (e.g.
# morvane-installer needs python-pyparted). TrustAll until packages are signed.
RUN sed -i '/^\[system\]/i [morvane]\nSigLevel = Optional TrustAll\nServer = https://morvane.doughmination.gay/$repo/os/$arch\n' /etc/pacman.conf

RUN pacman -Syu --noconfirm --needed artools-iso base-devel \
 && pacman -Scc --noconfirm
