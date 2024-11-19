from django.shortcuts import render
import numpy as np
import pandas as pd
import io
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.shortcuts import render
from django.conf import settings
from Store.models import Sanpham, Danhmuc
from analysis import models
from orders.models import Order, OrderItem
from datetime import date
from django.db.models import Count, Sum, F, Value ,FloatField
from analysis.utils import *

def work_with_series(request):
    wiews1=  pd.Series([9006.1001141,117182,9937])
    wiews1 = pd.DataFrame({'views':wiews1})
    wiews1 = wiews1.to_html()

    likes = pd.Series([402,389,403,397,404], index=["c1","c2","c3","c4","c5"])
    likes_df = pd.DataFrame({'likes':likes})
    likes1 = likes_df.to_html

    views2 = pd.read_csv(os.path.join(settings.MEDIA_ROOT,'analysis/data_views.csv'))
    views2 = pd.DataFrame({'views':views2['views']})
    headviews2 = views2.head().to_html
    tailviews2 = views2.tail().to_html

    len_views2 = len(views2)

    double_likes = likes.map(lambda x: x*2)
    double_likes = pd.DataFrame({'double_likes':double_likes})
    double_likes = double_likes.to_html

    stars = likes.describe()
    stars_df = pd.DataFrame(stars)
    stats_html = stars_df.to_html()

    return render(request,"analysis/series.html",
                  {'views1':wiews1,
                   'likes1':likes1,
                   'headviews2':headviews2,
                   'tailviews2':tailviews2,
                   'len_views2':len_views2,
                   'double_likes':double_likes,
                   'stats_html':stats_html,
                   })

# def work_with_chart_1(request):


#     data_sanpham_danhmuc = pd.read_csv(os.path.join(
#         settings.MEDIA_ROOT,'analysis/sanpham.csv'))
#     bar = get_bar( data_sanpham_danhmuc, 'Danhmuc', 'Soluong', "Số Lượng Nước Hoa Theo Danh Mục")

#     data_sanpham_thuonghieu = pd.read_csv(os.path.join(
#         settings.MEDIA_ROOT,'analysis/sanpham.csv'))
#     bar = get_bar( data_sanpham_thuonghieu, 'Danhmuc', 'Soluong', "Số Lượng Nước Hoa Theo Danh Mục")

#     return render (request,"analysis/chart.html",{'bar':bar,})



def get_graph():
    """Chuyển đổi biểu đồ thành định dạng base64 để hiển thị trên web."""
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return graph

def get_bar(data, x_name, y_name,title):
    plt.switch_backend('AGG') 
    plt.figure(figsize=(10, 6))

   
    sns.barplot(data=data, x=x_name, y=y_name, palette='viridis')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()  
    graph = get_graph()
    return graph

def work_with_chart_1(request):
    data_by_category = Sanpham.objects.values('category__name').annotate(total=Count('id'))
    df_category = pd.DataFrame(list(data_by_category))

    #  dữ liệu số lượng theo thương hiệu
    data_by_brand = Sanpham.objects.values('brand__name').annotate(total=Count('id'))
    df_brand = pd.DataFrame(list(data_by_brand))

    #  biểu đồ
    bar_category = get_bar(df_category,'category__name','total', "Số Lượng Theo Danh Mục")
    bar_brand = get_bar(df_brand,'brand__name','total', "Số Lượng Theo Thương Hiệu")

    return render(request, "analysis/chart.html", {'bar_category': bar_category, 'bar_brand': bar_brand})
    

# def get_bar(data, x_name, y_name, title):
#     plt.switch_backend('AGG') 
#     plt.figure(figsize=(10, 6))

#     # Vẽ biểu đồ cột
#     plt.bar(data[x_name], data[y_name], color='Reds')
#     plt.title(title)
#     plt.xticks(rotation=45)
#     plt.tight_layout()  
#     graph = get_graph()
#     return graph

# def get_bar(data, x_name, y_name, title):
#     fig = px.bar(data, x=x_name, y=y_name, title=title, color=y_name)
#     graph = fig.to_html(full_html=False)
#     return graph

# def work_with_chart_1(request):
#     data_by_category = Sanpham.objects.values('category__name').annotate(total=Count('id'))
#     df_category = pd.DataFrame(list(data_by_category))

#     # Dữ liệu số lượng theo thương hiệu
#     data_by_brand = Sanpham.objects.values('brand__name').annotate(total=Count('id'))
#     df_brand = pd.DataFrame(list(data_by_brand))

#     # Biểu đồ
#     bar_category = get_bar(df_category, 'category__name', 'total', "Số Lượng Theo Danh Mục")
#     bar_brand = get_bar(df_brand, 'brand__name', 'total', "Số Lượng Theo Thương Hiệu")

#     return render(request, "analysis/chart.html", {'bar_category': bar_category, 'bar_brand': bar_brand})
    


