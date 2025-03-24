# Gym Reservation Project

This project automates the process of reserving a gym slot using a web interface. It utilizes Selenium for browser automation and requires a configuration file for user credentials and desired reservation details.

## Project Structure

```
gym-reservation
├── main.py               # Main entry point of the application
├── make_reservation.py   # Contains the logic for making reservations
└── README.md             # Documentation for the project
```

## Requirements

- Python 3.x
- Selenium
- A compatible web driver (e.g., ChromeDriver for Google Chrome)

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd gym-reservation
   ```

2. **Install dependencies**:
   Make sure you have the required packages installed. You can use pip to install Selenium:
   ```
   pip install selenium
   ```

3. **Configure the application**:
   Create a `config.json` file in the project directory with the following structure:
   ```json
   {
       "browser_path": "path/to/your/browser",
       "webdriver_path": "path/to/your/webdriver",
       "username": "your_username",
       "password": "your_password",
       "desired_time_slot": "desired_time_slot",
       "phone_number": "your_phone_number"
   }
   ```

4. **Run the application**:
   Execute the `main.py` file to start the reservation process:
   ```
   python main.py
   ```

## Usage

- The application will log in to the gym's reservation system using the credentials provided in the `config.json` file.
- It will then attempt to make a reservation for the specified time slot.
- If successful, a confirmation message will be displayed.

## Notes

- Ensure that the web driver is compatible with the version of the browser you are using.
- Adjust the desired time slot in the `config.json` file as needed.
- The application may require adjustments based on changes to the gym's reservation website.