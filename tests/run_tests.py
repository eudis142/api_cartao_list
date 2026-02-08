# run_tests.py
import sys
import os

# Adiciona src ao PATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Executa pytest
import pytest

if __name__ == "__main__":
    sys.exit(pytest.main(["unit/test_cartao_list.py", "-v"]))