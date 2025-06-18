import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("weather_icon.jpg"))
        self.setMinimumSize(400, 600)
        self.initUI()
        self.setTheme()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Search section
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name...")
        self.getWeather = QPushButton("Search")

        search_layout.addWidget(self.city_input)
        search_layout.addWidget(self.getWeather)
        search_frame.setLayout(search_layout)
        main_layout.addWidget(search_frame)

        weather_frame = QFrame()
        weather_frame.setObjectName("weatherFrame")
        weather_layout = QVBoxLayout()
        weather_layout.setSpacing(15)

        self.name_city = QLabel()
        self.name_city.setAlignment(Qt.AlignCenter)
        self.temperature = QLabel()
        self.temperature.setAlignment(Qt.AlignCenter)
        self.icon_weather = QLabel()
        self.icon_weather.setAlignment(Qt.AlignCenter)
        self.description = QLabel()
        self.description.setAlignment(Qt.AlignCenter)
        self.min_max = QLabel()
        self.min_max.setAlignment(Qt.AlignCenter)
        self.feelslike = QLabel()
        self.feelslike.setAlignment(Qt.AlignCenter)
        self.wind_speed = QLabel()
        self.wind_speed.setAlignment(Qt.AlignCenter)
        self.humidity = QLabel()
        self.humidity.setAlignment(Qt.AlignCenter)
        
        weather_layout.addWidget(self.name_city)
        weather_layout.addWidget(self.temperature)
        weather_layout.addWidget(self.icon_weather)
        weather_layout.addWidget(self.description)
        weather_layout.addWidget(self.min_max)
        weather_layout.addWidget(self.feelslike)
        weather_layout.addWidget(self.wind_speed)
        weather_layout.addWidget(self.humidity)
        weather_frame.setLayout(weather_layout)
        main_layout.addWidget(weather_frame)

        self.getWeather.clicked.connect(self.get_weather)
        self.setLayout(main_layout)

    def setTheme(self):
        self.icon_weather.setObjectName("icon")
        self.name_city.setObjectName("city")
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1a1a2e;
                font-family: 'Segoe UI', Arial;
                color: #ffffff;
            }
            
            #searchFrame {
                background-color: #16213e;
                border-radius: 15px;
                padding: 15px;
                border: 1px solid #0f3460;
            }
            
            #weatherFrame {
                background-color: #16213e;
                border-radius: 20px;
                padding: 25px;
                border: 2px solid #0f3460;
            }
            
            
            QLineEdit {
                font-size: 25px;
                padding: 12px;
                border: 2px solid #0f3460;
                border-radius: 10px;
                background-color: #1a1a2e;
                color: #ffffff;
            }
            
            QLineEdit:focus {
                border: 2px solid #e94560;
            }
            
            QPushButton {
                font-size: 25px;
                color: white;
                background-color: #e94560;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #ff6b81;
            }
            
            QPushButton:pressed {
                background-color: #d6336c;
            }
            
            #temperature {
                font-size: 80px;
                font-weight: bold;
                color: #ffffff;
                margin: 10px 0;
            }
            
            #description {
                font-size: 28px;
                color: #e94560;
                margin: 25px 0;
                font-weight: 500;
            }
            
            #weathericon {
                font-size: 120px;
                margin: 15px 0;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 25px;
                padding:10px;
                border-radius:15px;
            }
            
            #min_max {
                color: #a2d2ff;
                font-size: 30px;
                margin: 10px 0;
            }
            
            #wind_speed, #humidity {
                color: #a2d2ff;
                font-size: 30px;
                margin: 5px 0;
            }
            #city{
                font-size:20px;
            }
            
        """
        )

    def get_weather(self):
        API = "7657c0648de544796d267f52a43ce5dd"
        city_name = self.city_input.text()
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()  #! raises error for http error
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as httpError:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nplease check your input")
                case 401:
                    self.display_error("Unautorized:\ninvalid api key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal server error:\nplase try again later")
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service unavailable:\nserver is down")
                case 504:
                    self.display_error("Gateaway timeout:\nno response from the server")
                case _:
                    self.display_error(f"http error occured {httpError}")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"request error: {req_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Check your internet connection")

    def display_error(self, message):
        self.temperature.setStyleSheet("color:red;" "font-size:25px;")
        self.temperature.setText(message)
        self.description.setText("")
        self.icon_weather.setText("")
        self.name_city.setText("")
        self.min_max.setText("")
        self.wind_speed.setText("")
        self.humidity.setText("")
        self.feelslike.setText("")
        


    def display_weather(self, data):
        self.temperature.setStyleSheet("color:white;" "font-size:25px;")
        
        temp_inK = data["main"]["temp"]  #! access main dictionary
        temp_inC = temp_inK - 273.15
        self.temperature.setText(f"{temp_inC:.0f}°C")
        desc = data["weather"][0]["description"]  #! access weather list
        desc = desc.title()
        weather_id = data["weather"][0]["id"]
        icon = self.icon_weather
        if weather_id >= 200 and weather_id < 300:
            icon.setText("⛈️")
        elif weather_id >= 300 and weather_id < 500:
            icon.setText("☔")
        elif weather_id >= 500 and weather_id < 600:
            icon.setText("🌧️")
        elif weather_id >= 600 and weather_id < 700:
            icon.setText("☃️")
        elif weather_id >= 700 and weather_id < 800:
            icon.setText("☁️")
        elif weather_id == 800:
            icon.setText("☀️")
        elif weather_id > 800:
            icon.setText("🌥️")

        self.description.setText(desc)
        min_temp = data["main"]["temp_min"] - 273.15
        max_temp = data["main"]["temp_max"] - 273.15
        feels_temp = data["main"]["feels_like"] - 273.15
        self.min_max.setText(
            f"{max_temp:.0f}°C / {min_temp:.0f}°C"
        )
        self.feelslike.setText(f"Feels like: {feels_temp:.0f}°C")

        speed_wind = data["wind"]["speed"] * 3.6
        self.wind_speed.setText(f"Wind: {speed_wind:.0f}km/h")

        humidity_data = data["main"]["humidity"]
        self.humidity.setText(f"Humidity: {humidity_data:.0f}%")
        
        name_of_city = data["name"].title()
        self.name_city.setText(name_of_city)

        print(data)


def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
