class Property:
    def __init__(self, realstatecode, ownercode, rstatetcode, yearmake, buildtcode,
                 property_area, unitm_code, property_facade, property_depth,
                 n_of_bedrooms, n_of_bathrooms, property_corner, offer_type_code,
                 province_code, region_code, property_address, photosituation,
                 descriptions):
        self.realstatecode = realstatecode
        self.ownercode = ownercode
        self.rstatetcode = rstatetcode
        self.yearmake = yearmake
        self.buildtcode = buildtcode
        self.property_area = property_area
        self.unitm_code = unitm_code
        self.property_facade = property_facade
        self.property_depth = property_depth
        self.n_of_bedrooms = n_of_bedrooms
        self.n_of_bathrooms = n_of_bathrooms
        self.property_corner = property_corner
        self.offer_type_code = offer_type_code
        self.province_code = province_code
        self.region_code = region_code
        self.property_address = property_address
        self.photosituation = photosituation
        self.descriptions = descriptions

    def __repr__(self):
        return f"<Property {self.realstatecode}: {self.property_address}>"