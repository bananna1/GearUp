from data_layer.app import db


class Gear(db.Model):  
    code = db.Column("code", db.Integer, primary_key=True, nullable=False)
    description = db.Column("description", db.String, nullable=False)
    gender = db.Column("gender", db.CHAR, nullable=False)
    category = db.Column("category", db.String, nullable=False)
    warmth = db.Column("warmth", db.String, nullable=False)
    waterproof = db.Column("waterproof", db.Integer, nullable=False)
    level = db.Column("level", db.String, nullable=False)
    link = db.Column("link", db.String, nullable=False)

    def __repr__(self):
        return f"{self.code}: {self.description}, {self.gender}, {self.category}, {self.warmth}, {self.waterproof}, {self.level}, {self.link}"
    
    def to_json(self):
        return {
            'code': self.code,
            'description': self.description,
            'gender': self.gender,
            'category': self.category,
            'warmth': self.warmth,
            'waterproof': self.waterproof,
            'level': self.level,
            'link': self.link
        }

class Users(db.Model):
    email = db.Column("email", db.String, primary_key=True, nullable=False)
    name = db.Column("name", db.String, nullable=False)
    lastname = db.Column("lastname", db.String, nullable=False)

    def __repr__(self):
        return f"{self.id}: {self.email}, {self.name}, {self.lastname}"
    
    def to_json(self):
        return {
            'email': self.email,
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname
        }

class FavouriteGear(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String, db.ForeignKey("users.email"), nullable=False)
    gearid = db.Column("gearid", db.Integer, db.ForeignKey("gear.code"), nullable=False)

    def __repr__(self):
        return f"{self.email}: {self.gearid}"
    
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'gearid': self.gearid
        }

    __table_args__ = (
        db.UniqueConstraint('email', 'gearid', name='uix_email_gearid'),
    )

