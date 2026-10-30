from unittest.mock import patch

from src.network import get_status

@patch("requests.get")
def test_get_status(mock_get):
    mock_get.return_value.status_code = 200
    assert get_status("https://example.com") == 200
