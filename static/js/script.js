// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.querySelector('.result-container');
    const predictionElement = document.querySelector('.prediction');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const company = document.getElementById('company').value;
        const car_model = document.getElementById('car_model').value;
        const year = document.getElementById('year').value;
        const fuel_type = document.getElementById('fuel_type').value;
        const kms_driven = document.getElementById('kms_driven').value;
        
        // Validate form
        if (!company || !car_model || !year || !fuel_type || !kms_driven) {
            alert('Please fill all the required fields');
            return;
        }
        
        // Prepare data for API
        const data = {
            company: company,
            car_model: car_model,
            year: year,
            fuel_type: fuel_type,
            kms_driven: kms_driven
        };
        
        // Send AJAX request
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display prediction
                resultContainer.style.display = 'block';
                predictionElement.textContent = data.formatted_prediction;
                
                // Scroll to result
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            } else {
                // Display error
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        });
    });
});
