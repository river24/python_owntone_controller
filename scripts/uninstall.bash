#!/bin/bash

SERVICE_NAME="kb1k_owntone"

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

# uninstall
if [ -f /etc/systemd/system/${SERVICE_NAME}.service ] ; then
  systemctl stop ${SERVICE_NAME}.service
  systemctl disable ${SERVICE_NAME}.service
  rm /etc/systemd/system/${SERVICE_NAME}.service
fi
systemctl daemon-reload

