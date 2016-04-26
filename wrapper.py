#!/usr/bin/env python

import base64
import json
import os
import requests
import requests.exceptions
import sys
import urllib
import urllib2

class Wrapper:
    def __init__(self):
        self.api_version = 'v1'
        self.auth_args = {'grant_type': 'client_credentials'}
        self.auth_path = 'oauth/access_token'
        self.auth_token = None
        self.base_url = 'https://api.cloudpassage.com'
        self.client_key = None
        self.client_secret = None

    # Authenticate client using OAuth2 and set access_token if successful
    def authenticate_client(self):
        url = "%s/%s" % (self.base_url, self.auth_path)
        response = self.get_auth_token(url, self.auth_args, self.client_key, self.client_secret)
        if (response):
            authResponseJson = json.loads(response)
            if ('access_token' in authResponseJson):
                self.auth_token = authResponseJson['access_token']
            if ('expires_in' in authResponseJson):
                self.expires = authResponseJson['expires_in']
        return self.auth_token

    # Generic GET method used for all API requests
    def do_get_request(self, url, auth_token):
        headers = {'Authorization': 'Bearer ' + auth_token}
        try:
            response = requests.get(url, headers=headers)
            return (response.text, False)
        except requests.exceptions.Timeout, e:
            print >> sys.stderr, 'Connection Timeout'
        except requests.exceptions.TooManyRedirects, e:
            print >> sys.stderr, 'Too Many Redirects'
        except requests.exceptions.RequestException as e:
            print >> sys.stderr, e

    # Generate initial OAuth2 Auth Header using client key and secret
    def generate_auth_header(self, client_key, client_secret):
        auth_string = client_key + ':' + client_secret
        encoded_string = base64.b64encode(auth_string)
        return {'Authorization': 'Basic ' + encoded_string}

    # Trade initial Basic Auth Header for an Auth Token
    def get_auth_token(self, url, args, key, secret):
        headers = self.generate_auth_header(key, secret)
        try:
            response = requests.post(url, params=args, headers=headers)
            return response.text
        except requests.exceptions.Timeout, e:
            print >> sys.stderr, 'Connection Timeout'
        except requests.exceptions.TooManyRedirects, e:
            print >> sys.stderr, 'Too Many Redirects'
        except requests.exceptions.RequestException as e:
            print >> sys.stderr, e

    # Translate HTTP status codes to human-readable response
    def get_http_status(self, code):
        if (code == 200):
            return 'OK'
        elif (code == 401):
            return 'Unauthorized'
        elif (code == 403):
            return 'Forbidden'
        elif (code == 404):
            return 'Not Found'
        elif (code == 422):
            return 'Validation Failed'
        elif (code == 500):
            return 'Internal Server Error'
        elif (code == 502):
            return 'Gateway Error'
        else:
            return "Unknown code [%d]" % code

    # Get all Server Groups associated with the authenticated user
    def get_server_groups(self):
        url = "%s/%s/groups" % (self.base_url, self.api_version)
        (data, auth_error) = self.do_get_request(url, self.auth_token)
        if (data):
            return (json.loads(data), auth_error)
        else:
            return (None, auth_error)

    # Get all Servers associated with requested group_id
    def get_servers_by_group(self, group_id):
        url = "%s/%s/groups/%s/servers" % (self.base_url, self.api_version, group_id)
        (data, auth_error) = self.do_get_request(url, self.auth_token)
        if (data):
            return (json.loads(data), auth_error)
        else:
            return (None, auth_error)

    # Get all SVM Scan Results associated with a requested server_id
    def get_svm_results_by_server(self, server_id):
        url = "%s/%s/servers/%s/svm" % (self.base_url, self.api_version, server_id)
        (data, auth_error) = self.do_get_request(url, self.auth_token)
        if (data):
            return (json.loads(data), auth_error)
        else:
            return (None, auth_error)
