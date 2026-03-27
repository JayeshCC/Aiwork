from aiwork.api import server


def test_api_main_uses_cli_arguments(monkeypatch):
    called = {}

    def fake_start_server(host="0.0.0.0", port=5000, debug=False, auto_port=False):
        called["host"] = host
        called["port"] = port
        called["debug"] = debug
        called["auto_port"] = auto_port

    monkeypatch.setattr(server, "start_server", fake_start_server)

    server.main(["--host", "127.0.0.1", "--port", "8081", "--debug", "--auto-port"])

    assert called == {
        "host": "127.0.0.1",
        "port": 8081,
        "debug": True,
        "auto_port": True,
    }


def test_build_parser_defaults():
    args = server.build_parser().parse_args([])

    assert args.host == "0.0.0.0"
    assert args.port == 5000
    assert args.debug is False
    assert args.auto_port is False
