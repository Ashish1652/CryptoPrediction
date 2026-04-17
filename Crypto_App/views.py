from django.shortcuts import render, redirect
from matplotlib import pyplot as plt

from .models import AddBlog
from .forms import blog_form
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import *
import os
import pandas as pd
import numpy as np
import math
import datetime as dt
import pandas as pd
import pickle
from datetime import datetime,timedelta
# from keras.models import load_model
import tensorflow as tf
# from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM

# Create your views here.
def index(request):
    return render(request, 'index.html')

def addGuestPost(request):
    return render(request, 'AddGuestPost.html')

def about(request):
    return render(request, 'about.html')

def displayform(request):
    form_obj = blog_form()
    return render(request,'AddGuestPost.html',{'form':form_obj})

def add_blog(request):
    if request.method == "POST":
        data = blog_form(request.POST,request.FILES)
        if data.is_valid():
            data.save()
            return redirect('/')
        else:
            form_obj = blog_form()
            return render(request, 'AddGuestPost.html', {'form': form_obj})


def display_blog(request):
    record = AddBlog.objects.all()
    return render(request,'blog.html',{'rec':record})


def prediction(request):
    return render(request, 'Prediction.html')


def UserLogin(request):
    if request.method == "POST":
        C_name = request.POST['uname']
        C_password = request.POST['pwds']
        if UserDetails.objects.filter(Username=C_name, Password=C_password).exists():
            user = UserDetails.objects.all().filter(Username=C_name, Password=C_password)
            messages.info(request, 'logged in')
            request.session['UserId'] = user[0].id
            request.session['type_id'] = 'User'
            request.session['UserType'] = C_name
            request.session['login'] = "Yes"
            return redirect("/")
        else:
            messages.info(request, 'Please Register')
            return redirect("/UserRegisteration")
    else:
        return render(request, 'UserLogin.html', {})


