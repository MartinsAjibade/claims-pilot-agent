from unittest.mock import MagicMock, patch


def test_chat_completion_returns_assistant_text():
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message = MagicMock()
    mock_resp.choices[0].message.content = "ok"

    with patch("claim_pilot_ai.llm.litellm_client.litellm.completion", return_value=mock_resp) as m:
        from claim_pilot_ai.llm.litellm_client import chat_completion

        out = chat_completion([{"role": "user", "content": "hi"}], max_tokens=10)
    assert out == "ok"
    m.assert_called_once()
    call_kw = m.call_args.kwargs
    assert call_kw["messages"][0]["content"] == "hi"
    assert call_kw["max_tokens"] == 10
