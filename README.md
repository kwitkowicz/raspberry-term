# DHTDynamicCharts

Database logger and web interface for DHT11 Sensor on Raspberry Pi 

## Description

A CherryPy web server and database logger for DHT11 temperature and hummidity sensor on the Raspberry Pi. The sensor is accessed using [Adafruit Python DHT Sensor Library](https://github.com/adafruit/Adafruit_Python_DHT). The logger reads data from the sensor, writes it to an SQLite database and returns the temperature, humidity and dew point. The server reads and exposes results to the front-end - simple pages written in HTML and JavaScript.

## Installation

Just clone a [repository](https://github.com/kwitkowicz/raspberry-term.git):
```
git clone https://github.com/kwitkowicz/raspberry-term.git
```

## Usage

Start server:
```
python temp_server.py
```
for 'in memory' database, or
```
python temp_server.py -f
```
for database in a regular file (First time you should execute `python db_setup.py` to create a database schema).
Next go to the browser and open `http://your_raspberry_ip:8080` for the current, animated data or `http://your_raspberry_ip:8080/historic` for the archival data plot. Historical data view has a primitive api: you can choose a time window using "start_date" and/or "stop_date" parameters, e.g.
```
http://192.168.0.53:8080/historic?start_date=2016-01-01 12:00:00&stop_date=2017-01-20 11:47:20
```

## Dependencies
* SQLite3
* Highcharts
* CherryPy
* Adafruit Python DHT 

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

GPL
