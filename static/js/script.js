// Wine Quality Prediction App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const inputs = document.querySelectorAll('input[type="number"]');
    const submitBtn = document.querySelector('.predict-btn');
    
    // Input validation ranges for wine quality features
    const validationRules = {
        fixed_acidity: { min: 3.8, max: 15.9, label: 'Fixed Acidity' },
        volatile_acidity: { min: 0.08, max: 1.58, label: 'Volatile Acidity' },
        citric_acid: { min: 0.0, max: 1.66, label: 'Citric Acid' },
        residual_sugar: { min: 0.6, max: 65.8, label: 'Residual Sugar' },
        chlorides: { min: 0.009, max: 0.611, label: 'Chlorides' },
        free_sulfur_dioxide: { min: 1.0, max: 289.0, label: 'Free Sulfur Dioxide' },
        total_sulfur_dioxide: { min: 6.0, max: 440.0, label: 'Total Sulfur Dioxide' },
        density: { min: 0.98711, max: 1.03898, label: 'Density' },
        pH: { min: 2.72, max: 4.01, label: 'pH' },
        sulphates: { min: 0.22, max: 2.0, label: 'Sulphates' },
        alcohol: { min: 8.0, max: 15.0, label: 'Alcohol' }
    };

    // Add real-time validation to inputs
    inputs.forEach(input => {
        const fieldName = input.name;
        const rule = validationRules[fieldName];
        
        if (rule) {
            input.addEventListener('input', function() {
                validateField(input, rule);
            });
            
            input.addEventListener('blur', function() {
                validateField(input, rule);
            });
        }
    });

    // Form submission handling
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                showLoading();
                // Submit the form after a short delay to show loading
                setTimeout(() => {
                    form.submit();
                }, 500);
            }
        });
    }

    function validateField(input, rule) {
        const value = parseFloat(input.value);
        const errorElement = input.parentNode.querySelector('.error-message');
        
        if (input.value === '') {
            clearValidation(input, errorElement);
            return true;
        }
        
        if (isNaN(value) || value < rule.min || value > rule.max) {
            showFieldError(input, errorElement, `${rule.label} should be between ${rule.min} and ${rule.max}`);
            return false;
        } else {
            clearValidation(input, errorElement);
            return true;
        }
    }

    function showFieldError(input, errorElement, message) {
        input.classList.add('error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }
    }

    function clearValidation(input, errorElement) {
        input.classList.remove('error');
        if (errorElement) {
            errorElement.classList.remove('show');
        }
    }

    function validateForm() {
        let isValid = true;
        
        inputs.forEach(input => {
            const fieldName = input.name;
            const rule = validationRules[fieldName];
            
            if (rule && !validateField(input, rule)) {
                isValid = false;
            }
            
            if (input.hasAttribute('required') && input.value.trim() === '') {
                isValid = false;
                const errorElement = input.parentNode.querySelector('.error-message');
                showFieldError(input, errorElement, 'This field is required');
            }
        });
        
        return isValid;
    }

    function showLoading() {
        submitBtn.innerHTML = '<div class="spinner"></div> Predicting...';
        submitBtn.disabled = true;
    }

    // Add placeholder suggestions based on typical wine values (all within valid ranges)
    const placeholders = {
        fixed_acidity: '7.4',
        volatile_acidity: '0.70',
        citric_acid: '0.00',
        residual_sugar: '1.9',
        chlorides: '0.076',
        free_sulfur_dioxide: '11.0',
        total_sulfur_dioxide: '34.0',
        density: '0.99780',
        pH: '3.51',
        sulphates: '0.56',
        alcohol: '9.4'
    };

    // Alternative sample data sets for variety
    const sampleDataSets = [
        {
            fixed_acidity: '7.4',
            volatile_acidity: '0.70',
            citric_acid: '0.00',
            residual_sugar: '1.9',
            chlorides: '0.076',
            free_sulfur_dioxide: '11.0',
            total_sulfur_dioxide: '34.0',
            density: '0.99780',
            pH: '3.51',
            sulphates: '0.56',
            alcohol: '9.4'
        },
        {
            fixed_acidity: '8.1',
            volatile_acidity: '0.28',
            citric_acid: '0.40',
            residual_sugar: '6.9',
            chlorides: '0.050',
            free_sulfur_dioxide: '30.0',
            total_sulfur_dioxide: '97.0',
            density: '0.99510',
            pH: '3.26',
            sulphates: '0.44',
            alcohol: '10.1'
        },
        {
            fixed_acidity: '7.8',
            volatile_acidity: '0.88',
            citric_acid: '0.00',
            residual_sugar: '2.6',
            chlorides: '0.098',
            free_sulfur_dioxide: '25.0',
            total_sulfur_dioxide: '67.0',
            density: '0.99680',
            pH: '3.20',
            sulphates: '0.68',
            alcohol: '9.8'
        }
    ];

    let currentSampleIndex = 0;

    // Set placeholders
    inputs.forEach(input => {
        if (placeholders[input.name]) {
            input.placeholder = `e.g., ${placeholders[input.name]}`;
        }
    });

    // Add sample data functionality
    function fillSampleData() {
        const currentSample = sampleDataSets[currentSampleIndex];
        console.log('Filling sample data:', currentSample); // Debug log
        
        Object.keys(currentSample).forEach(key => {
            const input = document.querySelector(`input[name="${key}"]`);
            if (input) {
                input.value = currentSample[key];
                console.log(`Set ${key} to ${currentSample[key]}`); // Debug log
                
                // Clear any existing errors
                input.classList.remove('error');
                const errorElement = input.parentNode.querySelector('.error-message');
                if (errorElement) {
                    errorElement.classList.remove('show');
                }
                
                // Trigger validation
                const rule = validationRules[key];
                if (rule) {
                    const isValid = validateField(input, rule);
                    console.log(`Validation for ${key}: ${isValid}`); // Debug log
                }
                
                // Trigger change event for any listeners
                input.dispatchEvent(new Event('input'));
                input.dispatchEvent(new Event('change'));
            }
        });
        
        // Cycle through sample data sets
        currentSampleIndex = (currentSampleIndex + 1) % sampleDataSets.length;
        
        // Update button text to show which sample is next
        const sampleBtn = document.querySelector('.sample-btn');
        if (sampleBtn) {
            const nextIndex = currentSampleIndex;
            sampleBtn.innerHTML = `📋 Fill Sample Data ${nextIndex + 1}/${sampleDataSets.length}`;
        }
    }

    // Add sample data button
    const sampleBtn = document.createElement('button');
    sampleBtn.type = 'button';
    sampleBtn.className = 'sample-btn';
    sampleBtn.innerHTML = '📋 Fill Sample Data 1/3';
    sampleBtn.onclick = fillSampleData;
    sampleBtn.title = 'Click to fill form with sample wine data. Click multiple times for different samples.';
    
    const submitContainer = document.querySelector('.submit-container');
    if (submitContainer) {
        submitContainer.insertBefore(sampleBtn, submitBtn);
    }
});

// Quality interpretation function for results page
function getQualityDescription(score) {
    const quality = parseFloat(score);
    
    if (quality >= 7) {
        return { 
            description: 'Excellent Wine', 
            color: '#27ae60',
            emoji: '🍷✨'
        };
    } else if (quality >= 6) {
        return { 
            description: 'Good Wine', 
            color: '#2ecc71',
            emoji: '🍷👍'
        };
    } else if (quality >= 5) {
        return { 
            description: 'Average Wine', 
            color: '#f39c12',
            emoji: '🍷👌'
        };
    } else {
        return { 
            description: 'Below Average Wine', 
            color: '#e74c3c',
            emoji: '🍷⚠️'
        };
    }
}
