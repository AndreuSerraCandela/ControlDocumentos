// Configuración de Facephi SDK
export const facephiConfig = {
  // SDK FRONTEND - Nuevas credenciales para el frontend
  frontend: {
    apiKey: '4WpTfNAjrN7O0DSIas53zOfY26QF61rsnA67rUnS',
    baseUrl: 'https://documentos.malla.es'
  },
  
  // SDK BACKEND - Credenciales originales del backend (NO TOCAR)
  backend: {
    apiKey: 'kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU',
    baseUrl: 'https://api.identity-platform.io',
    clientId: '52f5e18b-e599-4de3-91e1-f4b0e80ff657',
    secretId: '82880bda-d8c4-448c-baf1-ecc650a3bc58'
  },
  
  // Credenciales de Artifactory para acceso a recursos
  artifactory: {
    user1: {
      username: 'maybecloudes01',
      tokenShort: 'cmVmdGtuOjAxOjAwMDAwMDAwMDA6YVpvM2l6c2NuTDJycUJvQVhDYnJPVExXYlhm',
      tokenB64: 'Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllWcHZNMmw2YzJOdVRESnljVUp2UVZoRFluSlBWRXhYWWxobQ=='
    },
    user2: {
      username: 'maybecloudes02',
      tokenShort: 'cmVmdGtuOjAxOjAwMDAwMDAwMDA6YUJsVGxkNlpEZXhIa01RRDRINzRZUkJVcjNv',
      tokenB64: 'Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllVSnNWR3hrTmxwRVpYaElhMDFSUkRSSU56UlpVa0pWY2pOdg=='
    }
  },
  
  endpoints: {
    // Endpoints del backend (originales)
    extractDocumentData: 'https://api.identity-platform.io/services/extractDocumentDataWeb',
    documentValidation: 'https://api.identity-platform.io/verify/documentValidation/v2/data',
    documentValidationStart: 'https://api.identity-platform.io/verify/documentValidation/v2/start',
    documentValidationStatus: 'https://api.identity-platform.io/verify/documentValidation/v2/status',
    finishTracking: 'https://api.identity-platform.io/services/finishTracking',
    
    // Endpoints del frontend (nuevos)
    sdkOnboarding: 'https://documentos.malla.es/sdk-onboarding',
    documentCapture: 'https://documentos.malla.es/capture',
    documentVerification: 'https://documentos.malla.es/verify'
  }
};

// Configuración de la API backend
export const apiConfig = {
  baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000'
};
