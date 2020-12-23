---
layout: post
title:  Y0usef 1 Vulnhub Writeup
category: ctfs
tags: [vulnhub, ctf, php, linux, php-reverse-shell]
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

<a href="{{ site.baseurl }}/assets/reports/nmap/vulnhub/bluesky/version.html" target="_blank" title="Y0usef NMAP Scan">Y0usef NMAP Scan</a> 


# There is a forbidden directory under adminstration

```text
[00:15:06] Starting:                                                                                                                     
[00:15:06] 403 -  313B  - /adminstration/.htaccess.php
[00:15:07] 403 -  314B  - /adminstration/.htpasswd.html
[00:15:07] 403 -  312B  - /adminstration/.htpasswd.js
[00:15:07] 403 -  312B  - /adminstration/.htaccess.js
[00:15:07] 403 -  313B  - /adminstration/.htpasswd.php
[00:15:07] 403 -  313B  - /adminstration/.htpasswd.txt
[00:15:07] 403 -  314B  - /adminstration/.htaccess.html
[00:18:21] 301 -  326B  - /adminstration/include  ->  http://192.168.5.8/adminstration/include/
[00:18:21] 200 -    1KB - /adminstration/include/
[00:18:21] 403 -   75B  - /adminstration/index.php
[00:18:51] 301 -  325B  - /adminstration/logout  ->  http://192.168.5.8/adminstration/logout/
[00:21:33] 301 -  325B  - /adminstration/upload  ->  http://192.168.5.8/adminstration/upload/
[00:21:36] 301 -  324B  - /adminstration/users  ->  http://192.168.5.8/adminstration/users/

```

### Had to login as guest to the VM to get the code base to understand what was happening. (The author said he had screwed some stuff up)

#### Mess with headers

[![](/assets/images/vulnhub/y0usef/6054fdaf.png)](/assets/images/vulnhub/y0usef/6054fdaf.png)

# Login with admin:admin

[![](/assets/images/vulnhub/y0usef/6e55a6ac.png)](/assets/images/vulnhub/y0usef/6e55a6ac.png)

## Can upload a file

[![](/assets/images/vulnhub/y0usef/0c4ebbc2.png)](/assets/images/vulnhub/y0usef/0c4ebbc2.png)

# Set up our reverse shell
[![](/assets/images/vulnhub/y0usef/c5b17c99.png)](/assets/images/vulnhub/y0usef/c5b17c99.png)

[![](/assets/images/vulnhub/y0usef/eaabb7b3.png)](/assets/images/vulnhub/y0usef/eaabb7b3.png)

## Login in via ssh as yousef

[![](/assets/images/vulnhub/y0usef/3aecf34c.png)](/assets/images/vulnhub/y0usef/3aecf34c.png)

# ROOT

[![](/assets/images/vulnhub/y0usef/ddf3a8bd.png)](/assets/images/vulnhub/y0usef/ddf3a8bd.png)

## base64 decode the message

[![](/assets/images/vulnhub/y0usef/f517a90a.png)](/assets/images/vulnhub/y0usef/f517a90a.png)

```text
You've got the root Congratulations any feedback content me twitter @y0usef_11
```


