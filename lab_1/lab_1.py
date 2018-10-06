from .draw_chart import draw_charts
from .import_data import import_all_data
from .process_data import process_data


def run():
    raw_data = import_all_data()
    data = process_data(raw_data)
    draw_charts(data)
