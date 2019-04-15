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

from .utils import GCPEXCEPTION
import json, yaml
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from oauth2client.client import GoogleCredentials, ApplicationDefaultCredentialsError

class GcpIap:

    pageSize = 1000000000

    def __init__(self, SERVICE_ACCOUNT_FILE=None):
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
        try:
            if SERVICE_ACCOUNT_FILE:
                self.credentials = service_account.Credentials.from_service_account_file(os.path.expanduser(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
            else:
                try:
                    self.credentials = GoogleCredentials.get_application_default()
                except ApplicationDefaultCredentialsError as e:
                    credentials = self.getGCredentials()
                    self.credentials = GoogleCredentials( 
                        credentials['token_response']['access_token'], 
                        credentials['client_id'],
                        credentials['client_secret'], 
                        credentials['refresh_token'], 
                        credentials['token_response']['expires_in'],
                        credentials['token_uri'], 
                        credentials['user_agent'],
                        revoke_uri=credentials['revoke_uri']
                        ).create_scoped(SCOPES)
        except Exception as e:
            raise GCPEXCEPTION(str(e))

    def getGCredentials(self):
        import sqlite3
        config_default_path = '~/.config/gcloud'
        credentials_db = 'credentials.db'
        credentials_query = 'SELECT value FROM credentials'
        try:
            config_path = os.path.expanduser(os.environ['CLOUDSDK_CONFIG'])
        except KeyError:
            config_path = os.path.expanduser(config_default_path)
        try:
            conn = sqlite3.connect(os.path.join(config_path, credentials_db))
            c = conn.cursor()
            c.execute(credentials_query)
            credentials = json.loads(c.fetchone()[0])
            conn.close()
        except Exception:
            raise Exception("The crendentials isn't present, you need login with gcloud or use credentials json file")
        return credentials

        
    def getResource(self, resource, version):
        return build(resource, version, credentials=self.credentials)

    def getProject(self, projectId):
        service = self.getResource('cloudresourcemanager', 'v1')
        try:
            return service.projects().get(projectId=projectId).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listProjects(self):
        l = []
        service = self.getResource('cloudresourcemanager', 'v1')
        try:
            for project in service.projects().list(pageSize=self.pageSize).execute()['projects']:
                l.append(project['projectId'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def getAllInstancesRaw(self, projectId):
        service = self.getResource('compute', 'v1')
        try:
            return service.instances().aggregatedList(project=projectId).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listZonesUsed(self, projectId):
        l = []
        try:
            instances = self.getAllInstancesRaw(projectId)
            for k,v in instances['items'].items():
                if 'instances' in v:
                    l.append(k.replace('zones/',''))
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listInstancesByZone(self, projectId, zone):
        l = []
        service = self.getResource('compute', 'v1')
        try:
            instances = service.instances().list(project=projectId, zone=zone).execute()
            for v in instances['items']:
                l.append(v['name'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listInstances(self, projectId):
        l = []
        try:
            instances = self.getAllInstancesRaw(projectId)
            for k,v in instances['items'].items():
                if 'instances' in v:
                    for instance in v['instances']:
                        l.append(instance['name'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def getIapPolicy(self, project, zone=None ,instance=None, format='yaml'):
        formatSupported = ['json', 'yaml']
        if not format in formatSupported: raise GCPEXCEPTION('The supported format is yaml or json')
        service = self.getResource('iap', 'v1beta1')
        project_num = self.getProject(project)['projectNumber']
        zone = '/zones/%s' % zone if zone else ""
        instance = '/instances/%s' % instance if instance else ""
        try:
            resp = service.v1beta1().getIamPolicy(resource='projects/%s/iap_tunnel%s%s' % (project_num, zone, instance)).execute()
            if format == 'json':
                resp = { "policy" : resp }
                return json.dumps(resp, indent=4, sort_keys=True)
            elif format == 'yaml':
                js = json.loads(json.dumps(resp))
                return yaml.safe_dump({ "policy" : js }, allow_unicode=True,  default_flow_style=False)
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def setIapPolicy(self, project, policyfile, zone=None ,instance=None):
        service = self.getResource('iap', 'v1beta1')
        project_num = self.getProject(project)['projectNumber']
        zone = '/zones/%s' % zone if zone else ""
        instance = '/instances/%s' % instance if instance else ""
        try:
            body = open(os.path.expanduser(policyfile)).read()
        except IOError as e:
            raise GCPEXCEPTION(str(e))
        try:
            body = yaml.safe_load(body)
        except yaml.scanner.ScannerError as e:
            raise GCPEXCEPTION(str(e))

        try:
            resp = service.v1beta1().setIamPolicy(resource='projects/%s/iap_tunnel%s%s' % (project_num, zone, instance), body=body).execute()
            return json.dumps({ "policy" : resp }, indent=4, sort_keys=True)
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

