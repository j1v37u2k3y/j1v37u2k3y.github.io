#!/bin/bash
IL="${1}"
working_dir="./nmap/${IP}"
mkdir -p "${working_dir}"
wget https://j1v37u2k3y.github.io/assets/reports/nmap/nmap-bootstrap.xsl -O ~/nmap-bootstrap.xsl
nmap -n -vvv -sS -sV -sC -p- -oA "${working_dir}"/version --stylesheet ~/nmap-bootstrap.xsl -iL "${IL}"
