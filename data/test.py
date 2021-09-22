'''
使用pandas读取csv文件
    文件名是测点ID
    第一列是日期
    第二列是检测值
要求
    删除没有检测值的行
'''
import pandas

file_name = 'DC4-6.csv'

def handle_file_name(name):
    