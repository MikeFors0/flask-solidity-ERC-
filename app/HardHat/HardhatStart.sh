#! /usr/bin/sh

set -eu

clear;

echo "-------------------"
echo "Install Dependencies..."
echo "-------------------"
sudo npm install

echo "-------------------"
echo "Clean artifacts..."
echo "-------------------"
npx hardhat clean


sleep 2;
gnome-terminal -- npx hardhat node

echo "-------------------"
echo "Compile ..."
echo "-------------------"
sleep 3;
npx hardhat compile

echo "-------------------"
echo "Deploy contract ..."
echo "-------------------"
sleep 3;
npx hardhat run --network localhost scripts/deploy.js

echo "-------------------"
echo "Сеть запущенна и готова к работе"
echo "-------------------"
