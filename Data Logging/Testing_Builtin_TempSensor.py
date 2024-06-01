import machine
import time


# Constants
ADCPIN = 4
ADC_RESOLUTION = 65535
VOLTAGE_REFERENCE = 3.3

# Initialize the ADC on the specified pin
sensor = machine.ADC(ADCPIN)

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
        time.sleep(2)
        # Print the temperature
        print("The Temperature is:", temperature)
