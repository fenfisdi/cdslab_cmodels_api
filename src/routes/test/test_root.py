from unittest import TestCase
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient



def solve_path(path: str):
    source = 'src.routes.root'
    return ".".join([source, path])

class ListSimulationExpiredTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/simulation/expired'
    
    @patch(solve_path("RootSimulationInterface"))
    def test_list_simulation_expired(self, root_interface: Mock):
        root_interface.find_all_expired.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route, params=dict(to_expire=5))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)

