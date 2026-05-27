#!/bin/bash

export ASPIRE_VERSION='17.4.0'

function start_aspire_here() {
    singularity shell --nv ~/01_Software/ASPIRE_devel_$ASPIRE_VERSION/aspkit-devel-cuda12.6.3-ubuntu24.04-x86_64_$ASPIRE_VERSION.sif
}

function install_aspire_devel_version() {
    echo Running from $0
    if [ $# -gt 1 ]; then
        echo ERROR Too many arguments given! Only give the version number, i.e. 17.1.0
        return
    fi
    
    mkdir ~/01_Software/ASPIRE_devel_$1
    cd ~/01_Software/ASPIRE_devel_$1
    singularity pull --docker-login docker://registry.whffl.nl/aspkit-license/aspkit-devel-cuda12.6.3-ubuntu24.04-x86_64:$1
}