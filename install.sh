#!/bin/bash

echo "Updating system..."
apt update -y

echo "Installing dependencies..."
apt install python3 python3-venv python3-pip git -y

echo "Enter your Telegram Bot Token:"
read BOT_TOKEN

mkdir -p /opt/subbot
cd /opt/subbot

echo "Cloning repository..."
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Creating systemd service..."

cat > /etc/systemd/system/subbot.service <<EOL
[Unit]
Description=Telegram Subscription Convert Bot
After=network.target

[Service]
User=root
WorkingDirectory=/opt/subbot
Environment=BOT_TOKEN=$BOT_TOKEN
ExecStart=/opt/subbot/venv/bin/python /opt/subbot/sub_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload
systemctl enable subbot
systemctl start subbot

echo "Installation Complete!"
echo "Bot is now running permanently 🚀"
