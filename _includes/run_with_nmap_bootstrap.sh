#!/bin/bash
IP="<IP_ADDRESS>"
working_dir="${HOME}/nmap/${IP}"
mkdir "${working_dir}"
wget https://j1v37u2k3y.github.io/assets/reports/nmap/nmap-bootstrap.xsl ~/nmap-bootstrap.xsl
nmap -n -vvv -sS -sV -sC -p- -oA "${working_dir}"/version --stylesheet ~/nmap-bootstrap.xsl "${IP}"
