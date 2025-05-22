let countdownInterval;
let verificationHistory = [];

// Función para iniciar el proceso de verificación
function startVerification() {
    document.getElementById('status-message').textContent = 'Leyendo documento...';
    document.getElementById('countdown').classList.remove('hidden');
    document.getElementById('result-container').classList.add('hidden');
    document.getElementById('alert-container').classList.add('hidden');
    document.getElementById('verify-button').classList.add('hidden');

    let timeLeft = 60;
    const timerElement = document.getElementById('timer');
    
    countdownInterval = setInterval(() => {
        timeLeft--;
        timerElement.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            document.getElementById('status-message').textContent = 'Tiempo agotado. Por favor, intente de nuevo.';
            document.getElementById('verify-button').classList.remove('hidden');
        }
    }, 1000);

    // Iniciar la escucha de resultados
    startResultListener();
}

// Función para escuchar los resultados
function startResultListener() {
    const eventSource = new EventSource('/check-document/stream');
    
    eventSource.onmessage = function(event) {
        const result = JSON.parse(event.data);
        clearInterval(countdownInterval);
        document.getElementById('countdown').classList.add('hidden');
        displayResult(result);
        eventSource.close();
    };

    eventSource.onerror = function() {
        eventSource.close();
    };
}

// Función para detectar si es un dispositivo móvil
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Función para reproducir sonido de alerta
function playAlertSound() {
    const audio = new Audio('/static/alert.mp3');
    audio.play().catch(e => console.log('Error al reproducir sonido:', e));
}

// Función para hacer vibrar el dispositivo (solo en móviles)
function vibrateDevice() {
    if (navigator.vibrate) {
        navigator.vibrate([200, 100, 200, 100, 200]);
    }
}

// Función para mostrar el resultado
function displayResult(result) {
    document.getElementById('result-container').classList.remove('hidden');
    document.getElementById('verify-button').classList.remove('hidden');

    const now = new Date();
    const timeString = now.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    // Extraer nombre y apellidos del documento
    const name = result.documentData?.resultJSON?.DocumentData?.serviceDocument?.FRONTSIDE?.FIELD_DATA?.GIVEN_NAMES || '';
    const surname = result.documentData?.resultJSON?.DocumentData?.serviceDocument?.FRONTSIDE?.FIELD_DATA?.SURNAME?.join(' ') || '';

    document.getElementById('dni-value').textContent = result.documentData?.dni || 'No disponible';
    document.getElementById('name-value').textContent = `${name} ${surname}`.trim() || 'No disponible';
    document.getElementById('time-value').textContent = timeString;
    document.getElementById('status-value').textContent = result.blocked ? 'No autorizado' : 'Autorizado';

    if (result.blocked) {
        document.getElementById('alert-container').classList.remove('hidden');
        
        // Activar notificaciones según el dispositivo
        if (isMobileDevice()) {
            vibrateDevice();
            playAlertSound();
        } else {
            playAlertSound();
            // Efecto visual para PC
            document.getElementById('alert-container').style.animation = 'pulse 1s infinite';
        }
    }

    // Añadir al historial
    addToHistory(result.documentData?.dni || '', `${name} ${surname}`.trim(), timeString, result.blocked);
}

// Función para añadir una verificación al historial
function addToHistory(dni, fullName, time, blocked) {
    const [name, ...surnames] = fullName.split(' ');
    const now = new Date();
    const dateStr = now.toLocaleDateString('es-ES');
    
    const historyItem = {
        nombre: name || 'No disponible',
        apellidos: surnames.join(' ') || 'No disponible',
        dni: dni || 'No disponible',
        fechaEntrada: dateStr,
        horaEntrada: time,
        fechaSalida: dateStr,
        horaSalida: '18:00',
        militar: 'No',
        civil: 'Sí',
        nacionalidad: 'España',
        motivoVisita: 'Visita Base Naval'
    };

    verificationHistory.unshift(historyItem);
    updateHistoryDisplay();
}

// Función para actualizar la visualización del historial
function updateHistoryDisplay() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';

    verificationHistory.forEach(item => {
        const row = document.createElement('tr');
        
        // Añadir cada celda
        const cells = [
            item.nombre,
            item.apellidos,
            item.dni,
            item.fechaEntrada,
            item.horaEntrada,
            item.fechaSalida,
            item.horaSalida,
            item.militar,
            item.civil,
            item.nacionalidad,
            item.motivoVisita
        ];

        cells.forEach((cellText, index) => {
            const td = document.createElement('td');
            td.textContent = cellText;
            
            // Añadir clases especiales para militar y civil
            if (index === 7) { // Militar
                td.className = cellText === 'Sí' ? 'military-yes' : 'military-no';
            }
            if (index === 8) { // Civil
                td.className = cellText === 'Sí' ? 'civil-yes' : 'civil-no';
            }
            
            row.appendChild(td);
        });

        historyList.appendChild(row);
    });
}

