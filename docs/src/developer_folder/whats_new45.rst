.. _whats_new:

What's new in PyMoDAQ 5
***********************

The main modifications in PyMoDAQ 5 is related to the organization of the packaging.

Three new packages were created to offer features pack independantly :

* `pymodaq_data`_: specific for data management/saving/loading
* `pymodaq_gui`_: specific to create GUI and giving access to the one we know from pymodaq
* `pymodaq_utils`_: the basic things that are used everywhere (ie: logging, configuration management, mathematical tools...)

The main idea behind this change is to increase modularity, reusability and to be able to load just the part of the features we need.

.. figure:: /image/pymomorph4to5.gif

.. _pymodaq_utils:

pymodaq_utils
------------
This package provide a set of utilities (constants, methods and classes) that are used in the
various subpackages of PyMoDAQ (PyMoDAQ itself, but also plugins and data management and user interfaces modules).

Basically, all the common generic class and methods used in every pymodaq packages, like logging.
Figure :numref:`pymodaq_utils_hierarchy` show the layout of this package.

.. _pymodaq_utils_hierarchy:

.. figure:: /image/pymodaq_utils_files.png
  :width: 200

  Layout of the ``utils`` module

It looks a lot like the old utils directory in PyMoDAQ 4 (without the gui and data objects).
They can also be used
in some other programs to use their features. Below is a short description of what they are related to:

* abstract: contains abstract classes (if not stored in another specific module)
* array_manipulation: utility functions to create, manipulate  and extract info from numpy arrays
* config: objects dealing with configuration files (for instance the main config for pymodaq). Can be used elsewhere,
  for instance in instrument plugin
* enums: base class and method to ease the use of enumerated types
* factory: base class to be used when defining a factory pattern
* logger: methods to initialize the logging objects in the various modules
* math_utils: a set of useful mathematical functions
* units: methods for conversion between physical units (especially photon energy in eV, nm, cm, J...)

.. _pymodaq_data:

pymodaq_data
------------
All the changes made in PyMoDAQ 4 about :ref:`data management<data_management>` were moved in this package.

Before the :term:`modules<module>` where stored in different places, mainly ``pymodaq.utils.data``, ``pymodaq.utils.h5modules``
module. You had to install and load the whole PyMoDAQ python :term:`package<package>` if you want to use the Data Objects or acess the hdf5 features.
Now, you can install only ``pymodaq_data`` (which still requires the all the basic function from utils).
Figure :numref:`pymodaq_data_hierarchy` show the layout of this package.

.. _pymodaq_data_hierarchy:

.. figure:: /image/pymodaq_utils_files.png
   :width: 200

   Layout of the ``data`` module

.. _pymodaq_gui:

pymodaq_gui
------------
Set of Qt widgets and graphical components for the PyMoDAQ ecosystem.
The two main categories are : Managers, Plotting

:doc:`Manager</api/api_utility_modules/managers>`

:doc:ref to /api/api_doc/ ou /api/API_Utility_Modules

* QAction
* Paramaters
* Module Managers : DAQ_Moves, DAQ_Viewers...

:doc:`Plotting</api/api_utility_modules/api_plotting/viewers>`

