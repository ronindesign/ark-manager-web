from apps.tables import blueprint
from flask import render_template, request, redirect, url_for, jsonify, send_file, Response
from apps import db
from apps.home.models import Sales
from flask_login import login_required
from apps.tables.forms import SalesForm
from apps.tables.models import HideShowFilter, ModelChoices, ModelFilter, PageItems
import json
from apps.tables.utils import sales_filter
from io import StringIO, BytesIO
import csv


@blueprint.route("/create-filter", methods=['POST'])
def create_filter():
    if request.method == "POST":
        keys = request.form.getlist('key')
        values = request.form.getlist('value')
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]

            model_filter = ModelFilter.find_by_key_and_parent(parent=ModelChoices.SALES, key=key)
            if model_filter:
                setattr(model_filter, 'value', value)
            else:
                model_filter = ModelFilter(
                    parent=ModelChoices.SALES,
                    key=key,
                    value=value
                )
                db.session.add(model_filter)

            db.session.commit()


        return redirect(url_for('table_blueprint.datatables'))


@blueprint.route("/create-page-items", methods=['POST'])
def create_page_items():
    if request.method == 'POST':
        items = request.form.get('items')
        page_items = PageItems.find_by_parent(parent=ModelChoices.SALES)
        if page_items:
            page_items.items_per_page = items
        else:
            page_items = PageItems(parent=ModelChoices.SALES, items_per_page=items)
            db.session.add(page_items)

        db.session.commit()
        return redirect(url_for('table_blueprint.datatables'))
    
@blueprint.route("/create-hide-show-filter", methods=['POST']) 
def create_hide_show_filter():
    if request.method == "POST":
        data_str = list(request.form.keys())[0]
        data = json.loads(data_str)

        hide_show = HideShowFilter.find_by_key_and_parent(parent=ModelChoices.SALES, key=data.get('key'))
        if hide_show:
            setattr(hide_show, 'value', data.get('value'))
        else:
            hide_show = HideShowFilter(
                parent=ModelChoices.SALES,
                key=data.get('key'),
                value=data.get('value')
            )
            db.session.add(hide_show)
        
        db.session.commit()

        response_data = {'message': 'Model updated successfully'}
        return jsonify(response_data)

    return jsonify({'error': 'Invalid request'}, status=400)


@blueprint.route("/delete-filter/<id>/")
def delete_filter(id):
    filter_instance = ModelFilter.find_by_id_and_parent(id, ModelChoices.SALES)
    db.session.delete(filter_instance)
    db.session.commit()
    return redirect(url_for('table_blueprint.datatables'))


@blueprint.route("/tables", methods=['GET', 'POST'])
def datatables():
    form = SalesForm()
    db_field_names = [column.name for column in Sales.__table__.columns]

    # hide show column
    field_names = []
    for field_name in db_field_names:
        fields = HideShowFilter.find_by_key_and_parent(key=field_name, parent=ModelChoices.SALES)
        if not fields:
            hide_show = HideShowFilter(key=field_name, parent=ModelChoices.SALES)
            db.session.add(hide_show)
            db.session.commit()
        field_names.append(fields)
    

    filter_instance = ModelFilter.find_by_parent(ModelChoices.SALES)
    filter_string = {}
    for filter_data in filter_instance:
        filter_string[f'{filter_data.key}'] = f'%{filter_data.value}%'

    page_items = PageItems.find_last_by_parent(ModelChoices.SALES)

    queryset = Sales.query
    for key, value in filter_string.items():
        queryset = queryset.filter(getattr(Sales, key).ilike(value))
    
    queryset = sales_filter(queryset, db_field_names)

    if request.method == 'POST':
        form_data = {}
        for attribute, value in request.form.items():
            if attribute == 'csrf_token':
                continue
            
            column_type = Sales.__table__.columns[attribute].type
            if value == '' or value == 'None':
                if isinstance(column_type, db.Integer):
                    value = 0
                elif isinstance(column_type, db.Float):
                    value = 0.0
                else:
                    value = ''

            form_data[attribute] = value

        sales = Sales(**form_data)
        db.session.add(sales)
        db.session.commit()
        return redirect(url_for('table_blueprint.datatables'))


    context = {}
    context['parent'] = 'apps'
    context['segment'] = 'datatables'
    context['form'] = form
    context['sales'] = queryset
    context['db_field_names'] = db_field_names
    context['field_names'] = field_names
    context['filter_instance'] = filter_instance
    context['items'] = page_items
    return render_template("pages/pages/datatables.html", **context)


@blueprint.route("/delete-sales/<id>/")
def delete_sales(id):
	sales = Sales.find_by_id(id)
	db.session.delete(sales)
	db.session.commit()
	return redirect(url_for('table_blueprint.datatables'))


@blueprint.route("/update-sales/<id>/", methods=['GET', 'POST'])
def update_sales(id):
    sales = Sales.find_by_id(id)


    if request.method == 'POST':
        for attribute, value in request.form.items():
            if attribute == 'csrf_token':
                continue
            
            column_type = Sales.__table__.columns[attribute].type
            if value == '' or value == 'None':
                if isinstance(column_type, db.Integer):
                    value = 0
                elif isinstance(column_type, db.Float):
                    value = 0.0
                else:
                    value = ''
                
            setattr(sales, attribute, value)

        db.session.commit()
        
        return redirect(url_for('table_blueprint.datatables'))

    return redirect(url_for('table_blueprint.datatables'))



@blueprint.route('/export-csv', methods=['GET'])
def export_csv():
    db_field_names = [column.name for column in Sales.__table__.columns]
    fields = []
    show_fields = HideShowFilter.query.filter_by(value=False, parent=ModelChoices.SALES).all()
    for field in show_fields:
        fields.append(field.key)

    # Create an in-memory buffer
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(fields)


    filter_string = {}
    filter_instance = ModelFilter.find_by_parent(ModelChoices.SALES)
    for filter_data in filter_instance:
        filter_string[f'{filter_data.key}'] = f'%{filter_data.value}%'

    queryset = Sales.query
    for key, value in filter_string.items():
        queryset = queryset.filter(getattr(Sales, key).ilike(value))
    
    queryset = sales_filter(queryset, db_field_names)

    for product in queryset:
        row_data = [getattr(product, field) for field in fields]
        writer.writerow(row_data)

    csv_data = output.getvalue()

    response = Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="products.csv"'}
    )

    return response