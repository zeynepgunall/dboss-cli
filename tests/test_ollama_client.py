import pytest
import requests

from dboss.ollama_client import OllamaError, generate, strip_code_fences


# --- strip_code_fences ---

@pytest.mark.parametrize("text,expected", [
    ("```plaintext\nfeat: add login\n```", "feat: add login"),
    ("```bash\nchore: update deps\n```", "chore: update deps"),
    ("```\nfix: null pointer\n```", "fix: null pointer"),
    ("feat: plain text", "feat: plain text"),
    ("  feat: trim spaces  ", "feat: trim spaces"),
])
def test_strip_code_fences(text, expected):
    assert strip_code_fences(text) == expected


# --- generate ---

def test_generate_success(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = True
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"response": "feat: add login"}
    mocker.patch("dboss.ollama_client.requests.post", return_value=mock_resp)

    assert generate("some prompt") == "feat: add login"


def test_generate_connection_error(mocker):
    mocker.patch(
        "dboss.ollama_client.requests.post",
        side_effect=requests.exceptions.ConnectionError,
    )
    with pytest.raises(OllamaError, match="bağlanılamadı"):
        generate("some prompt")


def test_generate_404_raises_ollama_error(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = False
    mock_resp.status_code = 404
    mocker.patch("dboss.ollama_client.requests.post", return_value=mock_resp)

    with pytest.raises(OllamaError, match="Model bulunamadı"):
        generate("some prompt")


def test_generate_http_error(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = False
    mock_resp.status_code = 500
    mock_resp.text = "internal server error"
    mocker.patch("dboss.ollama_client.requests.post", return_value=mock_resp)

    with pytest.raises(OllamaError, match="HTTP 500"):
        generate("some prompt")
