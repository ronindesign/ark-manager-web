from apps import db
from sqlalchemy import func
import enum

class StatusChoices(enum.Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    RUNNING = 'RUNNING'

    def __str__(self):
        return str(self.value)


class TaskResult(db.Model):
    __tablename__ = 'TaskResult'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=True)
    periodic_task_name = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum(StatusChoices), default=StatusChoices.PENDING)
    result = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_done = db.Column(db.DateTime, nullable=True)


class CurrencyChoices(enum.Enum):
    USD = 'USD'
    EUR = 'EUR'

    def __str__(self):
        return str(self.value)


class RefundedChoices(enum.Enum):
    YES = 'YES'
    NO = 'NO'

    def __str__(self):
        return str(self.value)
    
class Sales(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(255), nullable=True)
    BuyerName = db.Column(db.String(255), nullable=True)
    PurchaseEmail = db.Column(db.String(255), nullable=True)
    PurchaseDate = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)
    Currency = db.Column(db.Enum(CurrencyChoices), default=CurrencyChoices.USD)
    Refunded = db.Column(db.Enum(RefundedChoices), default=RefundedChoices.NO)
    Price = db.Column(db.Float, nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(ID=_id).first()
    
    @classmethod
    def get_list(cls):
        return cls.query.all()

    def to_dict(self):
        data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        data['Currency'] = str(self.Currency)
        data['Refunded'] = str(self.Refunded)
        return data
    
    @classmethod
    def get_json_list(cls):
        sales = cls.query.all()
        return [sale.to_dict() for sale in sales]