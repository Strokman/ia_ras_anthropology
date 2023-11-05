class Pagination:

    def __init__(self, models: list, per_page: int = 20):
        self.models = models
        self.per_page = per_page
        self.pages_count = len(models) // per_page + 1

    def paginate(self):
        rv = {}

        page = 1
        start = 0
        stop = self.per_page
        if len(self.models) <= self.per_page:
            rv[page] = enumerate(self.models, start + 1)
            return rv

        for _ in range(0, self.pages_count):
            rv[page] = enumerate(self.models[start:stop], start + 1)
            start = stop
            stop += self.per_page
            page += 1
        return rv
