#!/bin/bash
#Log Mapper installation script. Change variables below before running.

echo " _                  __  __                             "
echo "| |    ___   __ _  |  \/  | __ _ _ __  _ __   ___ _ __ "
echo "| |   / _ \ / _` | | |\/| |/ _` | '_ \| '_ \ / _ \ '__|"
echo "| |__| (_) | (_| | | |  | | (_| | |_) | |_) |  __/ |   "
echo "|_____\___/ \__, | |_|  |_|\__,_| .__/| .__/ \___|_|   "
echo "            |___/               |_|   |_|              "

LM_INSTALL_LOC=$PWD
LM_MAPPER_USER=$USER
LM_ATTEMPT_DB="test.db"
LM_STATS_DB="stats.dict"
CONF_FILE="logmapper.conf"
HOSTNAME=`hostname`


#Define environment variables
echo "[*] Creating $CONF_FILE"
echo "#Log Mapper Environment Variables"
echo "LM_INSTALL_LOC=$LM_INSTALL_LOC" >> $CONF_FILE
echo "LM_MAPPER_USER=$LM_MAPPER_USER" >> $CONF_FILE
echo "LM_ATTEMPT_DB=$LM_ATTEMPT_DB" >> $CONF_FILE
echo "LM_STATS_DB=$LM_STATS_DB" >> $CONF_FILE


#Load variables just for fun
echo "[*] Loading environment variables"
. "$CONF_FILE"

##### Package Dependencies
echo "[*] Installing packages"

PACKAGES="python3 python-pi"

if [[ "$ID_LIKE" = "debian" ]]; then
    apt update -y
    apt install -y $PACKAGES
elif [[ "$ID_LIKE" = "rhel fedora" ]]; then
	yum update -y
	yum install -y $PACKAGES
fi


###### Python Dependencies
echo "[*] Installing dependencies for Python2"
pip install -r requirements.txt
echo "[*] Installing dependencies for Python3"
pip3 install -r requirements.txt


#Install and set up caddy
echo "[*] Installing Caddy Server"
curl https://getcaddy.com | bash -s personal


###### Caddy Reverse Proxy
echo "[*] Creating Caddyfile"
echo "$HOSTNAME {" > Caddyfile
echo "    proxy / localhost:5000" >> Caddyfile
echo "}" >> Caddyfile


###### Services
echo "[*] Creating log files"
mkdir log
echo "Created logmapper-web.log" > log/logmapper-web.log
echo "Created logmapper-caddy.log" > log/logmapper-caddy.log


#Link services
echo "[*] Adding services to rc.local"
echo "$LM_INSTALL_LOC/services/logmapper-caddy.service start" >> /etc/rc.local
echo "$LM_INSTALL_LOC/services/logmapper-web.service start" >> /etc/rc.local
#Start services
echo "[*] Starting services"
#$LM_INSTALL_LOC/services/logmapper-caddy.service start
$LM_INSTALL_LOC/services/logmapper-web.service start


#Create cronjobs
echo "[*] Creating cronjobs"
crontab -l > logmapper.cron
echo "*/30 * * * * $LM_INSTALL_LOC/update.sh | tee $LM_INSTALL_LOC/log/logmapper-update.log" > logmapper.cron
crontab logmapper.cron
rm logmapper.cron


chown -$R $LM_MAPPER_USER:$LM_MAPPER_USER $LM_INSTALL_LOC

echo "[*] All set up. Go to https://www.duckdns.org/ to set up a free domain name. Otherwise, configure Caddyfile with your domain name. Then run `caddy` to register your domain with Let's Encrpt."
echo "[*] Press enter to run the update script for the first time..."
read temp

#Run script for first time
bash $LM_INSTALL_LOC/update.sh
