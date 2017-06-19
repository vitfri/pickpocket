FROM debian:jessie
#
# These variables configure the build.
#
ENV SUITE jessie
#
# [Leave surrounding comments to eliminate merge conflicts]
#
# Configure & update apt
ENV DEBIAN_FRONTEND noninteractive
RUN echo 'APT::Install-Recommends "0";\nAPT::Install-Suggests "0";' > \
        /etc/apt/apt.conf.d/01norecommend
RUN apt-get update
RUN apt-get upgrade -y
# silence debconf warnings
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y libfile-fcntllock-perl

# Install and configure sudo, passwordless for everyone
RUN apt-get -y install sudo
RUN echo "ALL	ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers

###########################################
# Install packages
#
# Customize the following for building/running targeted software

# Basic dev tools
RUN apt-get install -y \
	git \
	build-essential \
	devscripts \
	fakeroot \
	equivs \
	lsb-release \
	less \
	python-debian \
	libtool \
	ccache

# Python dev and install tools
RUN apt-get install -y \
	python-dev \
	python-pyside \
	pyside-tools \
	python-pip

# Build deps for following python packages
RUN apt-get install -y \
	pkg-config \
	libssl-dev \
	libffi-dev \
	autoconf \
	automake

# Python package deps for pyethrecover_v3
RUN pip install -U \
	joblib \
	rlp \
	ethereum \
	bitcoin \
	Crypto


###########################################
# Set up environment
#
# Customize the following to match the user's environment

# Set up user ID inside container to match your ID
ENV USER joeuser
ENV UID 1000
ENV GID 1000
ENV HOME /home/${USER}
ENV SHELL /bin/bash
RUN echo "${USER}:x:${UID}:${GID}::${HOME}:${SHELL}" >> /etc/passwd
RUN echo "${USER}:x:${GID}:" >> /etc/group

# Customize the run environment to your taste
# - bash prompt
# - 'ls' alias
RUN sed -i /etc/bash.bashrc \
    -e 's/^PS1=.*/PS1="\\h:\\W\\$ "/' \
    -e '$a alias ls="ls -aFs"'
