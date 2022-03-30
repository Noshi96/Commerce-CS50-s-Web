
from auctions.models import Category

def categories():
    my_list = []
    keys = range(len(Category.objects.all()))
    values = [category.category_name for category in Category.objects.all()]
    for i in keys:
            my_list.append((str(i), str(values[i])))
    return my_list

