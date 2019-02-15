#!/bin/sh
echo ""
echo "Choose the app to Deploy"
echo "----------------------------------------------------"
echo "1. Frontend"
echo "2. Backend"
echo "3. Both"
read -p "Enter the Number of the App : " id
argument=$id
if [ $argument == 1 ]
then
   echo "Deploying Frontend Code"
   cd ~/Parts/frontend
   echo "Updating the code from the git ...."
   git pull
   echo "Deleting existing docker images and containers ...."
   docker rm -f frontend
   docker rmi frontend
   cd ~/Parts/compose
   docker-compose up -d frontend
elif [ $argument == 2 ]
then
   echo "Deploying Backend Code"
   cd ~/Parts/backend
   echo "Updating the code from the git ...."
   git pull
   echo "Deleting existing docker images and container ..."
   docker rm -f backend
   docker rmi backend
   cd ~/Parts/compose
   docker-compose up -d backend
elif [ $argument == 3 ]
then
   echo "Deploying Backend and Frontend Code"
   cd ~/Parts/backend
   echo	"Updating the code from	the git	...."
   git pull
   echo	"Deleting existing docker images and container ..."
   docker rm -f	backend frontend
   docker rmi backend frontend
   cd ~/Parts/compose
   docker-compose up -d	frontend
else
   echo "Invalid Argument"
fi
