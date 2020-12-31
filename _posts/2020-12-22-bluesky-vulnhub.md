---
layout: post
title:  Bluesky Vulnhub Writeup
category: ctfs
tags: [vulnhub, ctf, apache-tomcat, struts-2]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---
Difficulty: Easy

Goal: Get the root shell i.e.(root@localhost:~#) and then obtain flag under /root).

Information: Your feedback is appreciated - Email: suncsr.challenges@gmail.com

Tested: VMware Workstation 16.x Pro (This works better with VMware rather than VirtualBox)

<!--cut-->

* TOC 
{:toc}

# NMAP

<a href="{{ site.baseurl }}/assets/reports/nmap/vulnhub/bluesky/version.html" target="_blank" title="Bluesky NMAP Scan">Bluesky NMAP Scan</a> 


## 22 and 8080 is open

| Port | Protocol | State Reason | Service | Product       | Version | Extra Info |
| ---- | ----     | ----         | ----    | ----          | ----    | ----       |
| 22	 |  tcp	    | open syn-ack | ssh	   | OpenSSH       |7.2p2 Ubuntu 4ubuntu2.10 |	Ubuntu Linux; protocol 2.0 |
| 8080 |	tcp	    | open syn-ack | http    | Apache Tomcat |	9.0.40 |            |


### Seems admin:admin lets us into the manager application 

[![](/assets/images/vulnhub/bluesky/access-to-backend.png)](/assets/images/vulnhub/bluesky/access-to-backend.png)

#### So we pass the header into dirsearch

```shell
dirsearch -u http://bluesky:8080/ -e php,js,txt,jsp,asp,md,json,html,htm -w /usr/share/wordlists/dirb/big.txt -H "Authorization: Basic YWRtaW46YWRtaW4=" -t 100 --exclude-subdirs "/docs/,examples/" -R 3 
 ```
