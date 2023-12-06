function updateData() {
    const firstUrl = 'http://192.168.117.204/';
    const backupUrl = 'http://192.168.117.211/';

    // Check the state of Max Values toggle switch
    const showMaxValues = document.getElementById('maxValuesToggle').checked;

    // Check the state of Mean Values toggle switch
    const showMeanValues = document.getElementById('meanValuesToggle').checked;

    // Function to fetch data from a given URL
    const fetchData = (url) => {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            });
    };

    // Ping function to check if a device is reachable
    const pingDevice = (url) => {
        return fetch(url, { method: 'HEAD' })
            .then(response => response.ok)
            .catch(() => false);
    };

    // Update Pico W 1 status
    pingDevice(firstUrl)
        .then(isReachable => {
            const picoW1Status = document.getElementById('PicoW1Status');
            if (isReachable) {
                picoW1Status.innerText = 'Up';
                picoW1Status.className = 'status-up';
            } else {
                picoW1Status.innerText = 'Down';
                picoW1Status.className = 'status-down';
            }
        });

    // Update Pico W 2 status
    pingDevice(backupUrl)
        .then(isReachable => {
            const picoW2Status = document.getElementById('PicoW2Status');
            if (isReachable) {
                picoW2Status.innerText = 'Up';
                picoW2Status.className = 'status-up';
            } else {
                picoW2Status.innerText = 'Down';
                picoW2Status.className = 'status-down';
            }
        });

    // Try fetching data from the first URL
    fetchData(firstUrl)
        .then(data => {
            // Update your HTML with data
            document.getElementById('temperature').innerText = data.temperature || 0;
            document.getElementById('humidity').innerText = data.humidity || 0;
            document.getElementById('pressure').innerText = data.pressure || 0;
            document.getElementById('gas').innerText = data.gas || 0;

            // Max Values
            if (showMaxValues) {
                document.getElementById('max_temperature').innerText = data.max_values.max_temperature || 0;
                document.getElementById('max_humidity').innerText = data.max_values.max_humidity || 0;
                document.getElementById('max_pressure').innerText = data.max_values.max_pressure || 0;
                document.getElementById('max_gas').innerText = data.max_values.max_gas || 0;
            } else {
                // Set default values to 0 or any desired default value without making a fetch request
                document.getElementById('max_temperature').innerText = 0;
                document.getElementById('max_humidity').innerText = 0;
                document.getElementById('max_pressure').innerText = 0;
                document.getElementById('max_gas').innerText = 0;
            }

            // Mean Values
            if (showMeanValues) {
                document.getElementById('mean_temperature').innerText = data.mean_values.mean_temperature || 0;
                document.getElementById('mean_humidity').innerText = data.mean_values.mean_humidity || 0;
                document.getElementById('mean_pressure').innerText = data.mean_values.mean_pressure || 0;
                document.getElementById('mean_gas').innerText = data.mean_values.mean_gas || 0;
            } else {
                // Set default values to 0 or any desired default value without making a fetch request
                document.getElementById('mean_temperature').innerText = 0;
                document.getElementById('mean_humidity').innerText = 0;
                document.getElementById('mean_pressure').innerText = 0;
                document.getElementById('mean_gas').innerText = 0;
            }
        })
        .catch(error => {
            console.error(`Error fetching data from ${firstUrl}:`, error);

            // If fetching from the first URL fails, try the backup URL
            fetchData(backupUrl)
                .then(data => {
                    // Update your HTML with data from the backup URL
                    document.getElementById('temperature').innerText = data.temperature || 0;
                    document.getElementById('humidity').innerText = data.humidity || 0;
                    document.getElementById('pressure').innerText = data.pressure || 0;
                    document.getElementById('gas').innerText = data.gas || 0;

                    // Max Values
                    if (showMaxValues) {
                        document.getElementById('max_temperature').innerText = data.max_values.max_temperature || 0;
                        document.getElementById('max_humidity').innerText = data.max_values.max_humidity || 0;
                        document.getElementById('max_pressure').innerText = data.max_values.max_pressure || 0;
                        document.getElementById('max_gas').innerText = data.max_values.max_gas || 0;
                    } else {
                        // Set default values to 0 or any desired default value without making a fetch request
                        document.getElementById('max_temperature').innerText = 0;
                        document.getElementById('max_humidity').innerText = 0;
                        document.getElementById('max_pressure').innerText = 0;
                        document.getElementById('max_gas').innerText = 0;
                    }

                    // Mean Values
                    if (showMeanValues) {
                        document.getElementById('mean_temperature').innerText = data.mean_values.mean_temperature || 0;
                        document.getElementById('mean_humidity').innerText = data.mean_values.mean_humidity || 0;
                        document.getElementById('mean_pressure').innerText = data.mean_values.mean_pressure || 0;
                        document.getElementById('mean_gas').innerText = data.mean_values.mean_gas || 0;
                    } else {
                        // Set default values to 0 or any desired default value without making a fetch request
                        document.getElementById('mean_temperature').innerText = 0;
                        document.getElementById('mean_humidity').innerText = 0;
                        document.getElementById('mean_pressure').innerText = 0;
                        document.getElementById('mean_gas').innerText = 0;
                    }
                })
                .catch(backupError => {
                    // Handle the error gracefully for the backup URL
                    console.error(`Error fetching data from ${backupUrl}:`, backupError);

                    // Set default values to 0
                    document.getElementById('temperature').innerText = 0;
                    document.getElementById('humidity').innerText = 0;
                    document.getElementById('pressure').innerText = 0;
                    document.getElementById('gas').innerText = 0;

                    document.getElementById('max_temperature').innerText = 0;
                    document.getElementById('max_humidity').innerText = 0;
                    document.getElementById('max_pressure').innerText = 0;
                    document.getElementById('max_gas').innerText = 0;

                    document.getElementById('mean_temperature').innerText = 0;
                    document.getElementById('mean_humidity').innerText = 0;
                    document.getElementById('mean_pressure').innerText = 0;
                    document.getElementById('mean_gas').innerText = 0;
                });
        });
}
