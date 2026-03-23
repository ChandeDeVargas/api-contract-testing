import logging
import sys

class TestLogger:
    def __init__(self):
        self._logger = logging.getLogger("api_contract_tests")
        self._logger.setLevel(logging.DEBUG)
        
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def step(self, msg: str):
        print(f"\n[STEP] {msg}")

    def info(self, msg: str):
        self._logger.info(msg)

    def debug(self, msg: str):
        self._logger.debug(msg)

test_logger = TestLogger()
logger = test_logger
