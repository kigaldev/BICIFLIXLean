document.addEventListener('DOMContentLoaded', function() {
    // Generar años dinámicamente
    const yearSelect = document.getElementById('year');
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= currentYear - 20; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    }

    // Selector de pasos del formulario
    const form = document.getElementById('tasacion-compra-form');
    const steps = form.querySelectorAll('.form-section');
    let currentStep = 0;

    // Botones de navegación
    const nextButtons = form.querySelectorAll('.next-step');
    const prevButtons = form.querySelectorAll('.prev-step');

    // Función para validar paso actual
    function validateStep(step) {
        const inputs = step.querySelectorAll('input, select');
        return Array.from(inputs).every(input => input.validity.valid);
    }

    // Botones Next
    nextButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            const currentStepElement = steps[currentStep];
            if (validateStep(currentStepElement)) {
                currentStepElement.style.display = 'none';
                currentStep++;
                steps[currentStep].style.display = 'block';
            } else {
                alert('Por favor, completa todos los campos requeridos');
            }
        });
    });

    // Botones Previous
    prevButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            steps[currentStep].style.display = 'none';
            currentStep--;
            steps[currentStep].style.display = 'block';
        });
    });

    // Manejo del submit
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Aquí implementaremos la lógica de envío de tasación
        alert('Tasación solicitada. Próximamente recibirás un informe detallado.');
    });
});