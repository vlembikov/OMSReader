#!/bin/bash

# полный путь до скрипта
ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог в котором лежит скрипт
DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`

ln -s  $DIRECTORY/omsserv.py /usr/bin/omsserv.py 
ln -s $DIRECTORY/run/omsrun.sh /usr/bin/omsrun.sh
cp $DIRECTORY/run/omsrun.service /etc/systemd/system/omsrun.service
systemctl daemon-reload
systemctl enable omsrun.service
systemctl start omsrun.service
