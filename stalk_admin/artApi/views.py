# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StrawData1, StrawData2, StrawData3
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import functools

import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

import os
from stalk_admin.settings import BASE_DIR

# 模型路径
modelBP_path = "'D:\\BP2.h5'"


# Create your views here.
@api_view(['GET'])
def tableData(request):
    # 获取前端传递的参数
    page = request.GET.get('page')
    # limit 为数组[1,5],是id的范围
    limit = request.GET.get('limit')
    limit = eval(limit)
    tableNum = request.GET.get('tableNum')
    print(page)

    # 获取数据
    if tableNum == 'data1':
        # 获取数据
        data = StrawData1.objects.filter(id__range=limit)
    elif tableNum == 'data2':
        # 获取数据
        data = StrawData2.objects.filter(id__range=limit)
    elif tableNum == 'data3':
        # 获取数据
        data = StrawData3.objects.filter(id__range=limit)

    # 获取数据总数
    total = data.count()
    # 分页，每页10条数据
    paginator = Paginator(data, 10)
    # 获取第几页的数据
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    # 整理数据
    data_list = []
    for i in data:
        item = {
            'id': i.id,
            'material_ts': format(float(i.material_ts), '.4f'),
            'material_vs': format(float(i.material_vs), '.4f'),
            'carbon': getattr(i, 'carbon', '0'),
            'hydrogen': getattr(i, 'hydrogen', '0'),
            'oxygen': getattr(i, 'oxygen', '0'),
            'nitrogen': getattr(i, 'nitrogen', '0'),
            # 如果是0，就是'否'，如果是1，就是'是'
            'is_add': '是' if i.is_add else '否',
            'is_pre': '是' if i.is_pre else '否',
            'days': i.days,
            'ch4': format(float(i.ch4), '.4f'),
            'gas': format(float(i.gas), '.4f'),
        }
        data_list.append(item)

    # 返回数据
    return Response({'msg': '获取数据成功', 'data': data_list, 'total': total})


# 智能搜索
@api_view(['GET'])
def search(request):
    modelType = request.GET.get('modelType')
    searchObj = request.GET.get('searchObj')
    dataNum = request.GET.get('dataNum')
    searchObj = eval(searchObj)

    data_num = 1
    if dataNum == 'data1':
        data_num = 1
    elif dataNum == 'data2':
        data_num = 2
    elif dataNum == 'data3':
        data_num = 3

    # 获取数据,BP神经网络
    if modelType == '1':
        print('BP神经网络')
        # 获取参数
        paramObj = getPredictObj(searchObj)
        paramObj = np.array([list(paramObj.values())])
        # 获取预测数据
        preData = getPreData(paramObj, data_num, 'BP_' + dataNum)
        # 整理数据
        data_list = {
            'ch4': format(float(preData[0][0]), '.4f'),
            'gas': format(float(preData[0][1]), '.4f'),
        }
        # 返回数据
        return Response({'msg': '获取数据成功', 'data': data_list})

    elif modelType == '2':
        print('RBF神经网络')
        # 获取参数
        paramObj = getPredictObj(searchObj)
        paramObj = np.array([list(paramObj.values())])
        # 获取预测数据
        preData = getPreData(paramObj, data_num, 'RBF_'+ dataNum)
        # 整理数据
        data_list = {
            'ch4': format(float(preData[0][0]), '.4f'),
            'gas': format(float(preData[0][1]), '.4f'),
        }
        # 返回数据
        return Response({'msg': '获取数据成功', 'data': data_list})

    elif modelType == '3':
        print('LSTM神经网络')
        # 获取参数
        paramObj = getPredictObj(searchObj)
        paramObj = np.array([list(paramObj.values())])
        # 获取预测数据
        preData = getPreData(paramObj, data_num, 'LSTM_'+ dataNum)
        # 整理数据
        data_list = {
            'ch4': format(float(preData[0][0]), '.4f'),
            'gas': format(float(preData[0][1]), '.4f'),
        }
        # 返回数据
        return Response({'msg': '获取数据成功', 'data': data_list})
    
    else:
        return Response({'msg': '预测数据失败，请检查参数是否正确', 'data': ''})
    

# 预测模型函数
def getPreData(paramObj, tableNum, models):
    x_data, y_data = readData(tableNum)
    dict1 = paramObj
    # 打印数据
    print('数据集：', x_data[0])
    print('参数为：', dict1)

    # 获取归一化对象
    scaler, scaler_y = getMinMaxScaler(x_data, y_data)

    # 加载模型
    if models == 'BP_data1':
        model = tf.keras.models.load_model('D:\\BP_data1_1.h5')
    elif models == 'BP_data2':
        model = tf.keras.models.load_model('D:\\BP_data2_1.h5')
    elif models == 'BP_data3':
        model = tf.keras.models.load_model('D:\\BP_data3_1.h5')
    elif models == 'RBF_data1':
        model = tf.keras.models.load_model('D:\\RBF_data1_1.h5')
    elif models == 'RBF_data2':
        model = tf.keras.models.load_model('D:\\RBF_data2_1.h5')
    elif models == 'RBF_data3':
        model = tf.keras.models.load_model('D:\\RBF_data3_1.h5')
    elif models == 'LSTM_data1':
        model = tf.keras.models.load_model('D:\\LSTM_data1_1.h5')
    elif models == 'LSTM_data2':
        model = tf.keras.models.load_model('D:\\LSTM_data2_1.h5')
    elif models == 'LSTM_data3':
        model = tf.keras.models.load_model('D:\\LSTM_data3_1.h5')
    else:
        return '模型加载失败'
    dict1 = scaler.transform(dict1)
    # 预测
    predictions = model.predict(dict1)
    # 反归一化
    predictions = scaler_y.inverse_transform(predictions)
    return predictions

