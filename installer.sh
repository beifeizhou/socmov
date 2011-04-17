cp /etc/apt/sources.list /etc/apt/sources.list.backup
cat repos.txt >> /etc/apt/sources.list
apt-get update

mkdir apache
mkdir logs
mkdir media
mkdir install
cd install

#Base installation
sudo apt-get install git-core python python-setuptools swig python-dev mysql-server python-mysqldb 

#The Movie Database Python SDK Installation
git clone https://github.com/doganaydin/themoviedb.git
cd themoviedb
sudo python setup.py install
cd ..

#Facebook Python SDK Installation
git clone https://github.com/facebook/python-sdk.git
cd python-sdk
sudo python setup.py install
cd ..

#numpy
#sudo apt-get install python-numpy

#scipy
#sudo apt-get install python-scipy

#PyMVPA installation
#git clone https://github.com/PyMVPA/PyMVPA.git
#cd PyMVPA
#sudo python setup.py install
#cd ..

#Django installation
wget http://media.djangoproject.com/releases/1.3/Django-1.3.tar.gz
tar xzvf Django-1.3.tar.gz
cd Django-1.3
sudo python setup.py install
cd ..

#Create MySQL Database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS socmovdb;"

#wget http://www.csie.ntu.edu.tw/~cjlin/libsvm/libsvm-3.1.tar.gz
#tar xzvf libsvm-3.1.tar.gz
#cd libsvm-3.1
#make

#sudo apt-get install libsvm-tools
#sudo apt-get install libsvm-dev
#sudo apt-get install python-libsvm
#Apache stuff
sudo apt-get install sed
sudo apt-get install apache2.2-common apache2
sudo apt-get install nginx
sudo apt-get install libapache2-mod-wsgi
