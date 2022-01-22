import os
import re
import pandas as pd
import numpy as np
import ipdb
import django


pd.options.mode.chained_assignment = None  # default='warn'


def parse_dc_data():
    '''
    自动上传电磁式沉降环数据
    列A:日期 (yyyy/m/d  忽略y月d日)
    列G:沉降值 float
    sheet名称:DC{id}-{name}, 一个sheet对应一个测点
    '''
    source_path = 'data/DC4电磁式沉降环-整编.xlsx'

    def _get_sheets():
        '''第一步 提取要处理的sheets'''
        file_dict = pd.read_excel(source_path, sheet_name=None)
        all_sheets = file_dict.keys()
        target_sheets = [i for i in all_sheets if re.match(r'^DC\d+-\d+$', i)]
        return target_sheets

    def _parse_sheet(sheet):
        '''第二步 处理sheet中的内容'''
        content = pd.read_excel(source_path, sheet_name=sheet)
        extracted = content.iloc[:, [0, 6]]
        extracted.columns = ['date', 'value']
        clean_dates = pd.to_datetime(extracted['date'], errors='coerce')
        extracted['date'] = clean_dates
        clean_values = extracted.dropna(subset=['date'])
        return clean_values

    sheet_items = _get_sheets()
    result = dict()
    for sheet in sheet_items:
        clean_values = _parse_sheet(sheet)
        result[sheet] = clean_values
    return result


def upload(point, content):
    tmp = point.split('-')
    section = tmp[0]
    sec_object, sec_created = Msections.objects.get_or_create(
        name=section
    )
    result_message = ''
    if sec_created:
        result_message += f'section {section} created;'
    else:
        result_message += f'section {section} existed;'

    point_obj = Mpoint.objects.filter(name=point).first()
    if point_obj:
        result_message += f'delete old point {point};'
        point_obj.delete()
    else:
        result_message += f'point {point} created;'
    point_obj = Mpoint.objects.create(name=point, section=sec_object)

    content = content.dropna(axis=0, how='any')
    date = pd.to_datetime(content['date'], errors='coerce')
    value = content['value'].astype('float')
    handled_content = {
        'date': date,
        'value': value
    }
    df = pd.DataFrame(handled_content)
    count = 0
    v_objects = []
    for _, row in df.iterrows():
        date = datetime.make_aware(row['date'])
        value = row['value']
        v_objects.append(Mvalue(value=value, m_time=date, m_point=point_obj))
        count += 1
    Mvalue.objects.bulk_create(v_objects)
    result_message += f'{count} lines of values added to {point};'
    print(result_message)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dam_backend.settings')
    django.setup()

    from django.utils import timezone as datetime
    from main.models import Mpoint, Msections, Mvalue

    dc_data = parse_dc_data()
    for key in dc_data.keys():
        upload(key, dc_data[key])
