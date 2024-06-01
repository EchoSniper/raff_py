import machine
import utime

# Constants
ADCPIN = 4
ADC_RESOLUTION = 65535
VOLTAGE_REFERENCE = 3.3

# Initialize the ADC 
sensor = machine.ADC(ADCPIN)

# Function to read temperature from the sensor
def ReadTemperature():
    # Read the raw ADC value
    adc_value = sensor.read_u16()
    # Convert the raw ADC value to a voltage
    volt = (VOLTAGE_REFERENCE / ADC_RESOLUTION) * adc_value
    # Convert the voltage to temperature (in Celsius)
    temperature = 27 - (volt - 0.706) / 0.001721
    # Return the temperature rounded to one decimal place
    return round(temperature, 1)

# Main loop
while True:
    # Read the temperature
    temperature = ReadTemperature()

    # Get the current time
    timestamp = utime.localtime()

    # Format the timestamp for display
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}".format(
        timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4])

    # Print temperature and timestamp to the shell
    print("{} - Temperature: {} °C".format(timestamp_str, temperature))

    # Log temperature and timestamp to a file
    with open("temperature_log.csv", "a") as f:
        f.write("{},{}\n".format(timestamp_str, temperature))
