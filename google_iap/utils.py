#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################ Copyrights and license ############################
#                                                                              #
# Copyright 2019 Sophian Mehboub <sophian.mehboub@gmail.com>                   #
#                                                                              #
# This file is part of google-iap.                                             #
#                                                                              #
# google-iap is free software: you can redistribute it and/or modify it under  #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# google-iap is distributed in the hope that it will be useful, but WITHOUT ANY#
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with google-iap. If not, see <http://www.gnu.org/licenses/>.           #
#                                                                              #
################################################################################

import sys
def signal_handler(sig, frame):
    sys.exit(0)

class GCPEXCEPTION(Exception): pass

