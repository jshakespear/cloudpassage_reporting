#!/usr/bin/env python

import os
import wrapper

class Report:
    CLIENT_KEY = os.environ.get('HALO_CLIENT_KEY')
    CLIENT_SECRET = os.environ.get('HALO_CLIENT_SECRET')

    api_connection = None

    # Authenticate with CP API and set api_conneciton for use by other API calls
    def create_api_connection(self):
        global api_connection
        api_connection = wrapper.Wrapper()
        api_connection.client_key = self.CLIENT_KEY
        api_connection.client_secret = self.CLIENT_SECRET
        response = api_connection.authenticate_client()
        return response

    # Get Server Groups from API wrapper and return only data needed for reporting
    def get_server_groups(self):
        server_groups = []
        server_groups_obj, err = api_connection.get_server_groups()
        groups = server_groups_obj['groups']
        for group in groups:
            server_group = {}
            server_group['id'] = group['id']
            server_group['name'] = group['name']
            server_groups.append(server_group)
        return server_groups

    # Get Servers associated with ServerGroup from API wrapper and return only data needed for reporting
    def get_servers_by_group(self, group_id):
        servers = []
        servers_obj, err = api_connection.get_servers_by_group(group_id)
        servers_list = servers_obj['servers']
        for server_obj in servers_list:
            server = {}
            server['hostname'] = server_obj['hostname']
            server['id'] = server_obj['id']
            servers.append(server)
        return servers

    # Get SVM Scan Results associated with Server from API wrapper and return only data needed for reporting
    def get_svm_results_by_server(self, server_id):
        svm_results = []
        svm_results_obj, err = api_connection.get_svm_results_by_server(server_id)
        svm_results_list = svm_results_obj['scan']['findings']
        for svm_result_obj in svm_results_list:
            svm_result = {}
            svm_result['package_name'] = svm_result_obj['package_name']
            svm_result['package_version'] = svm_result_obj['package_version']
            svm_result['critical'] = svm_result_obj['critical']
            svm_result['cve_entries'] = svm_result_obj['cve_entries']
            svm_results.append(svm_result)
        return svm_results

    # Print scan results in a human-readable tree format
    def print_results(self, server_groups):
        print 'SVM Scan Results:'
        print "\tServer Group:"
        for server_group in server_groups:
            print "\t\t" + server_group['name'] + ' (' + server_group['id'] + ')'
            servers = server_group['servers']
            print "\t\tServers:"
            if len(servers) > 0:
                for server in servers:
                    print "\t\t\tHostname: " + server['hostname']
                    svm_results = server['svm_results']
                    print "\t\t\tPackages:"
                    for svm_result in svm_results:
                        print "\t\t\t\tName: " + svm_result['package_name']
                        print "\t\t\t\tVersion: " + svm_result['package_version']
                        print "\t\t\t\tCritical?: " + str(svm_result['critical'])
                        cve_entries = svm_result['cve_entries']
                        if len(cve_entries) > 0:
                            print "\t\t\t\tCVE Entries:"
                            for cve_entry in cve_entries:
                                print "\t\t\t\t\t" + cve_entry['cve_entry']
                        print ''
            else:
                print "\t\t\tNone"

    # Entry point for the application which generates and prints report
    def run(self):
        server_groups = self.get_server_groups()
        for server_group in server_groups:
            server_group['servers'] = self.get_servers_by_group(server_group['id'])
            for server in server_group['servers']:
                server['svm_results'] = self.get_svm_results_by_server(server['id'])

        self.print_results(server_groups)
