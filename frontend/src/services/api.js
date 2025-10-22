import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Servicio para escanear un documento
export const scanDocument = async (documentData) => {
  try {
    const response = await api.post('/check-document', documentData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al escanear el documento');
  }
};

// Servicio para cargar todos los documentos
export const loadDocuments = async () => {
  try {
    const response = await api.get('/documents');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al cargar documentos');
  }
};

// Servicio para buscar documentos
export const searchDocuments = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.nationality) params.append('nationality', filters.nationality);
    if (filters.dni) params.append('dni', filters.dni);
    
    const response = await api.get(`/documents/search?${params.toString()}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al buscar documentos');
  }
};

// Servicio para obtener documentos con imagen facial
export const getDocumentsWithFace = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.nationality) params.append('nationality', filters.nationality);
    if (filters.dni) params.append('dni', filters.dni);
    
    const response = await api.get(`/documents/with-face?${params.toString()}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al obtener documentos con imagen facial');
  }
};

// Servicio para cargar documentos masivamente
export const loadDocumentsBatch = async (documents) => {
  try {
    const response = await api.post('/documents/load', { documents });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al cargar documentos');
  }
};

export default api;
