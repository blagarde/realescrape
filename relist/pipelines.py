from realescrape.management.commands.importjson import import_items


class DjangoPipeline(object):

    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items += [item]
        return item

    def close_spider(self, spider):
        import_items(self.items)
