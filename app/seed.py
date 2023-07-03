from app.models import db

vendor1 = Vendor(name='Insomnia Cookies')
db.session.add(vendor1)

vendor2 = Vendor(name='Cookies Cream')
db.session.add(vendor2)

sweet1 = Sweet(name='Chocolate Chip Cookie')
db.session.add(sweet1)

sweet2 = Sweet(name='Brownie')
db.session.add(sweet2)

vendor_sweet1 = VendorSweet(price=200, vendor=vendor1, sweet=sweet1)
db.session.add(vendor_sweet1)

vendor_sweet2 = VendorSweet(price=300, vendor=vendor1, sweet=sweet2)
db.session.add(vendor_sweet2)

db.session.commit()
