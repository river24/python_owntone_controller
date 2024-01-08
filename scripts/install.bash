#!/bin/bash

SERVICE_NAME="python_owntone_controller"

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

# 実行ユーザの確認
if [ ${UID} -eq 0 ] || [ -z ${SUDO_USER} ] ; then
  :
else
  echo "This script is expected to be called by 'root' (uid=0) via 'sudo' command." >&2
  exit 1
fi

# install
USER=${SUDO_USER} ROOT_DIR=${ROOT_DIR} envsubst < ${ROOT_DIR}/configs/systemd.base > /etc/systemd/system/${SERVICE_NAME}.service

systemctl daemon-reload

systemctl enable ${SERVICE_NAME}.service
systemctl start ${SERVICE_NAME}.service

