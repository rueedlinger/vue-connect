class MockResp:
    def __init__(self, data=[], status_code=200):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data