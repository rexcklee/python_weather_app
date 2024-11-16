"""
Weather Processing App
Student: Chi Kin Lee
WeatherScraper class
"""
from html.parser import HTMLParser
import urllib.request
from datetime import datetime, date

class WeatherScraper(HTMLParser):
    """ Handle HTML parsing """
    def __init__(self, *, convert_charrefs:bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.tbody = False
        self.abbr = False
        self.td = False
        self.date_string = ''
        self.max = ''
        self.max_found = False
        self.min = ''
        self.min_found = False
        self.mean = ''
        self.mean_found = False
        self.weather_data = {}
        today_date = date.today()
        self.START_YEAR = today_date.year
        self.start_month = today_date.month
        self.end = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.tbody = True
        if self.tbody is True:
            if tag == 'abbr':
                self.abbr = True
                if attrs:
                    if attrs[0][1] != "Average" and attrs[0][1] != "Extreme":
                        self.max_found = True
                        self.date_string = attrs[0][1]
                        date_reformat = datetime.strptime(self.date_string, '%B %d, %Y')
                        self.date = date_reformat.strftime('%Y-%m-%d')
                        if date_reformat.month != self.this_month:    
                            self.end = True
            if tag == 'td' and (self.max_found is True or self.min_found is True or self.mean_found is True):
                self.td = True

    def handle_endtag(self, tag):
        if tag == 'tbody':
            self.tbody = False
        if self.tbody is True:
            if tag == 'abbr':
                self.abbr = False
            if tag == 'td' and self.max_found is True:
                self.td = False
                self.max_found = False          
                self.min_found = True
            elif tag == 'td' and self.min_found is True: 
                self.td = False
                self.min_found = False 
                self.mean_found = True  
            elif tag == 'td' and self.mean_found is True: 
                self.td = False
                self.mean_found = False   
                
    def handle_data(self, data):
        if self.tbody is True:
            if self.td is True:
                if self.max_found is True:
                    self.max = data
                if self.min_found is True:
                    self.min = data
                if self.mean_found is True:
                    self.mean = data    
                    self.weather_data[self.date] = {"Max": self.max, "Min": self.min, "Mean": self.mean}

    def get_data(self):
        for self.this_year in range(self.START_YEAR, 0, -1):
            if self.end is True:
                break
            for self.this_month in range(self.start_month, 0 , -1):
                self.start_month = 12
                with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&Day=1&Year={self.this_year}&Month={self.this_month}#') as response:
                    html = response.read().decode('utf-8')
                self.feed(html)
                if self.end is True:
                    break
        return self.weather_data