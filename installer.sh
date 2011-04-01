mkdir install
cd install

#Base installation
sudo apt-get install git-core
sudo apt-get install python
sudo apt-get install python-setuptools
sudo apt-get install swig
sudo apt-get install python-dev

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
sudo apt-get install python-numpy

#scipy
sudo apt-get install python-scipy

#PyMVPA installation
git clone https://github.com/PyMVPA/PyMVPA.git
cd PyMVPA
sudo python setup.py install
cd ..

#Django installation
wget http://media.djangoproject.com/releases/1.3/Django-1.3.tar.gz
tar xzvf Django-1.3.tar.gz
cd Django-1.3
sudo python setup.py install
cd ..

#MySQL Installation
sudo apt-get install mysql-server
sudo apt-get install python-mysqldb 
