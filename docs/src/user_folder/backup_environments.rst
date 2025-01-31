  .. _section_backup_environments:

Environment backups
===================

PyMoDAQ keeps track of your virtual environment packages and save pip-compatible backups that you can use to transfert or revert
to a working environment

New environments are kept only if they're differents from the previous saved one. The oldest ones are deleted, according to the 
*limit* value kept in the configuration: it is the maximum number of environment backups to keep. There is actually three parameters
to control backups in the config:

.. code-block:: toml

   	...
	[backup]
	keep_backup = true        # should PyMoDAQ keep backups of environments' installed packages?
	folder = "environments"   # where to keep the backup (relative to local config path)
	limit = 25                # how many to keep (maximum)
	...


When activated, these backups are located in PyMoDAQ's local configuration folder, under the general following path:

``/home/<username>/.pymodaq/<folder value from config>/<environment_name>``



Backup structure
----------------
Backup files are structured in a simple way to be compatible with pip but with a little bit more metadata. They start with two commented lines:

* the first one is the python executable path used to launch PyMoDAQ
* the second one is the python executable version

For example:

.. code-block::

	# executable: /home/mairain/.virtualenvs/pymodaq-dev/bin/python
	# version: 3.12.3 (main, Jan 17 2025, 18:03:48) [GCC 13.3.0]

	PySide6==6.8.1
	PySide6_Addons==6.8.1
	PySide6_Essentials==6.8.1
	...


Also, the filename gives some information about when a backup was created by being named according to the following pattern ``<year><month><day><hour><minute><second>_environment.txt``.

A backup created on January 31rd 2025 at 11:24:05 would be ``20250131112405_environment.txt``

It is recommended not to rename backup files as it may mess up ranking them by date.

Restore or transfert a working environment
------------------------------------------


If PyMoDAQ doesn't start after updating/modifying the packages in your virtual environment, or if you want to transfert a working
environment, you can try using a backup to install. For exemple, using ``mamba``, and an environment backup file using python ``3.12.3``

* First create a new environment using the same python version as the one in your backup file ``mamba create -n pymodaq_newenv python=3.12.3``
* Activate the environment ``mamba activate pymodaq_newenv``
* Install packages from the backup file ``pip install -r 20250131112405_environment.txt``
* ``dashboard`` should open PyMoDAQ dashboard