// Función para manejar la selección de archivos
function handleFileSelect() {
    const fileInput = document.getElementById('excel-file');
    const uploadButton = document.getElementById('upload-button');
    const selectFileButton = document.getElementById('select-file-button');
    const fileNameDisplay = document.getElementById('file-name');
    
    if (fileInput && uploadButton && selectFileButton) {
        // Al hacer clic en el botón de seleccionar archivo
        selectFileButton.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Cuando se selecciona un archivo
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                fileNameDisplay.textContent = fileName;
                uploadButton.disabled = false;
            } else {
                fileNameDisplay.textContent = 'Ningún archivo seleccionado';
                uploadButton.disabled = true;
            }
        });
        
        // Al hacer clic en el botón de subir
        uploadButton.addEventListener('click', function() {
            if (fileInput.files.length > 0) {
                const form = document.getElementById('upload-form');
                if (form) {
                    submitForm(form);
                }
            }
        });
    }
}

// Función de envío del formulario
function submitForm(form) {
    const fileInput = document.getElementById('excel-file');
    const uploadButton = document.getElementById('upload-button');
    const fileNameDisplay = document.getElementById('file-name');
    const statusElement = document.getElementById('upload-status');
    
    if (!fileInput.files.length) {
        return;
    }
    
    const originalButtonText = uploadButton.textContent;
    uploadButton.textContent = 'Procesando...';
    uploadButton.disabled = true;
    
    // Mostrar estado de carga
    showUploadStatus('Subiendo archivo...', 'info');
    
    // Crear overlay de carga
    showLoadingOverlay(true, 'Procesando archivo...');
    
    // Enviar el formulario usando formData y fetch
    const formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta:', data);
        
        // Mostrar mensaje de éxito con detalles
        const message = `¡Lista actualizada correctamente!
                         <br>Registros nuevos: <strong>${data.new_records}</strong>
                         <br>Registros actualizados: <strong>${data.updated_records}</strong>
                         <br>Total de registros: <strong>${data.total_records}</strong>`;
        
        // Mostrar notificación con un botón para ir a la pantalla principal
        showSuccessNotification(message, () => {
            // Ocultar todo relacionado con la carga
            hideAdminSection();
        });
        
        // Ocultar overlay de carga
        showLoadingOverlay(false);
        
        // Limpiar el formulario
        fileInput.value = '';
        fileNameDisplay.textContent = 'Ningún archivo seleccionado';
        uploadButton.textContent = originalButtonText;
        uploadButton.disabled = true;
    })
    .catch(error => {
        console.error('Error:', error);
        showUploadStatus(`Error: ${error.message}`, 'error');
        showLoadingOverlay(false);
        uploadButton.textContent = originalButtonText;
        uploadButton.disabled = fileInput.files.length === 0;
    });
}

// Función para mostrar un overlay durante la carga
function showLoadingOverlay(show, message = 'Cargando...') {
    let overlay = document.getElementById('loading-overlay');
    
    if (show) {
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.innerHTML = `
                <div class="loading-content">
                    <div class="spinner"></div>
                    <div class="loading-message">${message}</div>
                </div>
            `;
            document.body.appendChild(overlay);
        } else {
            overlay.querySelector('.loading-message').textContent = message;
            overlay.style.display = 'flex';
        }
    } else if (overlay) {
        overlay.style.display = 'none';
    }
}

// Función para mostrar notificación de éxito con acción
function showSuccessNotification(message, callback) {
    let notification = document.getElementById('success-notification');
    
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'success-notification';
        document.body.appendChild(notification);
    }
    
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">✓</div>
            <div class="notification-message">${message}</div>
            <button class="notification-button">Aceptar</button>
        </div>
    `;
    
    notification.style.display = 'flex';
    
    // Agregar evento al botón
    const button = notification.querySelector('.notification-button');
    button.addEventListener('click', () => {
        notification.style.display = 'none';
        if (typeof callback === 'function') {
            callback();
        }
    });
    
    // Auto cerrar después de 5 segundos
    setTimeout(() => {
        if (notification.style.display !== 'none') {
            notification.style.display = 'none';
            if (typeof callback === 'function') {
                callback();
            }
        }
    }, 5000);
}

// Ocultar la sección de administración y mostrar la lista de registros
function hideAdminSection() {
    const adminSection = document.querySelector('.admin-section');
    if (adminSection) {
        adminSection.style.display = 'none';
    }
    
    // Mostrar la sección de historial
    const historyContainer = document.querySelector('.history-container');
    if (historyContainer) {
        historyContainer.scrollIntoView({ behavior: 'smooth' });
    }
}

// Función para mostrar el estado de la carga
function showUploadStatus(message, type) {
    console.log('Estado de carga:', message, type);
    
    const statusElement = document.getElementById('upload-status');
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.classList.remove('hidden', 'success', 'error', 'info');
        
        if (type) {
            statusElement.classList.add(type);
        }
        
        // Hacer scroll hasta el mensaje
        statusElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Evento DOMContentLoaded para configurar todo
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM cargado, configurando event listeners');
    
    // Configurar mensaje de verificación
    document.getElementById('status-message').textContent = 'Presione el botón para iniciar la verificación';
    document.getElementById('verify-button').classList.remove('hidden');
    
    // Evento para el botón de verificación
    document.getElementById('verify-button').addEventListener('click', () => {
        console.log('Botón de verificación pulsado');
        startVerification();
    });
    
    // Configurar selector de archivos y envío de formulario
    handleFileSelect();
}); 