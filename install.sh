#!/bin/bash

# полный путь до скрипта
ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог в котором лежит скрипт
DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`



ln -s  $DIRECTORY/omsserv.py /usr/bin/omsserv.py 
cp $DIRECTORY/run/omsrun.service /etc/systemd/system/omsrun.service

$DIRECTORY/lib/smartcard/build_so.sh

systemctl daemon-reload
systemctl enable omsrun.service
systemctl start omsrun.service

echo "installing finished. Restart you system"
