import importlib.util
import os


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_quickstart_functions():
    module = load_module(os.path.join("examples", "quickstart.py"), "quickstart_example")
    extract_out = module.extract({})
    assert "text" in extract_out
    summary_out = module.summarize({"outputs": {"extract": {"text": "hello world"}}})
    assert "summary" in summary_out


def test_airflow_export_demo_main(tmp_path, monkeypatch):
    module = load_module(os.path.join("examples", "airflow_export_demo.py"), "airflow_export_demo")
    monkeypatch.chdir(tmp_path)
    module.main()


def test_memory_demo_main():
    module = load_module(os.path.join("examples", "memory_demo.py"), "memory_demo")
    module.main()


def test_customer_support_logic():
    module = load_module(
        os.path.join("examples", "agents", "customer_support", "run.py"),
        "customer_support_demo",
    )
    intent = module.understand_intent({"query": "I want a refund"})
    assert intent["intent"] == "refund_request"

    search = module.search_knowledge_base({"outputs": {"intent": intent}})
    response = module.generate_response({"outputs": {"search": search}})
    assert "response" in response


def test_document_processor_logic():
    module = load_module(
        os.path.join("examples", "agents", "document_processor", "run.py"),
        "document_processor_demo",
    )
    ocr_out = module.ocr_extract({"input_path": "invoice.pdf"})
    assert "raw_text" in ocr_out
    assert module.amount_guardrail.validate(ocr_out) is True

    analysis = module.analyze_finance({"outputs": {"ocr_task": ocr_out}})
    assert "analysis" in analysis
    assert "next_tasks" in analysis
