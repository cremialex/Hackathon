class PnlEvent:
    def __init__(self, time, amount, client, reason):
        self._time = time
        self._amount = amount
        self._client = client
        self._reason = reason

    def log(self):
        return self._time.strftime('%Y%m%d'), str(self._amount), self._client, self._reason
