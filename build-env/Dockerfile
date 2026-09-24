# MorvaneOS build environment: Artix + artools-iso.
# Built and run by build.sh; the repo itself is mounted in at run time, not copied.
FROM artixlinux/artixlinux:latest

COPY build-env/mirrorlist /etc/pacman.d/mirrorlist

RUN pacman -Syu --noconfirm artools-iso \
 && pacman -Scc --noconfirm
