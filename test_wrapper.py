import unittest

from httmock import with_httmock

import wrapper
import mocks.wrapper

class TestWrapper(unittest.TestCase):

    @with_httmock(mocks.wrapper.resource_get)
    def test_get_server_groups(self):
        connection = wrapper.Wrapper()
        connection.auth_token = '1234'
        server_groups, err = connection.get_server_groups()

        self.assertNotEqual(server_groups, None)
        self.assertEqual(err, False)
        self.assertEqual(server_groups['count'], 3)

    @with_httmock(mocks.wrapper.resource_get)
    def test_get_servers_by_group(self):
        connection = wrapper.Wrapper()
        connection.auth_token = '1234'
        group_id = '8cb73'
        servers, err = connection.get_servers_by_group(group_id)

        self.assertNotEqual(servers, None)
        self.assertEqual(err, False)
        self.assertEqual(servers['count'], 1)

    @with_httmock(mocks.wrapper.resource_get)
    def test_get_servers_by_nonexistant_group(self):
        connection = wrapper.Wrapper()
        connection.auth_token = '1234'
        group_id = '1234'
        servers, err = connection.get_servers_by_group(group_id)

        self.assertEqual(servers, {})
        self.assertEqual(err, False)

    @with_httmock(mocks.wrapper.resource_get)
    def test_get_svm_results_by_server(self):
        connection = wrapper.Wrapper()
        connection.auth_token = '1234'
        server_id = '29bc5'
        results, err = connection.get_svm_results_by_server(server_id)

        self.assertNotEqual(results, None)
        self.assertEqual(err, False)
        self.assertEqual(results['id'], server_id)

    @with_httmock(mocks.wrapper.resource_get)
    def test_get_svm_results_by_nonexistant_server(self):
        connection = wrapper.Wrapper()
        connection.auth_token = '1234'
        server_id = '1234'
        results, err = connection.get_svm_results_by_server(server_id)

        self.assertEqual(results, {})
        self.assertEqual(err, False)

if __name__ == '__main__':
    unittest.main()
