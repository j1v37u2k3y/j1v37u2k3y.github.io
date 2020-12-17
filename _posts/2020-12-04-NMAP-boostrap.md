---
layout: post
title:  NMAP Bootstrap
category: admin
tags: [nmap, bootstrap]
published: true
author: j1v37u2k3y
searchable: true
---
Nmap boostrap makes it easier to display nmap scan results in the browser.
<!--cut-->

* TOC
{:toc}

# NMAP Boostrap 

 - [https://github.com/honze-net/nmap-bootstrap-xsl](https://github.com/honze-net/nmap-bootstrap-xsl)

```
mkdir nmap
nmap -n -vvv -sS -sV -sC -p- -oA nmap/version --stylesheet https://j1v37u2k3y.github.io/assets/reports/nmap/nmap-bootstrap.xsl 192.168.9.130
```

## Then create the html file

```
xsltproc -o version.html /root/nmap-bootstrap.xsl version.xml
```
