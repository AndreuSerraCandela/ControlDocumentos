# Document Scanner Frontend

Frontend React para escanear documentos utilizando el SDK de Facephi.

## Características

- 📱 Escaneo de documentos con cámara
- 🔍 Búsqueda de documentos por nacionalidad y DNI
- 👤 Visualización de imágenes faciales
- 📊 Estadísticas de documentos escaneados
- 🎨 Interfaz moderna y responsive

## Configuración

### Prerrequisitos

- Node.js (versión 16 o superior)
- npm o yarn
- API backend ejecutándose en http://localhost:8000

### Instalación

1. Instalar dependencias:
```bash
npm install
```

2. Configurar variables de entorno:
```bash
# Crear archivo .env en la raíz del proyecto
REACT_APP_API_URL=http://localhost:8000
REACT_APP_FACEPHI_API_KEY=4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS
REACT_APP_FACEPHI_BASE_URL=https://api.identity-platform.io
REACT_APP_FACEPHI_CLIENT_ID=52f5e18b-e599-4de3-91e1-f4b0e80ff657
REACT_APP_FACEPHI_SECRET_ID=82880bda-d8c4-448c-baf1-ecc650a3bc58
```

3. Ejecutar la aplicación:
```bash
npm start
```

La aplicación estará disponible en http://localhost:3000

## Uso

### Escanear Documento

1. Haz clic en "Iniciar Escaneo"
2. Permite el acceso a la cámara
3. Coloca el documento frente a la cámara
4. Haz clic en "Capturar Documento"
5. El documento se procesará automáticamente

### Buscar Documentos

1. Ve a la pestaña "Documentos Escaneados"
2. Usa los filtros de búsqueda:
   - Nacionalidad: Código de país (ej: ESP)
   - DNI: Número de documento
3. Haz clic en "Buscar"
4. Opcionalmente, activa "Mostrar Caras" para ver imágenes faciales

## Estructura del Proyecto

```
src/
├── components/
│   ├── DocumentScanner.js    # Componente de escaneo
│   └── DocumentResults.js    # Componente de resultados
├── services/
│   └── api.js               # Servicios de API
├── config/
│   └── facephi.js           # Configuración de Facephi
├── App.js                   # Componente principal
└── index.js                 # Punto de entrada
```

## Integración con Facephi

Este frontend está configurado para integrarse con el SDK de Facephi. Las credenciales están configuradas en `src/config/facephi.js`:

- **API Key**: 4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS
- **Client ID**: 52f5e18b-e599-4de3-91e1-f4b0e80ff657
- **Secret ID**: 82880bda-d8c4-448c-baf1-ecc650a3bc58

### Endpoints de Facephi

- `extractDocumentDataWeb`: Extracción de datos del documento
- `documentValidation/v2/start`: Inicio de validación
- `documentValidation/v2/data`: Datos de validación
- `documentValidation/v2/status`: Estado de validación
- `finishTracking`: Finalización del seguimiento

## Desarrollo

### Scripts Disponibles

- `npm start`: Ejecuta la aplicación en modo desarrollo
- `npm build`: Construye la aplicación para producción
- `npm test`: Ejecuta las pruebas
- `npm eject`: Expone la configuración de webpack

### Tecnologías Utilizadas

- React 18
- Styled Components
- Axios
- Facephi SDK Web
- HTML5 Camera API

## Notas Importantes

- La aplicación requiere acceso a la cámara del dispositivo
- Los documentos se procesan localmente antes de enviarse al backend
- Las imágenes faciales se almacenan en formato base64
- La validación de documentos se realiza usando el SDK de Facephi

## Solución de Problemas

### Error de Cámara
- Asegúrate de permitir el acceso a la cámara en el navegador
- Verifica que no haya otras aplicaciones usando la cámara

### Error de API
- Verifica que el backend esté ejecutándose en http://localhost:8000
- Revisa la consola del navegador para errores de red

### Error de SDK
- Verifica que las credenciales de Facephi sean correctas
- Asegúrate de tener una conexión a internet estable
