#!/bin/bash

# if [ $# -ne 1 ]; then
#   echo "Usage: $0 <path_to_paper>"
#   exit -1
# fi
# PAPER=$1
# USER_NAME=""
# 
# echo "Publishing $PAPER to group lunch website"
# 
# if [ -z "${SUNETID}" ]; then
#   echo -n "SUNETID variable not SET. SUNet ID: "
#   read USER_NAME
# else
#   USER_NAME=${SUNETID}
# fi
# 
# scp $PAPER $USER_NAME@ppl.stanford.edu:/kunle/web/html/kogroup/lunch/$PAPER
# 
# if [ -z "${SUNETID}" ]; then
#   WHITE='\033[1;37m'
#   NC='\033[0m'
#   echo -e "${WHITE}Set the SUNETID environment variable to avoid entering it every time${NC}"
# fi

cp ./main.pdf /Users/tianzhao/Dropbox/SYSML_RNN_DRAFT/
