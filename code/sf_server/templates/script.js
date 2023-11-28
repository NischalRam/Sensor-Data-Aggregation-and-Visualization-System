function updateData() {
    fetch('http://192.168.4.1')
        .then(response => {
            // Check if the response status is OK (status code 200)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update your HTML with data
            document.getElementById('temperature').innerText = data.temperature || 0;
            document.getElementById('humidity').innerText = data.humidity || 0;
            document.getElementById('pressure').innerText = data.pressure || 0;
            document.getElementById('gas').innerText = data.gas || 0;

            // Max Values
            document.getElementById('max_temperature').innerText = data.max_values.max_temperature || 0;
            document.getElementById('max_humidity').innerText = data.max_values.max_humidity || 0;
            document.getElementById('max_pressure').innerText = data.max_values.max_pressure || 0;
            document.getElementById('max_gas').innerText = data.max_values.max_gas || 0;

            // Mean Values
            document.getElementById('mean_temperature').innerText = data.mean_values.mean_temperature || 0;
            document.getElementById('mean_humidity').innerText = data.mean_values.mean_humidity || 0;
            document.getElementById('mean_pressure').innerText = data.mean_values.mean_pressure || 0;
            document.getElementById('mean_gas').innerText = data.mean_values.mean_gas || 0;
        })
        .catch(error => {
            // Handle the error gracefully
            console.error('Error fetching data:', error);

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
}
