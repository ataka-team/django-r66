django-r66
==========

django - route 66 application. WebUI for management of your Debian based Router



About features
==============

Wired interfaces
~~~~~~~~~~~~~~~~

 Not yet documented

Wireless interfaces
~~~~~~~~~~~~~~~~~~~

 Not yet documented

PPP
~~~

 Not yet documented

Samba 
~~~~~

* List SAMBA users::

    pdbedit -L -v

* Add SAMBA user (system user is needed with shell to /bin/false at least)::

    smbpasswd -a root

* Delete user::

    pdbedit -x -u root

* Testing SAMBA resources from a Linux box client::

  smbclient -L //10.121.55.75 -U root
