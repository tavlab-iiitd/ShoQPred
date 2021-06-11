import pickle
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler


model = 'xgb_adult'
df = None
tsdf = None
new_data = None
process = None
stdcol = ['ID','sao2','heartrate','respiration','systemicsystolic','systemicdiastolic']
feat = list(pd.read_csv('weights/features.csv')['features'])
age, gender = 0,0

def index(request):
    return render(request, "index.html")


def about(request):
    context = {}
    template = loader.get_template('pages/about.html')
    return HttpResponse(template.render(context, request))


def authors(request):
    context = {}
    template = loader.get_template('pages/authors.html')
    return HttpResponse(template.render(context, request))


def git(request):
    return redirect("https://github.com/SAFE-ICU/ShoQPred")


def start(request):
    global model
    global df
    global age
    global gender
    if request.method == 'POST':
        print(request.POST)
        to_predict = request.POST['to_predict']
        pred_time = request.POST['time']
        age = request.POST['age']
        gender = request.POST['gender']
        gender = int(gender)
        age = int(age)
        model = 'xgb_adult' if age >= 18 else 'xgb_ped'
        if not type(df) == type(pd.DataFrame):
            context = {'model': model}
        else:
            context = {'model': model, 'data_frame': df}
        template = loader.get_template('pages/startXGB.html')
        return HttpResponse(template.render(context, request))
    if not type(df)==type(pd.DataFrame):
        context = {'model': model,'process':process}
    else:
        context = {'model': model,'data_frame':df,'process':process}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def uploadcsv(request):
    global model
    global df
    print(request.FILES)
    if request.FILES:
        csv = request.FILES['file']
        df = pd.read_csv(csv)
        context = {'data_frame': df.to_html(),'model': model,'process':process}
        template = loader.get_template('pages/startXGB.html')
        return HttpResponse(template.render(context, request))
    dfhtml = None if not type(df)==type(pd.DataFrame()) else df.to_html()
    context = {'data_frame': dfhtml,'model': model, 'process':process}
    template = loader.get_template('pages/startXGB.html')
    return HttpResponse(template.render(context, request))


def showPreprocess(request):
    global model
    global df
    dfhtml = None if not type(df) == type(pd.DataFrame()) else df.to_html()
    context = {'data_frame': dfhtml, 'model': model}
    context = {'data_frame': df.to_html(),'model': model}
    template = loader.get_template('pages/processXGB.html')
    return HttpResponse(template.render(context, request))


def scale_data(array, means, stds):
    return (array - means) / stds

def preprocessing(request):
    global model
    global df
    global tsdf
    global feat
    global process
    print(type(df),type(pd.DataFrame()))
    if type(df) != type(pd.DataFrame()):
        redirect(reverse('start'))
    else:
        df.to_html()
    process = list(df.columns) == stdcol
    if request.method == 'POST':
        print(request.POST)
        pid = request.POST['pid_options_file']
        hr = request.POST['hr_options_file']
        resp = request.POST['resp_options_file']
        spo2 = request.POST['spo2_options_file']
        bp = request.POST['bp_options_file']
        bp_dias = request.POST['bp_dias_options_file']
        cols = [pid, spo2, hr, resp, bp, bp_dias]
        df = df[cols]
        df.columns = stdcol
        process = list(df.columns) == stdcol
        new_data = None
        context = {'data_frame': df.to_html(),'model': model,'columns':df.columns,'process':process}
        template = loader.get_template('pages/processXGB.html')
        return HttpResponse(template.render(context, request))
    if not type(df) == type(pd.DataFrame()):
        redirect(reverse('start'))
    else:
        df.to_html()
    context = {'data_frame': df.to_html(),'model': model,'columns':df.columns,'process':process}
    template = loader.get_template('pages/processXGB.html')
    return HttpResponse(template.render(context, request))

def classify(request):
    global df
    global tsdf
    global new_data
    if not type(tsdf) == type(pd.DataFrame()):
        redirect(reverse('start'))
    else:
        tsdf.to_html()
    if not type(new_data)==type(pd.DataFrame()):

        with open('weights/'+model+'.sav', "rb") as file:
            xgb = pickle.load(file)
        with open('weights/' + model + '_scaler.pkl', "rb") as file:
            scaler = pickle.load(file)
        scaler = scaler['5_fold_object']
        print(df)
        tsdf = extract_features(df, column_id='ID')
        tsdf = impute(tsdf)
        tsdf['age'] = age
        tsdf['gender'] = gender
        tsdf.columns = tsdf.columns.str.lower()
        tsdf = tsdf[feat]
        print(tsdf.shape)
        print(scaler)
        tsdf = scaler.transform(tsdf)
        result = xgb.predict_proba(tsdf)
        result = result[0, 1]
        cutoff = pd.read_csv('weights/cutoff.csv')
        cutoff = cutoff[cutoff['model_name']==model][['cutoff']].iloc[0,0]
        new_data = pd.DataFrame({"Patient ID ": [df.iloc[0,0]],
                                 "Predicted Score": [result],
                                 "Cutoff score": cutoff,
                                 "Predicted Label": ["Shock" if result>cutoff else "Non-Shock"]})
        print(new_data)
        # new_data = new_data.append({filename: predicted_output})
        context = {'result': new_data.to_html(), 'shock': result * 1000, 'ns': (1 - result) * 1000}
        template = loader.get_template('pages/classifyXGB.html')
        return HttpResponse(template.render(context, request))

    print(new_data)
    # new_data = new_data.append({filename: predicted_output})
    context = {'result':new_data.to_html(), 'shock':new_data['Predicted Score'][0] * 1000,'ns':(1 - new_data['Predicted Score'][0]) * 1000}
    template = loader.get_template('pages/classifyXGB.html')
    return HttpResponse(template.render(context, request))


def download(request,idx):
    if idx==0 and type(df)==type(pd.DataFrame()):
        results = df
    elif idx==1 and type(df)==type(pd.DataFrame()):
        results = df
    elif idx==2 and type(new_data)==type(pd.DataFrame()):
        results = new_data
    elif idx==3 and type(tsdf)==type(pd.DataFrame()):
        results = new_data
    else:
        return redirect(reverse('home'))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=filename.csv'
    results.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
    return response


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))
