from django.shortcuts import render
from statisticsManagement.models import DailyRecord
from .controllers import convert_to_dataframe, findPeak, makePrediction
from pandas import DataFrame
from pandas.plotting import lag_plot, autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AR,AutoRegResults
import numpy as np
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def Analysis(request):
    allRecords = DailyRecord.objects.all()
    df = convert_to_dataframe(allRecords, fields=['record_date', 'total_count'])
    
    # Json objects for data label
    dateList = list(df['record_date'])
    dateList = [date_obj.strftime('%Y/%m/%d') for date_obj in dateList]
    dateListJson = {'category': []}
    for each in dateList:
        dateListJson['category'].append({'label': each})

    # Json objects for count data
    countList = list(df['total_count'])
    countListJson = {'data': []}
    for each in countList:
        countListJson['data'].append({'value': each})
    print(countListJson['data'])

    return render(request,'Analysis.html', {'Data':allRecords, 'data':countListJson['data'], 'category':dateListJson['category']} )

@login_required
def training(request):
    allRecords = DailyRecord.objects.all()

    #converting model data to dataframe
    df = convert_to_dataframe(allRecords, fields=['record_date', 'total_count'])
    #getting time series
    series = DataFrame(df['total_count'])

    # saving dataset
    X = series.values
    np.save('prediction/data.npy', X)
    # training autoregression and saving model
    model = AR(X)
    model_fit = model.fit()
    print('Lag: %s' % model_fit.k_ar)
    print('Coefficients: %s' % model_fit.params)
    # saving model
    model_fit.save('prediction/AR_model')

    nowDate = timezone.now().today().date().isoformat()
    return render(request,'Analysis.html',{'Data':allRecords, 'nowDate':nowDate})

@login_required
def getPre(request):
    #data from the form
    startDate = list(map(int, request.POST.get('startDate').split('-')))
    endDate = list(map(int, request.POST.get('endDate').split('-')))
    startDate = date(startDate[0], startDate[1], startDate[2])
    endDate = date(endDate[0], endDate[1], endDate[2])

    #loading model
    model = AutoRegResults.load('prediction/AR_model')
    print(model.params)
    print(model.k_ar)
    data = np.load('prediction/data.npy')
    # make predictions
    predictions = makePrediction(startDate, endDate, model, data)
    
    # get peak value and its dates
    peakDates, value = findPeak(predictions)

    # Json objects for date label
    dateList = list(predictions.keys())
    dateList = [date_obj.strftime('%Y/%m/%d') for date_obj in dateList]
    dateListJson = {'category': []}
    for each in dateList:
        dateListJson['category'].append({'label': each})

    # Json objects for count data
    countList = list(predictions.values())
    countListJson = {'data': []}
    for each in countList:
        countListJson['data'].append({'value': each})
    print(countListJson['data'])

    return render(request,'prediction.html',{'data':countListJson['data'], 'category':dateListJson['category'], 'predictions': predictions, 'max': value, 'peakDates': peakDates})