#!/bin/bash
sudo /sbin/SystemStarter stop iCoreService
killall TmLoginMgr
sudo /Library/StartupItems/sysaid/sysaid stop