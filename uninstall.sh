#!/bin/bash

# полный путь до скрипта
ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог в котором лежит скрипт
DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`



rm /usr/bin/omsserv.py 
rm /etc/systemd/system/omsrun.service

cd $DIRECTORY/lib/smartcard/scard/

rm scard_wrap.o
rm scard_wrap.c
rm helpers.o
rm winscarddll.o
rm _scard.so

systemctl daemon-reload


echo "uninstalling finished"
