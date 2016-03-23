#!/bin/bash

# полный путь до скрипта
ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог в котором лежит скрипт
DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`

PYV=`python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`

if [ "$PYV" \> "2.9.9.9" ]; then
    PYV="${PYV}m"
fi

swig -python -outdir scard -DPCSCLITE -o scard/scard_wrap.c scard/scard.i  

gcc -pthread -fno-strict-aliasing -fmessage-length=0 -grecord-gcc-switches -O2 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -g -DNDEBUG -fmessage-length=0 -grecord-gcc-switches -O2 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -g -DOPENSSL_LOAD_CONF -fPIC -DVER_PRODUCTVERSION=1,9,2,0000 -DVER_PRODUCTVERSION_STR=1.9.2 -DPCSCLITE=1 -Iscard/ -I/usr/include/PCSC -I/usr/include/python${PYV} -c scard/helpers.c -o scard/helpers.o


gcc -pthread -fno-strict-aliasing -fmessage-length=0 -grecord-gcc-switches -O2 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -g -DNDEBUG -fmessage-length=0 -grecord-gcc-switches -O2 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -g -DOPENSSL_LOAD_CONF -fPIC -DVER_PRODUCTVERSION=1,9,2,0000 -DVER_PRODUCTVERSION_STR=1.9.2 -DPCSCLITE=1 -Iscard/ -I/usr/include/PCSC -I/usr/include/python${PYV} -c scard/winscarddll.c -o scard/winscarddll.o

gcc -pthread -fno-strict-aliasing -fmessage-length=0 -grecord-gcc-switches -O2 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -g -DNDEBUG -fmessage-length=0 -grecord-gcc-switches -O2 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -g -DOPENSSL_LOAD_CONF -fPIC -DVER_PRODUCTVERSION=1,9,2,0000 -DVER_PRODUCTVERSION_STR=1.9.2 -DPCSCLITE=1 -Iscard/ -I/usr/include/PCSC -I/usr/include/python${PYV} -c scard/scard_wrap.c -o scard/scard_wrap.o

gcc -pthread -shared scard/helpers.o scard/winscarddll.o scard/scard_wrap.o -L/usr/lib -lpython${PYV} -o scard/_scard.so
