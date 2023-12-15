function updateData() {
    fetch('http://192.168.4.1')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').innerText = data.temperature || 'N/A';
            document.getElementById('humidity').innerText = data.humidity || 'N/A';
            document.getElementById('pressure').innerText = data.pressure || 'N/A';
            document.getElementById('gas').innerText = data.gas || 'N/A';

            // Max Values
            document.getElementById('max_temperature').innerText = data.max_values.max_temperature || 'N/A';
            document.getElementById('max_humidity').innerText = data.max_values.max_humidity || 'N/A';
            document.getElementById('max_pressure').innerText = data.max_values.max_pressure || 'N/A';
            document.getElementById('max_gas').innerText = data.max_values.max_gas || 'N/A';

            // Mean Values
            document.getElementById('mean_temperature').innerText = data.mean_values.mean_temperature || 'N/A';
            document.getElementById('mean_humidity').innerText = data.mean_values.mean_humidity || 'N/A';
            document.getElementById('mean_pressure').innerText = data.mean_values.mean_pressure || 'N/A';
            document.getElementById('mean_gas').innerText = data.mean_values.mean_gas || 'N/A';
        })
        .catch(error => console.error('Error fetching data:', error));
}