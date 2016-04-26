import mock
import report
import unittest
import wrapper

class TestReport(unittest.TestCase):

    @mock.patch('wrapper.Wrapper.authenticate_client', return_value='token1')
    def test_create_api_connection(self, authenticate_client_function):
        rep = report.Report()
        response = rep.create_api_connection()
        assert response == 'token1'

    @mock.patch('wrapper.Wrapper.get_server_groups', return_value=({"groups":[{"id":"1234","name":"name1"},{"id":"2345","name":"name2"}]}, False))
    def test_get_server_groups(self, get_server_groups_function):
        rep = report.Report()
        server_groups = rep.get_server_groups()
        server_group = server_groups[0]
        assert len(server_groups) == 2
        assert server_group['name'] == 'name1'

    @mock.patch('wrapper.Wrapper.get_servers_by_group', return_value=({"servers":[{"hostname":"test","id":"1234"},{"hostname":"test2","id":"2345"}]}, False))
    def test_get_servers_by_group(self, get_servers_by_group_function):
        rep = report.Report()
        servers = rep.get_servers_by_group('1234')
        server = servers[0]
        assert len(servers) == 2
        assert server['hostname'] == 'test'

    @mock.patch('wrapper.Wrapper.get_svm_results_by_server', return_value=({"scan":{"findings":[{"package_name":"test1","package_version":"1.0","critical":True,"cve_entries":[{"cve_entry":"CVE_1"},{"cve_entry":"CVE_2"}]}]}}, False))
    def test_get_svm_results_by_server(self, get_svm_results_by_server_function):
        rep = report.Report()
        results = rep.get_svm_results_by_server('1234')
        result = results[0]
        cve_entries = result['cve_entries']
        assert len(results) == 1
        assert result['package_name'] == 'test1'
        assert result['package_version'] == '1.0'
        assert result['critical'] == True
        assert len(cve_entries) == 2

if __name__ == '__main__':
    unittest.main()
