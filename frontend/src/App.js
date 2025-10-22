import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import DocumentScanner from './components/DocumentScanner';
import DocumentResults from './components/DocumentResults';
import { scanDocument, loadDocuments } from './services/api';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 40px;
  color: white;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin: 10px 0 0 0;
  opacity: 0.9;
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
`;

const TabContainer = styled.div`
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
`;

const Tab = styled.button`
  flex: 1;
  padding: 20px;
  border: none;
  background: ${props => props.active ? 'white' : 'transparent'};
  color: ${props => props.active ? '#667eea' : '#6c757d'};
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 3px solid ${props => props.active ? '#667eea' : 'transparent'};

  &:hover {
    background: ${props => props.active ? 'white' : '#e9ecef'};
  }
`;

const TabContent = styled.div`
  padding: 40px;
  min-height: 600px;
`;

function App() {
  const [activeTab, setActiveTab] = useState('scanner');
  const [scannedDocuments, setScannedDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDocumentScanned = async (documentData) => {
    setLoading(true);
    setError(null);
    
    try {
      // Enviar documento escaneado a la API backend
      const response = await scanDocument(documentData);
      
      if (response.exists) {
        setError('Este documento ya existe en la base de datos');
      } else {
        setScannedDocuments(prev => [documentData, ...prev]);
        setError(null);
      }
    } catch (err) {
      setError('Error al procesar el documento: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadDocuments = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await loadDocuments();
      setScannedDocuments(response.documents || []);
    } catch (err) {
      setError('Error al cargar documentos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Cargar documentos existentes al iniciar la aplicación
    handleLoadDocuments();
  }, []);

  return (
    <AppContainer>
      <Header>
        <Title>Document Scanner</Title>
        <Subtitle>Escanea documentos con tecnología Facephi</Subtitle>
      </Header>
      
      <MainContent>
        <TabContainer>
          <Tab 
            active={activeTab === 'scanner'} 
            onClick={() => setActiveTab('scanner')}
          >
            📱 Escanear Documento
          </Tab>
          <Tab 
            active={activeTab === 'results'} 
            onClick={() => setActiveTab('results')}
          >
            📋 Documentos Escaneados
          </Tab>
        </TabContainer>
        
        <TabContent>
          {activeTab === 'scanner' && (
            <DocumentScanner 
              onDocumentScanned={handleDocumentScanned}
              loading={loading}
              error={error}
            />
          )}
          
          {activeTab === 'results' && (
            <DocumentResults 
              documents={scannedDocuments}
              loading={loading}
              error={error}
              onRefresh={handleLoadDocuments}
            />
          )}
        </TabContent>
      </MainContent>
    </AppContainer>
  );
}

export default App;
