"""
Weather Processing App
Student: Chi Kin Lee
DBOperations class
"""
from dbcm import DBCM
from scrape_weather import WeatherScraper

class DBOperations:
    """ DBOperations is a class operate a weather app database """
    def __init__(self, dbname):
        self.initialize_db(dbname)

    def initialize_db(self, dbname):
        self.dbname = dbname   
        with DBCM(self.dbname) as cursor:
            try:
                cursor.execute("""create table samples 
                                   (id integer primary key autoincrement not null,
                                   date text not null,
                                   location text not null,
                                   min_temp real not null,
                                   max_temp real not null,
                                   avg_temp real not null,
                                   UNIQUE(date, location)
                                );""")
                print("Table created successfully.")
            except Exception as e:
                print("Creating table:", e)

    def save_data(self, weather_data):
        """ Insert weather data into the database """
        with DBCM(self.dbname) as cursor:
            for date, values in weather_data.items():
                sql = """insert into samples (date,location,min_temp,max_temp,avg_temp)
                         values (?,?,?,?,?)"""
                data = (date, 'Winnipeg, MB', values['Max'], values['Min'], values['Mean'])
                try:
                    cursor.execute(sql, data)
                    print("Added sample successfully.")
                except Exception as e:
                    print("Error inserting sample of date:", date, e)

    def fetch_data(self):
        """ return the weather data in the database """
        data = []
        with DBCM(self.dbname) as cursor:
            try:
                for row in cursor.execute("select * from samples"):
                    data.append(row)
                return data
            except Exception as e:
                print("Error fetching samples.", e)

    def purge_data(self):
        """ purge all the data in the database """
        with DBCM(self.dbname) as cursor:
            try: 
                cursor.execute("DELETE FROM samples")
            except Exception as e:
                print("Error deleting data in samples.", e)

duplicate_weather_data = {"2018-06-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
                          "2018-06-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
                          "2018-06-04": {"Max": 31.3, "Min": 29.9, "Mean": 30.0}}

# weatherScraper = WeatherScraper()
weatherdb = DBOperations("weather_test.sqlite")
# weatherdb.save_data(duplicate_weather_data)
print(weatherdb.fetch_data())
# weatherdb.purge_data()
