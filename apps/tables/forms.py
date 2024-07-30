from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField, DateField, EmailField
from apps.home.models import CurrencyChoices, RefundedChoices

class SalesForm(FlaskForm):
    ItemName = StringField('Item Name', id="Item_Name", render_kw={'class': 'form-control'})
    BuyerName = StringField('Buyer Name', id="Buyer_Name", render_kw={'class': 'form-control'})
    PurchaseEmail = EmailField('Purchase Email', id="Purchase_Email", render_kw={'class': 'form-control'})
    PurchaseDate = DateField('Purchase Date', id="Purchase_Date", render_kw={'class': 'form-control'})
    Country = StringField('Country', id="Country", render_kw={'class': 'form-control'})
    Price = IntegerField('Price', id="Price", render_kw={'class': 'form-control', 'step': '0.1'})
    Quantity = IntegerField('Quantity', id="Quantity", render_kw={'class': 'form-control'})
    Currency = SelectField('Currency', id="Currency", choices=[(choice.name, choice.value) for choice in CurrencyChoices], render_kw={'class': 'form-select'})
    Refunded = SelectField('Refunded', id="Refunded", choices=[(choice.name, choice.value) for choice in RefundedChoices], render_kw={'class': 'form-select'})