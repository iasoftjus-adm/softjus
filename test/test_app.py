# Unit tests
import unittest
import tempfile
import os

from src.models import Processo
from app.api.api_client import APIClient, LocalStorage
from data.fake_data import generate_fake_process, get_sample_process


class TestModels(unittest.TestCase):
    def test_processo_creation(self):
        """Test Processo model creation"""
        data = {
            'numeroProcesso': '00008323520184013202',
            'classe': {'codigo': 436, 'nome': 'Test Class'},
            'orgaoJulgador': {'codigo': 1, 'nome': 'Test Court'},
            'dataAjuizamento': '20200101000000',
            'movimentos': [{'dataHora': '2024-01-01T00:00:00Z', 'nome': 'Test'}]
        }

        processo = Processo.from_api_data(data)

        self.assertEqual(processo.numero, '00008323520184013202')
        self.assertEqual(processo.classe['nome'], 'Test Class')
        self.assertEqual(processo.orgao_julgador['nome'], 'Test Court')
        self.assertEqual(len(processo.movimentos), 1)

    def test_processo_to_dict(self):
        """Test Processo serialization to dict"""
        processo = Processo(
            numero='123',
            classe={'codigo': 1, 'nome': 'Test'},
            orgao_julgador={'codigo': 1, 'nome': 'Court'},
            data_ajuizamento='20200101',
            movimentos=[],
            assunto='Test Subject'
        )

        data = processo.to_dict()
        self.assertEqual(data['numero'], '123')
        self.assertEqual(data['classe']['nome'], 'Test')


class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = LocalStorage(self.temp_file.name)

    def tearDown(self):
        # Clean up temporary file
        os.unlink(self.temp_file.name)

    def test_save_and_load_favorites(self):
        """Test saving and loading favorites"""
        favorites = [
            {'processo': '123', 'classe': 'Test', 'data_adicao': '2024-01-01'},
            {'processo': '456', 'classe': 'Test2', 'data_adicao': '2024-01-02'}
        ]

        # Save favorites
        self.storage.save_favorites(favorites)

        # Load favorites
        loaded = self.storage.load_favorites()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]['processo'], '123')
        self.assertEqual(loaded[1]['processo'], '456')

    def test_load_empty_file(self):
        """Test loading from non-existent file"""
        # Create new storage with non-existent file
        storage = LocalStorage('/non/existent/path.json')
        favorites = storage.load_favorites()

        self.assertEqual(favorites, [])


class TestFakeData(unittest.TestCase):
    def test_generate_fake_process(self):
        """Test fake process generation"""
        processo = generate_fake_process()

        self.assertIsInstance(processo, Processo)
        self.assertIsNotNone(processo.numero)
        self.assertIsInstance(processo.classe, dict)
        self.assertIsInstance(processo.orgao_julgador, dict)
        self.assertIsInstance(processo.movimentos, list)

    def test_get_sample_process(self):
        """Test getting sample process data"""
        processos = get_sample_process('00008323520184013202')

        self.assertGreater(len(processos), 0)
        self.assertEqual(processos[0].numero, '00008323520184013202')


class TestAPIClient(unittest.TestCase):
    def test_validate_process_number(self):
        """Test process number validation"""
        client = APIClient()

        # Valid numbers
        self.assertTrue(client.validate_process_number('00008323520184013202'))
        self.assertTrue(client.validate_process_number('1234567-89.2024.1.01.1234'))

        # Invalid numbers (too short/long)
        self.assertFalse(client.validate_process_number('123'))
        self.assertFalse(client.validate_process_number(''))

    def test_fake_data_mode(self):
        """Test API client with fake data"""
        client = APIClient(use_fake_data=True)

        # Should return fake data without making real API call
        processos = client.search_process('test')

        self.assertIsInstance(processos, list)
        self.assertGreater(len(processos), 0)
        self.assertIsInstance(processos[0], Processo)


if __name__ == '__main__':
    unittest.main()