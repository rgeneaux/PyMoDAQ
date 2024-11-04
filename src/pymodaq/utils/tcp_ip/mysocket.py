# -*- coding: utf-8 -*-
"""
Created the 26/10/2023

@author: Sebastien Weber
"""
from pymodaq_utils.mysocket import Socket
from pymodaq.utils.tcp_ip.serializer import Serializer
from pymodaq_data.serializer import SERIALIZABLE


class Socket(Socket):
    """Custom Socket wrapping the built-in one and added functionalities to
    make sure message have been sent and received entirely"""

    def check_sended_with_serializer(self, obj: SERIALIZABLE):
        """ Convenience function to convert permitted objects to bytes and then use the check_sended method

        For a list of allowed objects, see :meth:`Serializer.to_bytes`
        """
        self.check_sended(Serializer(obj).to_bytes())
