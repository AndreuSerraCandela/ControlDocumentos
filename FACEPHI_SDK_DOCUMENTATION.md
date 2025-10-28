# Sistema Facephi Completo - Documentación

## 🔧 Configuración del SDK WebComponents

### 1. Credenciales de Artifactory
El archivo `.npmrc` está configurado con las credenciales de producción:

```bash
# Facephi registry credentials (prod)
@facephi:registry=https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:_password=Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllWcHZNMmw2YzJOdVRESnljVUp2UVZoRFluSlBWRXhYWWxobQ==
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:username=maybecloudes01
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:email=maybecloudes01@facephi.com
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:always-auth=true
```

### 2. API Keys Configuradas
- **Frontend SDK**: `4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS`
- **Backend SDK**: `kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU`
- **URL Frontend**: `https://documentos.malla.es`
- **URL Backend**: `https://api.identity-platform.io`

### 3. Instalación de Dependencias
```bash
# Instalar dependencias del SDK
npm install

# O usar otros gestores de paquetes
yarn install
bun install
```

### 4. Desarrollo
```bash
# Servidor de desarrollo
npm run dev

# Construir para producción
npm run build
```

## 🚀 Uso del Sistema

### Acceso
1. Ve a `http://127.0.0.1:8002`
2. Selecciona "Sistema Facephi Completo"
3. El sistema detectará automáticamente si el SDK está disponible

### Funcionalidades
- **🔍 Detección Automática**: Detecta si el SDK WebComponents está cargado
- **📷 Captura de Documentos**: Acceso a cámara optimizado para móviles
- **⚡ Procesamiento Dual**: Frontend y backend de Facephi trabajando juntos
- **📊 Resultados Detallados**: Visualización completa de datos extraídos
- **🛡️ Validación Completa**: Verificación de autenticidad y consistencia

### Modos de Funcionamiento
1. **Modo SDK Real**: Cuando el SDK WebComponents está disponible
2. **Modo Simulado**: Cuando el SDK no está disponible (para desarrollo/testing)

## 🔧 Configuración Avanzada

### Variables de Entorno
Para configurar las API keys en un proyecto Node.js:

```bash
# .env
VITE_FACEPHI_API_KEY=4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS
VITE_FACEPHI_BASE_URL=https://documentos.malla.es
VITE_BACKEND_API_KEY=kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU
VITE_BACKEND_BASE_URL=https://api.identity-platform.io
```

### WebComponents
El sistema carga automáticamente el SDK desde:
```html
<script type="module" src="https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/@facephi/sdk-web-fphi/dist/facephi-sdk.js"></script>
```

## 📋 Credenciales de Artifactory

### Usuario 1
- **Username**: `maybecloudes01`
- **Token Short**: `cmVmdGtuOjAxOjAwMDAwMDAwMDA6YVpvM2l6c2NuTDJycUJvQVhDYnJPVExXYlhm`
- **Token B64**: `Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllWcHZNMmw2YzJOdVRESnljVUp2UVZoRFluSlBWRXhYWWxobQ==`

### Usuario 2
- **Username**: `maybecloudes02`
- **Token Short**: `cmVmdGtuOjAxOjAwMDAwMDAwMDA6YUJsVGxkNlpEZXhIa01RRDRINzRZUkJVcjNv`
- **Token B64**: `Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllVSnNWR3hrTmxwRVpYaElhMDFSUkRSSU56UlpVa0pWY2pOdg==`

## 🐛 Troubleshooting

### SDK No Disponible
Si el SDK WebComponents no se carga:
1. Verifica las credenciales en `.npmrc`
2. Comprueba la conectividad con Artifactory
3. El sistema funcionará en modo simulado

### Errores de Cámara
1. Asegúrate de permitir el acceso a la cámara
2. Usa HTTPS en producción
3. Verifica que el navegador soporte getUserMedia

### Problemas de API
1. Verifica que las API keys sean correctas
2. Comprueba la conectividad con los endpoints
3. Revisa los logs de la consola del navegador

## 📚 Referencias
- [SDK Web WebComponents Documentation](https://github.com/facephi/sdk-web-examples/tree/master/examples/javascript/sdk-onboarding)
- [Facephi Identity Platform](https://api.identity-platform.io)
- [Artifactory Registry](https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/)