# 归一化函数
def getMinMaxScaler(x, y):
    # 归一化
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    scaler_y = MinMaxScaler()
    y = scaler_y.fit_transform(y)
    return scaler, scaler_y

# 参数整理函数
def getParams(obj):
    paramObj = {}
    if obj['is_add'] != '是':
        obj['is_add'] = '0'
    else:
        obj['is_add'] = '1'
    if obj['is_pre'] != '是':
        obj['is_pre'] = '0'
    else:
        obj['is_pre'] = '1'
    # 遍历对象，如果值不为空，就添加到参数对象中
    for key, value in obj.items():
        if value:
            paramObj[key + '__icontains'] = value
    return paramObj

# 预测对象整理函数
def getPredictObj(obj):
    predictObj = {}
    if obj['is_add'] != '是':
        obj['is_add'] = '0'
    else:
        obj['is_add'] = '1'
    if obj['is_pre'] != '是':
        obj['is_pre'] = '0'
    else:
        obj['is_pre'] = '1'
    # 遍历对象，如果值不为空，就添加到参数对象中
    for key, value in obj.items():
        if value:
            predictObj[key] = float(value)
    return predictObj

# 智能预测
@api_view(['GET'])
def predict(request):
    x_data, y_data = readData(1)

    stalk_data1 = StrawData1.objects.all()
    # 构建同类型的DataFrame
    item = {
        'material_ts': stalk_data1[0].material_ts,
        'material_vs': stalk_data1[0].material_vs,
        'carbon': stalk_data1[0].carbon,
        'hydrogen': stalk_data1[0].hydrogen,
        'nitrogen': stalk_data1[0].nitrogen,
        'is_add': stalk_data1[0].is_add,
        'is_pre': stalk_data1[0].is_pre,
        'days': stalk_data1[0].days,
    }
    dict1 = []
    for i in item.values():
        dict1.append(float(i))
    
    dict1 = np.array(dict1)

    # 归一化
    scaler = MinMaxScaler()
    x_data = scaler.fit_transform(x_data)
    scaler_y = MinMaxScaler()
    y_data = scaler_y.fit_transform(y_data)
    print('整体归一化的第一条数据', x_data[0])

    # 加载模型
    model = tf.keras.models.load_model('D:\\BP2.h5')

    # 对dict1进行归一化
    dict1 = scaler.transform(dict1.reshape(1, -1))
    print('归一化后的数据', dict1)

    # 预测
    predictions = model.predict(dict1)
    print('预测结果', predictions)

    # 反归一化
    predictions = scaler_y.inverse_transform(predictions)
    print('反归一化后的数据', predictions)

    # 返回数据
    return Response({'msg': '数据预测', 'data': predictions.tolist()})


# 数据集读取
@functools.lru_cache(maxsize=None)
def readData(num):
    x_data = []
    y_data = []
    # 读取数据库数据
    if num == 1:
        data = StrawData1.objects.all()
        for i in data:
            item1 = [
                float(i.material_ts), float(i.material_vs),float(i.carbon),float(i.hydrogen),float(i.nitrogen),float(i.is_add),float(i.is_pre),float(i.days)
            ]
            item2 = [i.ch4, i.gas]
            x_data.append(np.array(item1))
            y_data.append(np.array(item2))
        
    elif num == 2:
        data = StrawData2.objects.all()
        x_data = []
        y_data = []
        for i in data:
            item1 = [
                float(i.material_ts), float(i.material_vs),float(i.is_add),float(i.is_pre),float(i.days),
            ]
            item2 = [i.ch4, i.gas]
            x_data.append(np.array(item1))
            y_data.append(np.array(item2))
        
    elif num == 3:
        data = StrawData3.objects.all()
        x_data = []
        y_data = []
        for i in data:
            item1 = [
                float(i.material_ts), float(i.material_vs),float(i.carbon),float(i.hydrogen),i.oxygen,float(i.nitrogen),float(i.is_add),float(i.is_pre),float(i.days)
            ]
            item2 = [i.ch4, i.gas]
            x_data.append(np.array(item1))
            y_data.append(np.array(item2))
    
    return x_data, y_data
        
# 是否 转 01
def char_to_num(x_data ,a1, a2):
    for i in range(len(x_data)):
        if x_data[i][a1] == '是':
            x_data[i][a1] = 1
        else:
            x_data[i][a1] = 0
        if x_data[i][a2] == '是':
            x_data[i][a2] = 1
        else:
            x_data[i][a2] = 0
    return x_data