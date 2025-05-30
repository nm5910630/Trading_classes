from django.shortcuts import render
import yfinance as yf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect 
from django.views.decorators.cache import cache_page
from .models import TrackedStock,Testimonial
import logging
import numpy as np
import pandas as pd

# Create your views here.
@csrf_protect
def index(request):
    stocks = TrackedStock.objects.all()
    testi = Testimonial.objects.all()
    return render(request, 'index.html', {'stocks': stocks,'testi':testi})

@csrf_protect
def feature(request):
    stocks = TrackedStock.objects.all()
    testi = Testimonial.objects.all()
    return render(request, 'feature.html', {'stocks': stocks,'testi':testi})



logger = logging.getLogger(__name__)
@csrf_protect
@cache_page(60)
def get_stock_data(request, symbol):
    try:
        logger.info(f"Fetching data for symbol: {symbol}")
        
        stock = yf.Ticker(symbol)
        hist = stock.history(period='2d')  # Changed from '1d' to '2d'
        
        if hist.empty or len(hist) < 2:
            logger.warning(f"Insufficient data for symbol: {symbol}")
            return JsonResponse({'error': 'Not enough data points', 'symbol': symbol}, status=404)
        
        # Get today's and yesterday's close prices
        today_close = hist['Close'].iloc[-1]
        yesterday_close = hist['Close'].iloc[-2]
        
        # Calculate percentage change manually
        change_percent = ((today_close - yesterday_close) / yesterday_close) * 100
        
        data = {
            'symbol': symbol,
            'price': float(today_close),
            'change': float(change_percent),
            'volume': int(hist['Volume'].iloc[-1]),
            'last_updated': hist.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
            'high': float(hist['High'].iloc[-1]),  # Today's high
            'low': float(hist['Low'].iloc[-1]),    # Today's low
        }
        
        logger.info(f"Successfully fetched data for {symbol}: {data}")
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f"Error processing {symbol}: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'Failed to fetch stock data',
            'symbol': symbol,
            'details': str(e)
        }, status=500)