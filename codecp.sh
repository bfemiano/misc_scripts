#!/bin/bash

if [ $# -lt 2 ]
then
   echo "usage: <trunk_from> <trunk_to>"
   exit 65
fi
rsync -avz --exclude .svn $1 $2
