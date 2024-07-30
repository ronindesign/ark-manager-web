from apps.charts import blueprint
from flask import render_template
from apps.home.models import Sales


@blueprint.route('/charts/', methods=['GET'])
def app_charts():
	sales = [{'PurchaseDate': sale.PurchaseDate, 'ItemName': sale.ItemName, 'Quantity': sale.Quantity} for sale in Sales.get_list()]
	context = {}
	context['parent'] = 'apps'
	context['segment'] = 'app_charts'
	context['sales'] = sales
	return render_template("pages/pages/charts.html", **context)