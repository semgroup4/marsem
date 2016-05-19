python3 setup.py clean
python3 setup.py sdist
cd source
tar xf ../dist/MarsemServer-*.tar.gz
cd ..
#cat ~/.ssh/id_rsa.pub | ssh user@hostname 'cat >> .ssh/authorized_keys'
ssh pi@192.168.2.1 'rm -r /home/pi/marsem/* && exit'
scp -r source/MarsemServer-*/server pi@192.168.2.1:/home/pi/marsem/
