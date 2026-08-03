# hash-identifier Usage Example
```
root@kali:~# hash-identifier
   #########################################################################
   #     __  __             __       ______    _____       #
   #    /\ \ /\ \           /\ \     /\__  _\  /\  _ `\     #
   #    \ \ \_\ \     __      ____ \ \ \___ \/_/\ \/  \ \ \_/\ \    #
   #     \ \  _  \  /'__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
   #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
   #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
   #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.1 #
   #                                 By Zion3R #
   #                            www.Blackploit.com #
   #                               Root@Blackploit.com #
   #########################################################################

   -------------------------------------------------------------------------
 HASH: 098f6bcd4621d373cade4e832627b4f6

Possible Hashs:
[+]  MD5
[+]  Domain Cached Credentials - MD4(MD4(($pass)).(strtolower($username)))

Least Possible Hashs:
[+]  RAdmin v2.x
[+]  NTLM
[+]  MD4
[+]  MD2
[+]  MD5(HMAC)
[+]  MD4(HMAC)
[+]  MD2(HMAC)
[+]  MD5(HMAC(Wordpress))
[+]  Haval-128
[+]  Haval-128(HMAC)
[+]  RipeMD-128
[+]  RipeMD-128(HMAC)
[+]  SNEFRU-128
[+]  SNEFRU-128(HMAC)
[+]  Tiger-128
[+]  Tiger-128(HMAC)
[+]  md5($pass.$salt)
[+]  md5($salt.$pass)
[+]  md5($salt.$pass.$salt)
[+]  md5($salt.$pass.$username)
[+]  md5($salt.md5($pass))
[+]  md5($salt.md5($pass))
[+]  md5($salt.md5($pass.$salt))
[+]  md5($salt.md5($pass.$salt))
[+]  md5($salt.md5($salt.$pass))
[+]  md5($salt.md5(md5($pass).$salt))
[+]  md5($username.0.$pass)
[+]  md5($username.LF.$pass)
[+]  md5($username.md5($pass).$salt)
[+]  md5(md5($pass))
[+]  md5(md5($pass).$salt)
[+]  md5(md5($pass).md5($salt))
[+]  md5(md5($salt).$pass)
[+]  md5(md5($salt).md5($pass))
[+]  md5(md5($username.$pass).$salt)
[+]  md5(md5(md5($pass)))
[+]  md5(md5(md5(md5($pass))))
[+]  md5(md5(md5(md5(md5($pass)))))
[+]  md5(sha1($pass))
[+]  md5(sha1(md5($pass)))
[+]  md5(sha1(md5(sha1($pass))))
[+]  md5(strtoupper(md5($pass)))

   -------------------------------------------------------------------------
Packages and Binaries:
hash-identifier
Tool to identify hash types
Software to identify the different types of hashes used to encrypt data and especially passwords.

Installed size: 49 KB
How to install: sudo apt install hash-identifier

Dependencies:
hash-identifier
root@kali:~# hash-identifier -h
   #########################################################################
   #     __  __                     __           ______    _____           #
   #    /\ \ /\ \                   /\ \         /\__  _\  /\  _ `\         #
   #    \ \ \_\ \     __      ____ \ \ \___     \/_/\ \/  \ \ \_/\ \        #
   #     \ \  _  \  /'__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
   #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
   #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
   #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.2 #
   #                                                             By Zion3R #
   #                                                    www.Blackploit.com #
   #                                                   Root@Blackploit.com #
   #########################################################################
--------------------------------------------------

 Not Found.
--------------------------------------------------
 HASH: 

Learn more with OffSec
Want to learn more about hash-identifier? get access to in-depth training and hands-on labs:

PEN-200: 16.2.3. Password Attacks: Cracking Methodology

PEN-200 course
```
