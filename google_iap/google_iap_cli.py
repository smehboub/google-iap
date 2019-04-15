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

from .gcpiap import GcpIap
from docopt import docopt
from signal import signal, SIGINT
from .utils import signal_handler
signal(SIGINT, signal_handler)
import sys

def google_iap_cli(name):
    usage = """
    Usage:
      {0} projects list [--credentials=<s>]
      {0} zones list [--credentials=<s>] --project=<p>
      {0} instances list [--credentials=<s>] --project=<p> [--zone=<z>]
      {0} iap get [--credentials=<s>] --project=<p> [--zone=<z>] [--instance=<i>] [--format=<f>]
      {0} iap set [--credentials=<s>] --project=<p> [--zone=<z>] [--instance=<i>] --policy=<p>
      {0} --version
    
    Options:
      -h --help          Show this screen.
      --credentials=<s>  Service account json file
      --project=<p>      Project Id
      --zone=<z>         Zone name
      --instance=<i>     Instance name
      --policy=<p>       Policy json file or yaml file
      --format=<f>       Format (valid format : yaml or json) [default: yaml]
      --version          Version
    """.format(name)
    
    arguments = docopt(usage, version='1.0.7')
    
    if 'projects' in arguments:
        if arguments['projects'] == 1:
            if 'list' in arguments:
                if arguments['list']:
                    try:
                        gcpiap = GcpIap(arguments['--credentials'])
                        for project in gcpiap.listProjects():
                            print(project)
                        sys.exit(0)
                    except Exception as e:
                        print(str(e))
                        sys.exit(1)
    
    if 'zones' in arguments:
        if arguments['zones'] == 1:
            if 'list' in arguments:
                if arguments['list']:
                    try:
                        gcpiap = GcpIap(arguments['--credentials'])
                        for zone in gcpiap.listZonesUsed(arguments['--project']):
                            print(zone)
                        sys.exit(0)
                    except Exception as e:
                        print(str(e))
                        sys.exit(1)
    
    if 'instances' in arguments:
        if arguments['instances'] == 1:
            if 'list' in arguments:
                if arguments['list']:
                    try:
                        gcpiap = GcpIap(arguments['--credentials'])
                        if not arguments['--zone'] and arguments['--project']:
                            for instance in gcpiap.listInstances(arguments['--project']):
                                print(instance)
                        elif arguments['--zone'] and arguments['--project']:
                            for instance in gcpiap.listInstancesByZone(arguments['--project'], zone=arguments['--zone']):
                                print(instance)
                        sys.exit(0)
                    except Exception as e:
                        print(str(e))
                        sys.exit(1)
    
    if 'iap' in arguments:
        if arguments['iap'] == 1:
            if 'get' in arguments:
                if arguments['get']:
                    try:
                        gcpiap = GcpIap(arguments['--credentials'])
                        if not arguments['--instance'] and not arguments['--zone'] and arguments['--project']:
                            print(gcpiap.getIapPolicy(arguments['--project'], format=arguments['--format']))
                        elif not arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                            print(gcpiap.getIapPolicy(arguments['--project'], zone=arguments['--zone'], format=arguments['--format']))
                        elif arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                            print(gcpiap.getIapPolicy(arguments['--project'], zone=arguments['--zone'], instance=arguments['--instance'], format=arguments['--format']))
                        sys.exit(0)
                    except Exception as e:
                        print(str(e))
                        sys.exit(1)
    
    if 'iap' in arguments:
        if arguments['iap'] == 1:
            if 'set' in arguments:
                if arguments['set']:
                    try:
                        gcpiap = GcpIap(arguments['--credentials'])
                        if not arguments['--instance'] and not arguments['--zone'] and arguments['--project']:
                            print(gcpiap.setIapPolicy(arguments['--project'], arguments['--policy']))
                        elif not arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                            print(gcpiap.setIapPolicy(arguments['--project'], arguments['--policy'], zone=arguments['--zone']))
                        elif arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                            print(gcpiap.setIapPolicy(arguments['--project'], arguments['--policy'], zone=arguments['--zone'], instance=arguments['--instance']))
                        sys.exit(0)
                    except Exception as e:
                        print(str(e))
                        sys.exit(1)
    
    
