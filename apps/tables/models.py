from apps import db
import enum


class ModelChoices(enum.Enum):
    SALES = 'SALES'

    def __str__(self):
        return str(self.value)


class PageItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Enum(ModelChoices), nullable=False)
    items_per_page = db.Column(db.Integer, default=25)

    @classmethod
    def find_by_parent(cls, parent):
        return cls.query.filter_by(parent=parent).first()
    
    @classmethod
    def find_last_by_parent(cls, parent):
        return cls.query.filter_by(parent=parent).order_by(cls.id.desc()).first()

class HideShowFilter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Enum(ModelChoices), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_key_and_parent(cls, key, parent):
        return cls.query.filter_by(key=key, parent=parent).first()

class ModelFilter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Enum(ModelChoices), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_by_key_and_parent(cls, key, parent):
        return cls.query.filter_by(key=key, parent=parent).first()    
    
    @classmethod
    def find_by_parent(cls, parent):
        return cls.query.filter_by(parent=parent) 
    
    @classmethod
    def find_by_id_and_parent(cls, _id, parent):
        return cls.query.filter_by(id=_id, parent=parent).first()
