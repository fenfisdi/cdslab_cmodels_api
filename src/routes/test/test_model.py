from unittest import TestCase
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from uuid import uuid1


def solve_path(path: str):
    source = 'src.routes.model'
    return ".".join([source, path])

class CreateModelTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/model'
        self.valid_data = {
            "name":"test",
            "state_variables":[{
                "label" : "unittest",
                "representation":"test",
                "unit":"unittest",
                "can_fit":"True"
            }],
            "parameters":[{
                "label":"unittest",
                "representation":"test",
                "unit":"unittest",
                "min_value":"0.0",
                "max_value":"5.0"
            }]
        }
        
    @patch(solve_path("ModelInterface"))
    def test_create_model_exist(self, model_interface: Mock):
        model_interface.find_one_by_name.return_value = Mock()

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

class FindModelTestCase(TestCase):
    
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.model_id = uuid1()
        self.route = f'/model/{self.model_id.hex}'

    @patch(solve_path("ModelInterface"))
    def test_create_model(self, model_interface: Mock):
        model_interface.find_one_by_uuid.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route, params=dict(uuid=self.model_id))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

class FindModelTestCase(TestCase):
    
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.model_id = uuid1()
        self.route = f'/model/{self.model_id.hex}'

        self.valid_data = {
            "name":"test",
            "state_variables":[{
                "label" : "unittest",
                "representation":"test",
                "unit":"unittest",
                "can_fit":"True"
            }],
            "parameters":[{
                "label":"unittest",
                "representation":"test",
                "unit":"unittest",
                "min_value":"0.0",
                "max_value":"5.0"
            }]
        }

    @patch(solve_path("ModelInterface"))
    def test_update_model(self, model_interface: Mock):
        model_interface.find_one_by_uuid.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.put(
            self.route, 
            params=self.model_id.hex, 
            json=self.valid_data
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

class TestListModelTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/model'

    @patch(solve_path("ModelInterface"))
    def test_list_model(self,model_interface: Mock):
        model_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        