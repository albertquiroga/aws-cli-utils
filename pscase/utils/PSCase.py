class PSCase:
    def __init__(self, number, date, case_id, title, topic, description="", notes=""):
        self.number = number
        self.date = date
        self.title = title
        self.topic = topic
        self.case_id = case_id
        self.description = description
        self.notes = notes

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(number=dictionary['number'], date=dictionary['date'], case_id=dictionary['case_id'], title=dictionary['title'],
                   topic=dictionary['topic'], description=dictionary['description'], notes=dictionary['notes'])

    @classmethod
    def from_namespace(cls, namespace):
        return cls(number=namespace.number, date=namespace.date, case_id=namespace.case_id, title=namespace.title,
                   topic=namespace.topic, description=namespace.description, notes=namespace.notes)

    def to_ddb_item(self):
        item = {"number": {"N": self.number},
                "case_id": {"N": self.case_id},
                "date": {"S": self.date},
                "title": {"S": self.title},
                "topic": {"S": self.topic}}

        # DDB does not accept empty attributes on items, so only add the optional values if they are there
        if self.description:
            item['description'] = {"S": self.description}

        if self.notes:
            item['notes'] = {"S": self.notes}

        return item
