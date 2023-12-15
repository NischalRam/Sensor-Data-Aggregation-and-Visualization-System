from GetdatafromSensor import api_response, history_stack 
import ujson

def validate_readings(temp, hum, pres, gas):
    """
    Validate temperature, humidity, pressure, and gas readings.
    Adjust the range values based on your specific environment.
    """
    temp_min, temp_max = -20, 100  # Adjust these values based on your environment
    hum_min, hum_max = 0, 100    # Adjust these values based on your environment
    pres_min, pres_max = 800, 1200  # Adjust these values based on your environment
    gas_min, gas_max = 0, 100     # Adjust these values based on your environment

    # Validate temperature
    if not temp_min <= temp <= temp_max:
        raise ValueError(f"Temperature out of range: {temp}")

    # Validate humidity
    if not hum_min <= hum <= hum_max:
        raise ValueError(f"Humidity out of range: {hum}")

    # Validate pressure
    if not pres_min <= pres <= pres_max:
        raise ValueError(f"Pressure out of range: {pres}")

    # Validate gas
    if not gas_min <= gas <= gas_max:
        raise ValueError(f"Gas reading out of range: {gas}")





# Test case for api_response function
def test_api_response():
    # Define sample data
    temp = 25.5
    hum = 50.0
    pres = 1013.25
    gas = 450.75
    max_temp = 30.0
    max_hum = 60.0
    max_pres = 1020.0
    max_gas = 500.0
    mean_temp = 26.0
    mean_hum = 55.0
    mean_pres = 1015.0
    mean_gas = 480.0

    # Expected JSON output
    expected_json = ujson.dumps({
        "temperature": temp,
        "humidity": hum,
        "pressure": pres,
        "gas": gas,
        "max_values": {
            "max_temperature": max_temp,
            "max_humidity": max_hum,
            "max_pressure": max_pres,
            "max_gas": max_gas,
        },
        "mean_values": {
            "mean_temperature": mean_temp,
            "mean_humidity": mean_hum,
            "mean_pressure": mean_pres,
            "mean_gas": mean_gas,
        }
    })

    # Call the api_response function
    actual_json = api_response(temp, hum, pres, gas, max_temp, max_hum, max_pres, max_gas, mean_temp, mean_hum, mean_pres, mean_gas)

    # Compare actual and expected JSON
    assert actual_json == expected_json, f"Test Failed. Expected: {expected_json}, Actual: {actual_json}"

    print("Test Passed!")


def test_history_stack_management():
    # Ensure the history stack is initially empty
    assert len(history_stack) == 0, "History stack should be empty initially"

    # Add entries to the history stack
    for _ in range(40):  # Add more entries than the limit (30) to test stack size limitation
        # Simulate sensor readings (replace these values with actual sensor data)
        temp, hum, pres, gas = 25.0, 50.0, 1013.25, 400.0
        temp_history = {'temperature': temp, 'humidity': hum, 'pressure': pres, 'gas': gas}
        history_stack.append(temp_history)

    # Ensure the history stack size is limited to the last 30 entries
    assert len(history_stack) == 30, "History stack size should be limited to the last 30 entries"

    # Calculate and test maximum values based on the stack
    max_temp = max(entry['temperature'] for entry in history_stack)
    max_hum = max(entry['humidity'] for entry in history_stack)
    max_pres = max(entry['pressure'] for entry in history_stack)
    max_gas = max(entry['gas'] for entry in history_stack)

    # Replace these values with expected maximum values based on your simulated data
    expected_max_temp = 25.0
    expected_max_hum = 50.0
    expected_max_pres = 1013.25
    expected_max_gas = 400.0

    assert max_temp == expected_max_temp, f"Unexpected maximum temperature: {max_temp}"
    assert max_hum == expected_max_hum, f"Unexpected maximum humidity: {max_hum}"
    assert max_pres == expected_max_pres, f"Unexpected maximum pressure: {max_pres}"
    assert max_gas == expected_max_gas, f"Unexpected maximum gas: {max_gas}"

    # Calculate and test mean values based on the stack
    mean_temp = sum(entry['temperature'] for entry in history_stack) / len(history_stack)
    mean_hum = sum(entry['humidity'] for entry in history_stack) / len(history_stack)
    mean_pres = sum(entry['pressure'] for entry in history_stack) / len(history_stack)
    mean_gas = sum(entry['gas'] for entry in history_stack) / len(history_stack)

    # Replace these values with expected mean values based on your simulated data
    expected_mean_temp = 25.0
    expected_mean_hum = 50.0
    expected_mean_pres = 1013.25
    expected_mean_gas = 400.0

    assert mean_temp == expected_mean_temp, f"Unexpected mean temperature: {mean_temp}"
    assert mean_hum == expected_mean_hum, f"Unexpected mean humidity: {mean_hum}"
    assert mean_pres == expected_mean_pres, f"Unexpected mean pressure: {mean_pres}"
    assert mean_gas == expected_mean_gas, f"Unexpected mean gas: {mean_gas}"

    print("Test passed: History stack management is correct")

# Run the test
test_history_stack_management()
test_api_response()
validate_readings(data)
