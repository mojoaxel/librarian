=========
librarian
=========

Librarian is an archive manager for Outernet Receiver. 

It reads the content of a directory where the content has been downloaded from 
the satellite receiver, and allows the user to sort, remove, and accept new
content into the Outernet Receiver's content archive. It also provides an
interface for browsing the archive. Finally, it provides mechanisms for
self-updating.

The current version does not provide any search capability. That feature is
planned for future releases.

We chose to use Arch Linux as development.

Development environment and running Librarian
=============================================

Please see the documentation in ``docs/dev_env.rst``.

Android port
============

The Android port is based on Kivy_. The code includes a buildozer spec file,
and a wrapper script called ``main.py``. Please refer to Kivy documentation for
more information on how to set the development environment up.

Before compiling the app, you must bundle dependencies. You can do this by
running the following command in the source directory::

    pip install -r conf/requirements.txt -t vendor

Note that you cannot run this command multiple times. You must first remove the
``vendor`` directory completely after modifying requirements file and
reinstalling dependencies.

Android port is still being worked on, so don't expect it to work just yet.

Contributing interface translations
===================================

You can either translate using the .po files in the project directory, or use
the hosted version `on POEditor`_ (recommended). Note that Librarian is
currently under active development, so strings *will* change from time to time.

If you are contributing, or considering contributing translations, please swing
by our forums_ and say hello.

Testing translations
--------------------

Please see the documentation in ``docs/translations.rst`` for more information.

List of translation contributors
--------------------------------

Special thanks to all those who have contributed their valuable time and
knowledge:

- Lars Lillo Ulvestad 
- cavit 
- Susruthan Seran 
- Mogens From 
- David Marques 
- Chengtao Hua 
- necklinux 
- patrik 
- Josep Manel 
- Arthur 
- Ismail Al Ahmad 
- Romaric FAVE 
- Peer Oliver Schmidt 
- Sakara 
- Luis Fuentes 
- Dana Tierney 
- Ahmed 
- Navina 
- Baris Kilic 
- Buddha Burman 
- Christoph Nebendahl 


Reporting bugs and feature requests
===================================

Bugs and feature requests can be posted either in our forums_ or in the GitHub
`issue tracker`_.

.. _Vagrant: http://www.vagrantup.com/
.. _custom Vagrant base box: https://github.com/Outernet-Project/archlinux-vagrant
.. _VritualBox: https://www.virtualbox.org/
.. _port 8080: http://localhost:8080/
.. _on POEditor: https://poeditor.com/join/project?hash=90911b6fc31f2d68c7debd999aa078c6
.. _forums: https://discuss.outernet.is/
.. _issue tracker: https://github.com/Outernet-Project/librarian/issues
.. _Python download page: https://www.python.org/downloads/
.. _Kivy: http://kivy.org/#home
