#!/usr/bin/env bash

# dependencies for liboqs
sudo apt update 

sudo apt install -y astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind
git clone -b main https://github.com/open-quantum-safe/liboqs.git
cd liboqs

mkdir build && cd build
cmake -GNinja -DBUILD_SHARED_LIBS=ON -DOQS_MINIMAL_BUILD="SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87" ..
ninja

sudo ninja install

cd

sudo ldconfig

# Installing modify version of unbound
git clone https://github.com/HuMiTriet/unbound.git

sudo apt-get install -y pkg-config autoconf-archive
sudo apt install -y build-essential libssl-dev libexpat1-dev bison flex

cd unbound

autoreconf -vfi

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig

./configure --enable-debug --enable-filter --enable-oqs

make 

sudo make install

cd


# setup unbound
sudo useradd -r -s /bin/false unbound
