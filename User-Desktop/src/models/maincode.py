class Maincode:
    def __init__(self, recty, code, name, description):
        self.recty = recty
        self.code = code
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Maincode(recty={self.recty}, code={self.code}, name={self.name})>"

    @staticmethod
    def from_dict(data):
        return Maincode(
            recty=data.get('Recty'),
            code=data.get('Code'),
            name=data.get('Name'),
            description=data.get('Description')
        )