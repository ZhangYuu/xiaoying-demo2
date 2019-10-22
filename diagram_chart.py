from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
# 关于 CurrentConfig
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))
from random import randrange
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Funnel
from pyecharts.components import Table
app = Flask(__name__, static_folder="templates")

#漏斗图
def funnel_sort_ascending(study_progress) -> Funnel:
    c = (
        Funnel()
        .add(
            "学习进度",
            study_progress,
            #sort_="none",
            label_opts=opts.LabelOpts(position="inside"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="学习进度"))
    )
    return c

#下拉条折线图
def line_datazoom_slider(xlist,ylist,TitleName) -> Line:
    c = (
        Line()
        .add_xaxis(xlist)
        .add_yaxis("用户数", ylist)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=TitleName),
            datazoom_opts=[opts.DataZoomOpts()])
    )
    return c


#书本上课人数柱状图
def bar_base(book_list,book_data) -> Bar:
    c = (
        Bar()
        .add_xaxis(book_list)
        .add_yaxis("", book_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="课程用户统计", subtitle="销量"))
    )
    return c

def table_base(headers,rows) -> Table:
    table = Table()
    '''
    headers = ["City name", "Area", "Population", "Annual Rainfall"]
    rows = [
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Adelaide", 1295, 1158259, 600.5],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
    '''
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="课程用户统计表")
    )
    return table


"""
def pie_rosetype() -> Pie:
    v = Faker.choose()
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(v, [10,20,24])],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add(
            "",
            [list(z) for z in zip(v, [1,2,8])],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图示例"))
    )
    return c
"""

"""
def line_connect_null() -> Line:
    c = (
        Line()
        .add_xaxis(["一月", "二月", "三月", "四月", "五月", "六月"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)], is_connect_nones=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-连接空数据"))
    )
    return c

def funnel_sort_ascending() -> Funnel:
    c = (
        Funnel()
        .add(
            "学习进度",
            [("第一课",18),("第二课",12),("第三课",7),("第四课",5),("第五课",1)],
            #sort_="none",
            label_opts=opts.LabelOpts(position="inside"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="学习进度"))
    )
    return c
"""