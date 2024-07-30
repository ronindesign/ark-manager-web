from sqlalchemy import or_
from apps.home.models import Sales
from flask import request

def sales_filter(queryset, fields):
    value = request.args.get('search')

    if value:
        filters = []
        for field in fields:
            filters.append(getattr(Sales, field).ilike(f"%{value}%"))
        dynamic_filter = or_(*filters)
        return queryset.filter(dynamic_filter)

    return queryset