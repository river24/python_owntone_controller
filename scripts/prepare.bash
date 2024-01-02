#!/bin/bash

# PATH設定
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
export PATH=${PATH}

# スクリプト名を取得
SCRIPT_NAME=${0##*/}

# 各種ディレクトリ情報を変数に格納
CURRENT_DIR=$(/bin/pwd)
SCRIPT_DIR=$(cd $(dirname $0);/bin/pwd)
PARENT_DIR=$(cd $(dirname $0);cd ..;/bin/pwd)
ROOT_DIR=${PARENT_DIR}

# prepare
cd ${ROOT_DIR}
if [ ! -d venv ] ; then
  python3 -m venv venv
fi
source venv/bin/activate
pip3 install -r requirements.txt

