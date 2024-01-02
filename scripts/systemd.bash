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

# run
${ROOT_DIR}/scripts/run.bash

