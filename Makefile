.PHONY: run-ios run-macos

run-ios:
	buildozer ios debug deploy run

run-macos:
	python3 app/main.py
