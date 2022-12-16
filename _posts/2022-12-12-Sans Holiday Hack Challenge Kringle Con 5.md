---
layout: post
title:  Sans Holiday Hack Challenge Kringle Con 5
categories: ctfs
tags: [sans, ctf]
published: true
author: j1v37u2k3y, weirdatfirst
show_sidebar: true
toc: true
searchable: true
---
The 2022 SANS Holiday Hack Challenge
Featuring KringleCon 5: Golden Rings!
Welcome to this year's SANS Holiday Hack Challenge! We can't wait for you to hop in the game and share some holiday cheer as you build vital cybersecurity skills.

Before you start, we have two urgent messages for you. First, a really big snow storm has struck the North Pole, piling up snow all around Santa's castle and even blocking the doors. To continue their holiday prep, the elves have burrowed into the snow uncovering many fascinating things below the surface. Second, Santa's Five Golden Rings are missing! These Rings have magical powers vital to Santa's holiday operation. We absolutely need your help in finding the Rings, so get ready to embark on five epic quests. Remember to click on the badge in the center of your avatar to track your progress.

And, one last thing -- As you engage with our North Pole team and other players, remember to always treat them with kindness and respect following the Holiday Hack Challenge [Code of Conduct and Terms of Use](https://2022.kringlecon.com/invite?modal=tos).

Once you've read that code and agree to it, feel free to sign in.

Happy Holidays from the entire SANS Holiday Hack Challenge team!

<https://2022.kringlecon.com/invite>

<!--cut-->

* TOC
{:toc}

# (&#x2713;) KringleCon Orientation Objectives list

[![](/assets/images/sans/2022/074b39e2.png)](/assets/images/sans/2022/074b39e2.png)

[![](/assets/images/sans/2022/864c48f0.png)](/assets/images/sans/2022/864c48f0.png)

[![](/assets/images/sans/2022/16419233.png)](/assets/images/sans/2022/16419233.png)

## (&#x2713;) 1) Talk to Jingle Ringford

## (&#x2713;) 2) Get your badge

## (&#x2713;) 3) Create a wallet

[![](/assets/images/sans/2022/0e0b4d2c.png)](/assets/images/sans/2022/0e0b4d2c.png)

[![](/assets/images/sans/2022/f629327d.png)](/assets/images/sans/2022/f629327d.png)

[![](/assets/images/sans/2022/319b11f7.png)](/assets/images/sans/2022/319b11f7.png)

[![](/assets/images/sans/2022/ddb43f06.png)](/assets/images/sans/2022/ddb43f06.png)

```
WalletAddress: 0xbbCD3F40D2A7E430b4d23b975Ac4B4B987Cc352e
Key: 0xee7d8bcb8b5238023749792d17da4e0b9ed69dc9202b32e51962c58e1b54f276
```

## (&#x2713;) 4) Use the terminal

[![](/assets/images/sans/2022/3fb0e5b5.png)](/assets/images/sans/2022/3fb0e5b5.png)

[![](/assets/images/sans/2022/ac973f16.png)](/assets/images/sans/2022/ac973f16.png)

## (&#x2713;) 5) Talk to Santa

[![](/assets/images/sans/2022/8b20b257.png)](/assets/images/sans/2022/8b20b257.png)

[![](/assets/images/sans/2022/828f24a2.png)](/assets/images/sans/2022/828f24a2.png)

# Hall of talks (CHEST)

[![](/assets/images/sans/2022/6489417a.png)](/assets/images/sans/2022/6489417a.png)

# (&#x2713;) Recover the Tolkien Ring Objectives list

[![](/assets/images/sans/2022/2641bfe9.png)](/assets/images/sans/2022/2641bfe9.png)

## (&#x2713;) 1) Wireshark Practice

[![](/assets/images/sans/2022/0db739ef.png)](/assets/images/sans/2022/0db739ef.png)

### (&#x2713;) 1. There are objects in the PCAP file that can be exported by Wireshark and/or Tshark. What type of objects can be exported from this PCAP?

[![](/assets/images/sans/2022/267795e8.png)](/assets/images/sans/2022/267795e8.png)

TEXT TO USE: 
```
HTTP
```

[![](/assets/images/sans/2022/d617615b.png)](/assets/images/sans/2022/d617615b.png)

[![](/assets/images/sans/2022/fa34edd9.png)](/assets/images/sans/2022/fa34edd9.png)

### (&#x2713;) 2. What is the file name of the largest file we can export?

[![](/assets/images/sans/2022/36df8597.png)](/assets/images/sans/2022/36df8597.png)

TEXT TO USE: 
```
app.php
```

[![](/assets/images/sans/2022/7b61aa41.png)](/assets/images/sans/2022/7b61aa41.png)

### (&#x2713;) 3. What packet number starts that app.php file?

[![](/assets/images/sans/2022/4ba6b5f1.png)](/assets/images/sans/2022/4ba6b5f1.png)

TEXT TO USE: 
```
687
```

[![](/assets/images/sans/2022/c3fd466e.png)](/assets/images/sans/2022/c3fd466e.png)

### (&#x2713;) 4. What is the IP of the Apache server?

[![](/assets/images/sans/2022/24006dbe.png)](/assets/images/sans/2022/24006dbe.png)

TEXT TO USE: 
```
192.185.57.242
```

[![](/assets/images/sans/2022/ce17bc26.png)](/assets/images/sans/2022/ce17bc26.png)

### (&#x2713;) 5. What file is saved to the infected host?

[![](/assets/images/sans/2022/bc3af28c.png)](/assets/images/sans/2022/bc3af28c.png)

TEXT TO USE: 
```
Ref_Sept24-2020.zip
```

[![](/assets/images/sans/2022/fb959370.png)](/assets/images/sans/2022/fb959370.png)

### (&#x2713;) 6. Attackers used bad TLS certificates in this traffic. Which countries were they registered toed to? Submit the names of the countries in alphabetical order separated by a commas (Ex: y, SoNorway, South Korea).

[![](/assets/images/sans/2022/60fe636a.png)](/assets/images/sans/2022/60fe636a.png)

TEXT TO USE: 
```
Israel, South Sudan, United States
```

1. Transport Layer Security -> Handshake Protocol: Certificate -> Certificates -> Certificate: 308204253082030da003020102020900c498012488156a13300d06092a864886f70d0101… (id-at-commonName=heardbellith.Icanwepeh.nagoya,id-at-organizationalUnitName=moasn@emanc,id-at-organizationName=Wemadd Hixchac GmBH,id-at-localityName
2. Transport Layer Security -> Handshake Protocol: Certificate -> Certificates -> Certificate: 308203873082026fa003020102020900f20ef9f324741db2300d06092a864886f70d0101… (id-at-commonName=psprponounst.aquarelle,id-at-organizationName=Hedanpr S.p.a.,id-at-localityName=Khartoum,id-at-countryName=SS)
3. Transport Layer Security -> Handshake Protocol: Certificate -> Certificates -> Certificate: 308203e130820367a003020102021333000000188c1abdc391569b5f000000000018300a… (id-at-commonName=*.prod.do.dsp.mp.microsoft.com,id-at-organizationalUnitName=DSP,id-at-organizationName=Microsoft,id-at-localityName=Redmond,id-at-st

[![](/assets/images/sans/2022/72453b88.png)](/assets/images/sans/2022/72453b88.png)

[Country Codes](https://country-code.cl/)

### (&#x2713;) 7. Was the machine infected (Yes/No)

TEXT TO USE:
```
Yes
```

## (&#x2713;) 2) Windows Event Logs

[![](/assets/images/sans/2022/71081031.png)](/assets/images/sans/2022/71081031.png)

### (&#x2713;) 1. What month/day/year did the attack take place? For example, 09/05/2021.

[![](/assets/images/sans/2022/369cc41e.png)](/assets/images/sans/2022/369cc41e.png)

TEXT TO USE: 
```
12/24/2022
```

[![](/assets/images/sans/2022/d00dcceb.png)](/assets/images/sans/2022/d00dcceb.png)

### (&#x2713;) 2. An attacker got a secret from a file. What was the original file's name?

[![](/assets/images/sans/2022/9a296442.png)](/assets/images/sans/2022/9a296442.png)

TEXT TO USE: 
```
Recipe.txt
```

[![](/assets/images/sans/2022/062d55cf.png)](/assets/images/sans/2022/062d55cf.png)

### (&#x2713;) 3. The contents of the previous file were retrieved, changed, and stored to a variable by the attacker. This was done multiple times. Submit the last full PowerShell line that performed only these actions.

[![](/assets/images/sans/2022/e2731ffc.png)](/assets/images/sans/2022/e2731ffc.png)

TEXT TO USE: 
```
$foo = Get-Content .\Recipe| % {$_ -replace 'honey', 'fish oil'}
```

[![](/assets/images/sans/2022/247a878d.png)](/assets/images/sans/2022/247a878d.png)

### (&#x2713;) 4. After storing the altered file contents into the variable, the attacker used the variable to run a separate command that wrote the modified data to a file. This was done multiple times. Submit the last full PowerShell line that performed only this action.

[![](/assets/images/sans/2022/efe9fab6.png)](/assets/images/sans/2022/efe9fab6.png)

TEXT TO USE: 
```
$foo | Add-Content -Path 'Recipe'
```

[![](/assets/images/sans/2022/7b013f74.png)](/assets/images/sans/2022/7b013f74.png)

### (&#x2713;) 5. The attacker ran the previous command against a file multiple times. What is the name of this file?

TEXT TO USE:
```
Recipe.txt
```

### (&#x2713;) 6. Were any files deleted? (Yes/No)

TEXT TO USE:
```
yes
```

### (&#x2713;) 7. Was the original file (from question 2) deleted? (Yes/No)

TEXT TO USE:
```
no
```

### (&#x2713;) 8. What is the Event ID of the log that shows the actual command line used to delete the file?

TEXT TO USE:
```
4104
```
[![](/assets/images/sans/2022/29ea840d.png)](/assets/images/sans/2022/29ea840d.png)

### (&#x2713;) 9. Is the secret ingredient compromised (Yes/No)?

TEXT TO USE:
```
yes
```

### (&#x2713;) 10. What is the secret ingredient?

TEXT TO USE:
```
honey
```

## (&#x2713;) 3) Suricata Regatta

[![](/assets/images/sans/2022/000d9b51.png)](/assets/images/sans/2022/000d9b51.png)

### (&#x2713;) 1. 

RULE TO ADD:
```bash
alert dns $HOME_NET any -> any any (msg:"Known bad DNS lookup, possible Dridex infection"; dns.query; content:"adv.epostoday.uk"; nocase; sid:2025219; rev:4;)
```

### (&#x2713;) 2.

[![](/assets/images/sans/2022/c453ef3a.png)](/assets/images/sans/2022/c453ef3a.png)

RULE TO ADD:
```bash
alert http [192.185.57.242/32] any -> $HOME_NET any (msg:"Investigate suspicious connections, possible Dridex infection"; sid:2025220;)
alert http $HOME_NET any -> [192.185.57.242/32] any (msg:"Investigate suspicious connections, possible Dridex infection"; sid:2025221;)
```

### (&#x2713;) 3.

[![](/assets/images/sans/2022/595ba1bf.png)](/assets/images/sans/2022/595ba1bf.png)

RULE TO ADD:
```
alert tls any any -> any any (msg:"Investigate bad certificates, possible Dridex infection";tls.subject:"CN=heardbellith.Icanwepeh.nagoya"; sid:8; rev:1;)
```

### (&#x2713;) 4.

[![](/assets/images/sans/2022/8b8e88c7.png)](/assets/images/sans/2022/8b8e88c7.png)

RULE TO ADD:
```
alert http any any -> any any (file_data; content:"let byteCharacters = atob"; msg:"Suspicious JavaScript function, possible Dridex infection"; sid:5;)
```

# Recover the Elfen Ring Objectives list

[![](/assets/images/sans/2022/74cfb29d.png)](/assets/images/sans/2022/74cfb29d.png)

## 1) Clone with a Difference

[![](/assets/images/sans/2022/ed826479.png)](/assets/images/sans/2022/ed826479.png)

[![](/assets/images/sans/2022/62b0ba84.png)](/assets/images/sans/2022/62b0ba84.png)

## 2) Prison Escape

[https://learn.snyk.io/lessons/container-runs-in-privileged-mode/kubernetes/](https://learn.snyk.io/lessons/container-runs-in-privileged-mode/kubernetes/)

[![](/assets/images/sans/2022/7a110946.png)](/assets/images/sans/2022/7a110946.png)

[![](/assets/images/sans/2022/f82f9d80.png)](/assets/images/sans/2022/f82f9d80.png)

```bash
mount /dev/vda /mnt
cat /mnt/home/jailer/.ssh/jail.key.priv
082bb339ec19de4935867
```

[![](/assets/images/sans/2022/cf1a0e30.png)](/assets/images/sans/2022/cf1a0e30.png)


## 3) Jolly CI/CD

[![](/assets/images/sans/2022/81e22718.png)](/assets/images/sans/2022/81e22718.png)

[![](/assets/images/sans/2022/aaed7a41.png)](/assets/images/sans/2022/aaed7a41.png)


# Recover the Web Ring Objectives list

[![](/assets/images/sans/2022/3d3ab571.png)](/assets/images/sans/2022/3d3ab571.png)

[![](/assets/images/sans/2022/a819888b.png)](/assets/images/sans/2022/a819888b.png)


# Recover the Cloud Ring Objectives list

[![](/assets/images/sans/2022/96956847.png)](/assets/images/sans/2022/96956847.png)


# Recover the Burning Ring of Fire Objectives list

[![](/assets/images/sans/2022/10ca04ff.png)](/assets/images/sans/2022/10ca04ff.png)