def bitcoin(request):
    ticker_symbol = "Bitcoin"
    current_date = datetime.today().strftime('%Y-%m-%d')
    print('current_date', current_date)
    five_years_ago = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
    print(five_years_ago)
    # gs = yf.download(ticker_symbol, start=five_years_ago, end=current_date)
    # print(gs)

    # Preprocess data
    dataset_ex_df = pd.read_csv("bitcoin_2019-01-04_2024-03-05.csv", delimiter=',')
    dataset_ex_df = dataset_ex_df[::-1]
    dataset_ex_df = dataset_ex_df.reset_index()
    dataset_ex_df['Start'] = pd.to_datetime(dataset_ex_df['Start'])
    dataset_ex_df.set_index('Start', inplace=True)
    dataset_ex_df = dataset_ex_df['Close'].to_frame()

    # Load the model
    model_path = "arima_model_bitcoin.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Forecast next 30 days
    future_forecast = model.predict(n_periods=30)

    # Print the forecasted prices
    print("Forecasted Prices for Next 30 Days:")
    print(future_forecast)

    # Plot the forecasted prices
    plt.figure(figsize=(12, 6))
    plt.plot(pd.date_range(start=dataset_ex_df.index[-1], periods=31, freq='D')[1:], future_forecast, label='Forecast')
    plt.title(f'{ticker_symbol} Stock Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Plot actual data, predicted values, and future forecast
    plt.figure(figsize=(12, 6))

    # Plot actual data
    plt.plot(dataset_ex_df.index, dataset_ex_df['Close'], label='Actual Data')

    # Plot future forecast
    future_dates = pd.date_range(start=dataset_ex_df.index[-1], periods=30, freq='D')
    plt.plot(future_dates, np.concatenate(([dataset_ex_df['Close'].iloc[-1]], future_forecast[:-1])), color='orange',
             label='Forecast for Next 30 Days')
    plt.title(f'{ticker_symbol} Stock Data with Forecast')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Show the combined plot
    plt.show()

    return redirect('/prediction')


def dogecoin(request):
    ticker_symbol = "dogecoin"
    current_date = datetime.today().strftime('%Y-%m-%d')
    print('current_date', current_date)
    five_years_ago = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
    print(five_years_ago)
    # gs = yf.download(ticker_symbol, start=five_years_ago, end=current_date)
    # print(gs)

    # Preprocess data
    dataset_ex_df = pd.read_csv("dogecoin_2019-02-04_2024-03-05.csv", delimiter=',')
    dataset_ex_df = dataset_ex_df[::-1]
    dataset_ex_df = dataset_ex_df.reset_index()
    dataset_ex_df['Start'] = pd.to_datetime(dataset_ex_df['Start'])
    dataset_ex_df.set_index('Start', inplace=True)
    dataset_ex_df = dataset_ex_df['Close'].to_frame()

    # Load the model
    model_path = "arima_model_Dogecoin.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Forecast next 30 days
    future_forecast = model.predict(n_periods=30)

    # Print the forecasted prices
    print("Forecasted Prices for Next 30 Days:")
    print(future_forecast)

    # Plot the forecasted prices
    plt.figure(figsize=(12, 6))
    plt.plot(pd.date_range(start=dataset_ex_df.index[-1], periods=31, freq='D')[1:], future_forecast, label='Forecast')
    plt.title(f'{ticker_symbol} Stock Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Plot actual data, predicted values, and future forecast
    plt.figure(figsize=(12, 6))

    # Plot actual data
    plt.plot(dataset_ex_df.index, dataset_ex_df['Close'], label='Actual Data')

    # Plot future forecast
    future_dates = pd.date_range(start=dataset_ex_df.index[-1], periods=30, freq='D')
    plt.plot(future_dates, np.concatenate(([dataset_ex_df['Close'].iloc[-1]], future_forecast[:-1])), color='orange',
             label='Forecast for Next 30 Days')
    plt.title(f'{ticker_symbol} Stock Data with Forecast')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Show the combined plot
    plt.show()

    return redirect('/prediction')


def binance(request):
    ticker_symbol = "Binance"
    current_date = datetime.today().strftime('%Y-%m-%d')
    print('current_date', current_date)
    five_years_ago = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
    print(five_years_ago)
    # gs = yf.download(ticker_symbol, start=five_years_ago, end=current_date)
    # print(gs)

    # Preprocess data
    dataset_ex_df = pd.read_csv("binance-coin_2019-01-04_2024-03-05.csv", delimiter=',')
    dataset_ex_df = dataset_ex_df[::-1]
    dataset_ex_df = dataset_ex_df.reset_index()
    dataset_ex_df['Start'] = pd.to_datetime(dataset_ex_df['Start'])
    dataset_ex_df.set_index('Start', inplace=True)
    dataset_ex_df = dataset_ex_df['Close'].to_frame()

    # Load the model
    model_path = "arima_model_binance.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Forecast next 30 days
    future_forecast = model.predict(n_periods=30)

    # Print the forecasted prices
    print("Forecasted Prices for Next 30 Days:")
    print(future_forecast)

    # Plot the forecasted prices
    plt.figure(figsize=(12, 6))
    plt.plot(pd.date_range(start=dataset_ex_df.index[-1], periods=31, freq='D')[1:], future_forecast, label='Forecast')
    plt.title(f'{ticker_symbol} Stock Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Plot actual data, predicted values, and future forecast
    plt.figure(figsize=(12, 6))

    # Plot actual data
    plt.plot(dataset_ex_df.index, dataset_ex_df['Close'], label='Actual Data')

    # Plot future forecast
    future_dates = pd.date_range(start=dataset_ex_df.index[-1], periods=30, freq='D')
    plt.plot(future_dates, np.concatenate(([dataset_ex_df['Close'].iloc[-1]], future_forecast[:-1])), color='orange',
             label='Forecast for Next 30 Days')
    plt.title(f'{ticker_symbol} Stock Data with Forecast')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Show the combined plot
    plt.show()

    return redirect('/prediction')


def polkadot(request):
    ticker_symbol = "polkadot"
    current_date = datetime.today().strftime('%Y-%m-%d')
    print('current_date', current_date)
    five_years_ago = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
    print(five_years_ago)
    # gs = yf.download(ticker_symbol, start=five_years_ago, end=current_date)
    # print(gs)

    # Preprocess data
    dataset_ex_df = pd.read_csv("polkadot_2020-08-21_2024-03-05.csv", delimiter=',')
    dataset_ex_df = dataset_ex_df[::-1]
    dataset_ex_df = dataset_ex_df.reset_index()
    dataset_ex_df['Start'] = pd.to_datetime(dataset_ex_df['Start'])
    dataset_ex_df.set_index('Start', inplace=True)
    dataset_ex_df = dataset_ex_df['Close'].to_frame()

    # Load the model
    model_path = "arima_model_polkadot.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Forecast next 30 days
    future_forecast = model.predict(n_periods=30)

    # Print the forecasted prices
    print("Forecasted Prices for Next 30 Days:")
    print(future_forecast)

    # Plot the forecasted prices
    plt.figure(figsize=(12, 6))
    plt.plot(pd.date_range(start=dataset_ex_df.index[-1], periods=31, freq='D')[1:], future_forecast, label='Forecast')
    plt.title(f'{ticker_symbol} Stock Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Plot actual data, predicted values, and future forecast
    plt.figure(figsize=(12, 6))

    # Plot actual data
    plt.plot(dataset_ex_df.index, dataset_ex_df['Close'], label='Actual Data')

    # Plot future forecast
    future_dates = pd.date_range(start=dataset_ex_df.index[-1], periods=30, freq='D')
    plt.plot(future_dates, np.concatenate(([dataset_ex_df['Close'].iloc[-1]], future_forecast[:-1])), color='orange',
             label='Forecast for Next 30 Days')
    plt.title(f'{ticker_symbol} Stock Data with Forecast')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Show the combined plot
    plt.show()

    return redirect('/prediction')


def tether(request):
    ticker_symbol = "Tether"
    current_date = datetime.today().strftime('%Y-%m-%d')
    print('current_date', current_date)
    five_years_ago = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
    print(five_years_ago)
    # gs = yf.download(ticker_symbol, start=five_years_ago, end=current_date)
    # print(gs)

    # Preprocess data
    dataset_ex_df = pd.read_csv("Tether USDt_8_21_2019-10_20_2019_historical_data_coinmarketcap.csv", delimiter=';')
    dataset_ex_df = dataset_ex_df[::-1]
    dataset_ex_df = dataset_ex_df.reset_index()
    dataset_ex_df['timeOpen'] = pd.to_datetime(dataset_ex_df['timeOpen'])
    dataset_ex_df.set_index('timeOpen', inplace=True)
    dataset_ex_df = dataset_ex_df['close'].to_frame()

    # Load the model
    model_path = "arima_model.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Forecast next 30 days
    future_forecast = model.predict(n_periods=30)

    # Print the forecasted prices
    print("Forecasted Prices for Next 30 Days:")
    print(future_forecast)

    # Plot the forecasted prices
    plt.figure(figsize=(12, 6))
    plt.plot(pd.date_range(start=dataset_ex_df.index[-1], periods=31, freq='D')[1:], future_forecast, label='Forecast')
    plt.title(f'{ticker_symbol} Stock Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Plot actual data, predicted values, and future forecast
    plt.figure(figsize=(12, 6))

    # Plot actual data
    plt.plot(dataset_ex_df.index, dataset_ex_df['close'], label='Actual Data')

    # Plot future forecast
    future_dates = pd.date_range(start=dataset_ex_df.index[-1], periods=30, freq='D')
    plt.plot(future_dates, np.concatenate(([dataset_ex_df['close'].iloc[-1]], future_forecast[:-1])), color='orange',
             label='Forecast for Next 30 Days')
    plt.title(f'{ticker_symbol} Stock Data with Forecast')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Show the combined plot
    plt.show()

    return redirect('/prediction')


def ethereum(request):
    ticker_symbol = "Ethereum"
    current_date = datetime.today().strftime('%Y-%m-%d')
    print('current_date', current_date)
    five_years_ago = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
    print(five_years_ago)
    # gs = yf.download(ticker_symbol, start=five_years_ago, end=current_date)
    # print(gs)

    # Preprocess data
    dataset_ex_df = pd.read_csv("ethereum_2019-03-04_2024-03-05.csv", delimiter=',')
    dataset_ex_df = dataset_ex_df[::-1]
    dataset_ex_df = dataset_ex_df.reset_index()
    dataset_ex_df['Start'] = pd.to_datetime(dataset_ex_df['Start'])
    dataset_ex_df.set_index('Start', inplace=True)
    dataset_ex_df = dataset_ex_df['Close'].to_frame()

    # Load the model
    model_path = "arima_model_ethereum.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Forecast next 30 days
    future_forecast = model.predict(n_periods=30)

    # Print the forecasted prices
    print("Forecasted Prices for Next 30 Days:")
    print(future_forecast)

    # Plot the forecasted prices
    plt.figure(figsize=(12, 6))
    plt.plot(pd.date_range(start=dataset_ex_df.index[-1], periods=31, freq='D')[1:], future_forecast, label='Forecast')
    plt.title(f'{ticker_symbol} Stock Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Plot actual data, predicted values, and future forecast
    plt.figure(figsize=(12, 6))

    # Plot actual data
    plt.plot(dataset_ex_df.index, dataset_ex_df['Close'], label='Actual Data')

    # Plot future forecast
    future_dates = pd.date_range(start=dataset_ex_df.index[-1], periods=30, freq='D')
    plt.plot(future_dates, np.concatenate(([dataset_ex_df['Close'].iloc[-1]], future_forecast[:-1])), color='orange',
             label='Forecast for Next 30 Days')
    plt.title(f'{ticker_symbol} Stock Data with Forecast')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)

    # Show the combined plot
    plt.show()

    return redirect('/prediction')
