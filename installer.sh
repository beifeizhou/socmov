#Base installation
sudo apt-get install git-core
sudo apt-get install python

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
git clone git://github.com/numpy/numpy.git
cd numpy
sudo python setup.py install
cd ..
#scipy
git clone git://github.com/scipy/scipy.git scipy
cd scipy
sudo python setup.py install
cd ..

#PyMVPA installation
git clone https://github.com/PyMVPA/PyMVPA.git
sudo apt-get install python-setuptools
sudo apt-get install swig
sudo apt-get install python-dev
cd PyMVPA
sudo python setup.py install
cd ..

#Django installation
wget http://media.djangoproject.com/releases/1.3/Django-1.3.tar.gz
tar xzvf Django-1.3.tar.gz
cd Django-1.3
sudo python setup.py install
cd ..
