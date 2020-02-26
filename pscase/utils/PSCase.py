class PSCase:
    def __init__(self, number, date, case_id, title, topic, description="", notes=""):
        """
        Class constructor.
        :param number: Case number
        :param date: Case date
        :param case_id: Paragon Case ID
        :param title: Case title
        :param topic: Case topic
        :param description: Case description (manually written by the user)
        :param notes: Case notes (manually written by the user)
        """
        self.number = number
        self.date = date
        self.title = title
        self.topic = topic
        self.case_id = case_id
        self.description = description
        self.notes = notes

    @classmethod
    def from_dictionary(cls, dictionary):
        """
        Creates a PSCase object from a dictionary, this can be used for example to create a case from a DDB response
        :param dictionary: Dictionary containing the case data
        :return: PSCase object
        """
        return cls(number=dictionary['number'], date=dictionary['date'], case_id=dictionary['case_id'],
                   title=dictionary['title'], topic=dictionary['topic'],
                   description=dictionary['description'] if 'description' in dictionary else '',
                   notes=dictionary['notes'] if 'notes' in dictionary else '')

    @classmethod
    def from_namespace(cls, namespace):
        """
        Creates a PSCase object from a namespace one, this can be used for example to create a case from argparse CLI args
        :param namespace: Namespace object containing the case data
        :return: PSCase object
        """
        return cls(number=namespace.number, date=namespace.date, case_id=namespace.case_id, title=namespace.title,
                   topic=namespace.topic, description=namespace.description, notes=namespace.notes)

    def to_ddb_item(self):
        """
        Turns the PSCase object into a dictionary with the right format for DDB
        :return: DDB-formatted dictionary with the case data
        """
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
