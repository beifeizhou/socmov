#!/bin/bash 
function replace {
	if [ $# == 5 ]; then
		tt1="$1 $2"
		tt2="$3 $4"
		tt3=$5
		t="_TEMP"
		newfile="$tt3$t" 
		sudo cp -R --preserve $tt3 $newfile
		sed -e "s|$tt1|$tt2|g" $newfile > $tt3
		sudo rm $newfile
	else
		t="_TEMP"
		newfile="$3$t" 
		sudo cp -R --preserve $3 $newfile
		sed -e "s|$1|$2|g" $newfile > $3
		sudo rm $newfile	
	fi
}

function rename {
	sudo mv $1 $2
}

#apache
ipaddress=$1
servername=$2
CUR_PATH=$(dirname $(readlink -f $0))
DEFAULT_PATH="/home/maniks/socmov"
sudo cp -R --preserve server_setup/localhost_apache /etc/apache2/sites-available/localhost
sudo cp -R --preserve server_setup/httpd.conf /etc/apache2/httpd.conf
#echo -n "Enter domain name ( eg.google.com for www.google.com ) : "
#read servername
if [ "$servername" != "localhost" ]; then
	tmp="ServerName localhost"
	tmp2="ServerName www.$servername"
	replace $tmp $tmp2 /etc/apache2/sites-available/localhost
	replace "localhost" $servername /etc/apache2/sites-available/localhost
fi

replace $DEFAULT_PATH $CUR_PATH /etc/apache2/sites-available/localhost
replace $DEFAULT_PATH $CUR_PATH /etc/apache2/httpd.conf
rename /etc/apache2/sites-available/localhost "/etc/apache2/sites-available/$servername"
sudo ln -s "/etc/apache2/sites-available/$servername" "/etc/apache2/sites-enabled/$servername"

#echo -n "Enter IP address: "
#read ipaddress
sudo cp -R --preserve server_setup/ports.conf /etc/apache2/ports.conf
replace "127.0.0.1" $ipaddress /etc/apache2/ports.conf


#nginx
sudo rm /etc/nginx/sites-enabled/default
sudo cp -R --preserve server_setup/nginx.conf /etc/nginx/nginx.conf
sudo cp -R --preserve server_setup/proxy.conf /etc/nginx/proxy.conf
sudo cp -R --preserve server_setup/localhost_nginx /etc/nginx/sites-available/localhost

replace $DEFAULT_PATH $CUR_PATH /etc/nginx/sites-available/localhost
if [ "$servername" != "localhost" ]; then
	tmp="localhost localhost"
	tmp2="www.$servername $servername"
	replace $tmp $tmp2 /etc/nginx/sites-available/localhost
fi
replace "127.0.0.1" $ipaddress /etc/nginx/sites-available/localhost
rename /etc/nginx/sites-available/localhost "/etc/nginx/sites-available/$servername"
sudo ln -s "/etc/nginx/sites-available/$servername" "/etc/nginx/sites-enabled/$servername"


#apache directory in django project, copying the wsgi file
sudo cp -R --preserve server_setup/socmov.wsgi apache/socmov.wsgi
replace $DEFAULT_PATH $CUR_PATH apache/socmov.wsgi

#final command needed to run for apache : http://forum.webfaction.com/viewtopic.php?id=2282
export DJANGO_SETTINGS_MODULE=socmov.settings

#restart apache and nginx
sudo /etc/init.d/apache2 restart 
sudo /etc/init.d/nginx restart 
