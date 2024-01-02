#!/bin/bash -e

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
PARENT_DIR=$(cd $(dirname $0);cd ..;/bin/pwd)
ROOT_DIR=${PARENT_DIR}

cd ${ROOT_DIR}
source ${ROOT_DIR}/venv/bin/activate
python3 kb1k_owntone.py

