#!/bin/bash
#Log Mapper installation script. Change variables below before running.

echo " _                  __  __                             "
echo "| |    ___   __ _  |  \/  | __ _ _ __  _ __   ___ _ __ "
echo "| |   / _ \ / _\` | | |\/| |/ _\` | '_ \| '_ \ / _ \ '__|"
echo "| |__| (_) | (_| | | |  | | (_| | |_) | |_) |  __/ |   "
echo "|_____\___/ \__, | |_|  |_|\__,_| .__/| .__/ \___|_|   "
echo "            |___/               |_|   |_|              "
sleep 1

LM_INSTALL_LOC="$PWD"
LM_MAPPER_USER="$USER"
LM_ATTEMPT_DB="test.db"
LM_STATS_DB="stats.dict"
CONF_FILE="logmapper.conf"
HOSTNAME=`hostname`


#Define environment variables
echo "[*] Creating $CONF_FILE"
echo "#Log Mapper Environment Variables" > $CONF_FILE
echo "LM_INSTALL_LOC=$LM_INSTALL_LOC" >> $CONF_FILE
echo "LM_MAPPER_USER=$LM_MAPPER_USER" >> $CONF_FILE
echo "LM_ATTEMPT_DB=$LM_ATTEMPT_DB" >> $CONF_FILE
echo "LM_STATS_DB=$LM_STATS_DB" >> $CONF_FILE


#Load variables just for fun
echo "[*] Loading environment variables"
. "/etc/os-release"
. "$CONF_FILE"


##### Package Dependencies
echo "[*] Installing packages"

#TODO: Manage packages for Python versions 2 and 3.
PACKAGES="python3-dev python-dev python3 python3-pip python-pip"

if [[ "$ID_LIKE" = "debian" ]]; then
    apt update -y
    apt install -y $PACKAGES
elif [[ "$ID_LIKE" = "rhel fedora" ]]; then
	yum update -y
	yum install -y $PACKAGES
fi


###### Python Dependencies
echo "[*] Installing dependencies for Python"
pip install -r requirements.txt
pip3 install flask
#echo "[*] Installing dependencies for Python3"
#pip3 install -r requirements.txt


#Install and set up caddy
echo "[*] Installing Caddy Server"
sudo -u $LM_MAPPER_USER curl https://getcaddy.com | bash -s personal


###### Caddy Reverse Proxy
echo "[*] Creating Caddyfile"
echo "$HOSTNAME {" > Caddyfile
echo "    proxy / localhost:5000" >> Caddyfile
echo "}" >> Caddyfile
cat Caddyfile

###### Services
echo "[*] Creating log files"
mkdir log
echo "Created logmapper-web.log" > log/logmapper-web.log
echo "Created logmapper-caddy.log" > log/logmapper-caddy.log

###### Add environment variables to services and scripts
echo "[*] Adding variables to services"
sed "/#LM_CONF/a LM_INSTALL_LOC='$LM_INSTALL_LOC'\nLM_MAPPER_USER='$LM_MAPPER_USER'" services/logmapper-web.service > services/logmapper-web.service.bak
mv services/logmapper-web.service.bak services/logmapper-web.service

sed "/#LM_CONF/a LM_INSTALL_LOC='$LM_INSTALL_LOC'\nLM_MAPPER_USER='$LM_MAPPER_USER'" services/logmapper-caddy.service > services/logmapper-caddy.service.bak
mv services/logmapper-caddy.service.bak services/logmapper-caddy.service
chmod +x services/*.service

sed "/#LM_CONF/a LM_INSTALL_LOC='$LM_INSTALL_LOC'\nLM_MAPPER_USER='$LM_MAPPER_USER'" update.sh > update.sh.bak
mv update.sh.bak update.sh
chmod +x update.sh

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


#Give user permissions instead of root
chown -R $LM_MAPPER_USER:$LM_MAPPER_USER $LM_INSTALL_LOC


#Install complete
echo ""
echo "[*] All set up. Go to https://www.duckdns.org/ to set up a free domain name. Otherwise, configure Caddyfile with your domain name. Then run \`caddy\` to register your domain with Let's Encrpt."
echo "[*] Press enter to run the update script for the first time..."
read nothing


#Run script for first time
bash $LM_INSTALL_LOC/update.sh
