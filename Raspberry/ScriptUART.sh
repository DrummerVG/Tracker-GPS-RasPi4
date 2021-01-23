#!bin/bash

#Script para configuracion y activacion el puerto UART[i](2-5)

cd ..
cd ..
cd boot/
echo "dtoverlay="$1 >> config.txt
sudo reboot now
