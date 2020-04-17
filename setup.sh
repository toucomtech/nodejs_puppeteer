#################
# RUN WITH SUDO #
#################

# Update apt
apt-get update

# Install chromium if not already installed
apt-get install -y chromium-browser

# Download nodejs specific to your processor
# Install nodejs and remove artifacts
wget https://nodejs.org/dist/v12.16.2/node-v12.16.2-linux-armv7l.tar.xz
tar -xf node-v12.16.2-linux-armv7l.tar.xz
cd node-v12.16.2-linux-armv7l
cp -R * /usr/local
cd ..
rm node-v12.16.2-linux-armv7l.tar.xz
rm -Rf node-v12.16.2-linux-armv7l

# Initialize nodejs directory and install puppeteer-core
npm init -y
npm i puppeteer-core

# Restore permissions to user account
chown -R $SUDO_USER:$SUDO_USER *
