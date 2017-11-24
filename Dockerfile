FROM centos:latest

RUN yum -y update
RUN yum -y groupinstall "Development Tools"
RUN yum -y install \
  kernel-devel \
  kernel-headers \
  gcc-c++ \
  patch \
  libyaml-devel \
  autoconf \
  automake \
  make \
  libtool \
  bison \
  tk-devel \
  zip \
  wget \
  tar \
  gcc \
  zlib \
  zlib-devel \
  bzip2 \
  bzip2-devel \
  readline \
  readline-devel \
  sqlite \
  sqlite-devel \
  openssl \
  openssl-devel \
  git \
  gdbm-devel \
  python-devel


# LANG Setting
RUN rm -f /etc/rpm/macros.image-language-conf && \
    sed -i '/^override_install_langs=/d' /etc/yum.conf && \
    yum -y reinstall glibc-common && \
    yum clean all
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"


# python3 Install
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y \
  python35u \
  python35u-libs \
  python35u-devel \
  python35u-pip


# Alias Setting
RUN ln -s /usr/bin/python3.5 /usr/bin/python3
RUN unlink /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3.5 /usr/bin/pip


# Library install
RUN pip install \
  numpy \
  pyyaml \
  scipy \
  scikit-learn \
  pillow \
  h5py \
  tensorflow \
  keras \
  flask

CMD ["/bin/bash"]
