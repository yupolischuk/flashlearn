#!/bin/bash

location=./flashlearn_`date +%Y_%m_%d_%H_%M_%S`.sql

### Input password as hidden characters ### 
read -s -p "Enter Password: "  pswd

mysqldump -uroot -p$pswd flashlearn > $location

echo 'dump complete'




