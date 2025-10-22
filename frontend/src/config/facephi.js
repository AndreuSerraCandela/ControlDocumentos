// Configuración de Facephi SDK
export const facephiConfig = {
  apiKey: 'kpl4u8fgxZSqD7LUQva5Myr0G7ab95a8MVO9rBlU',
  baseUrl: 'https://api.identity-platform.io',
  clientId: '52f5e18b-e599-4de3-91e1-f4b0e80ff657',
  secretId: '82880bda-d8c4-448c-baf1-ecc650a3bc58',
  endpoints: {
    extractDocumentData: 'https://api.identity-platform.io/services/extractDocumentDataWeb',
    documentValidation: 'https://api.identity-platform.io/verify/documentValidation/v2/data',
    documentValidationStart: 'https://api.identity-platform.io/verify/documentValidation/v2/start',
    documentValidationStatus: 'https://api.identity-platform.io/verify/documentValidation/v2/status',
    finishTracking: 'https://api.identity-platform.io/services/finishTracking'
  }
};

// Configuración de la API backend
export const apiConfig = {
  baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000'
};
