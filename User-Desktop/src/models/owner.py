class Owner:
    def __init__(self, owner_code, owner_name, owner_phone, note):
        self.owner_code = owner_code
        self.owner_name = owner_name
        self.owner_phone = owner_phone
        self.note = note

    def __repr__(self):
        return f"<Owner(owner_code={self.owner_code}, owner_name={self.owner_name}, owner_phone={self.owner_phone}, note={self.note})>"