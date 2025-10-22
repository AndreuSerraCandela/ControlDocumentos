import React, { useState } from 'react';
import styled from 'styled-components';
import { searchDocuments, getDocumentsWithFace } from '../services/api';

const ResultsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const SearchContainer = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
`;

const SearchForm = styled.form`
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
`;

const SearchInput = styled.input`
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  flex: 1;
  min-width: 200px;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const SearchButton = styled.button`
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #5a6fd8;
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const RefreshButton = styled.button`
  background: #28a745;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #218838;
    transform: translateY(-1px);
  }
`;

const DocumentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
`;

const DocumentCard = styled.div`
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  }
`;

const DocumentHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e9ecef;
`;

const DocumentTitle = styled.h3`
  margin: 0;
  color: #333;
  font-size: 1.2rem;
`;

const DocumentStatus = styled.span`
  background: ${props => props.valid ? '#d4edda' : '#f8d7da'};
  color: ${props => props.valid ? '#155724' : '#721c24'};
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
`;

const DocumentInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const InfoRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const InfoLabel = styled.span`
  font-weight: 600;
  color: #666;
`;

const InfoValue = styled.span`
  color: #333;
  text-align: right;
  word-break: break-word;
`;

const FaceImage = styled.img`
  width: 100%;
  max-width: 150px;
  height: auto;
  border-radius: 10px;
  margin-top: 15px;
  border: 2px solid #e9ecef;
`;

const LoadingMessage = styled.div`
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
`;

const ErrorMessage = styled.div`
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
`;

const EmptyMessage = styled.div`
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 1.2rem;
`;

const StatsContainer = styled.div`
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
  text-align: center;
`;

const StatsTitle = styled.h2`
  margin: 0 0 10px 0;
  font-size: 1.5rem;
`;

const StatsNumber = styled.div`
  font-size: 2rem;
  font-weight: bold;
  margin: 10px 0;
`;

const DocumentResults = ({ documents, loading, error, onRefresh }) => {
  const [searchFilters, setSearchFilters] = useState({
    nationality: '',
    dni: ''
  });
  const [searchResults, setSearchResults] = useState([]);
  const [showFaceImages, setShowFaceImages] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setIsSearching(true);
    
    try {
      const filters = {};
      if (searchFilters.nationality) filters.nationality = searchFilters.nationality;
      if (searchFilters.dni) filters.dni = searchFilters.dni;
      
      const response = showFaceImages 
        ? await getDocumentsWithFace(filters)
        : await searchDocuments(filters);
      
      setSearchResults(response.documents || []);
    } catch (err) {
      console.error('Error en búsqueda:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const extractDocumentInfo = (doc) => {
    try {
      const frontside = doc.resultJSON?.DocumentData?.serviceDocument?.FRONTSIDE?.FIELD_DATA;
      const backside = doc.resultJSON?.DocumentData?.serviceDocument?.BACKSIDE?.MRZ_DATA;
      const checks = doc.resultJSON?.DocumentData?.serviceDocument?.CHECKS;
      const face = doc.resultJSON?.DocumentData?.serviceDocument?.DECOMPOSED?.FACE;
      
      return {
        dni: doc.dni,
        name: frontside?.GIVEN_NAMES || backside?.NAME || '',
        surname: frontside?.SURNAME?.join(' ') || backside?.SURNAME || '',
        nationality: frontside?.NATIONALITY_CODE || backside?.NATIONALITY || '',
        documentNumber: frontside?.DOCUMENT_NUMBER || backside?.IDENTITY_NUMBER || '',
        birthDate: frontside?.DATE_OF_BIRTH || backside?.BIRTH_DATE || '',
        expiryDate: frontside?.DATE_OF_EXPIRY || backside?.EXPIRATION_DATE || '',
        sex: frontside?.SEX || backside?.SEX || '',
        address: backside?.ADDRESS?.join(', ') || '',
        face: face || '',
        isValid: checks ? Object.values(checks).every(check => check === true) : false
      };
    } catch (error) {
      console.error('Error al extraer información del documento:', error);
      return {
        dni: doc.dni,
        name: '',
        surname: '',
        nationality: '',
        documentNumber: '',
        birthDate: '',
        expiryDate: '',
        sex: '',
        address: '',
        face: '',
        isValid: false
      };
    }
  };

  const displayDocuments = searchResults.length > 0 ? searchResults : documents;

  if (loading) {
    return <LoadingMessage>🔄 Cargando documentos...</LoadingMessage>;
  }

  return (
    <ResultsContainer>
      <StatsContainer>
        <StatsTitle>📊 Estadísticas</StatsTitle>
        <StatsNumber>{documents.length}</StatsNumber>
        <div>Documentos escaneados</div>
      </StatsContainer>

      <SearchContainer>
        <SearchForm onSubmit={handleSearch}>
          <SearchInput
            type="text"
            name="nationality"
            placeholder="Código de nacionalidad (ej: ESP)"
            value={searchFilters.nationality}
            onChange={handleInputChange}
          />
          <SearchInput
            type="text"
            name="dni"
            placeholder="DNI"
            value={searchFilters.dni}
            onChange={handleInputChange}
          />
          <SearchButton type="submit" disabled={isSearching}>
            {isSearching ? '🔍' : '🔍'} Buscar
          </SearchButton>
          <SearchButton 
            type="button" 
            onClick={() => setShowFaceImages(!showFaceImages)}
            style={{ background: showFaceImages ? '#28a745' : '#6c757d' }}
          >
            {showFaceImages ? '👤' : '👤'} {showFaceImages ? 'Ocultar' : 'Mostrar'} Caras
          </SearchButton>
          <RefreshButton type="button" onClick={onRefresh}>
            🔄 Actualizar
          </RefreshButton>
        </SearchForm>
      </SearchContainer>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      {displayDocuments.length === 0 ? (
        <EmptyMessage>
          📄 No hay documentos para mostrar
        </EmptyMessage>
      ) : (
        <DocumentsGrid>
          {displayDocuments.map((doc, index) => {
            const info = extractDocumentInfo(doc);
            return (
              <DocumentCard key={`${doc.dni}-${index}`}>
                <DocumentHeader>
                  <DocumentTitle>
                    {info.name} {info.surname}
                  </DocumentTitle>
                  <DocumentStatus valid={info.isValid}>
                    {info.isValid ? '✅ Válido' : '❌ Inválido'}
                  </DocumentStatus>
                </DocumentHeader>
                
                <DocumentInfo>
                  <InfoRow>
                    <InfoLabel>DNI:</InfoLabel>
                    <InfoValue>{info.dni}</InfoValue>
                  </InfoRow>
                  
                  <InfoRow>
                    <InfoLabel>Nacionalidad:</InfoLabel>
                    <InfoValue>{info.nationality}</InfoValue>
                  </InfoRow>
                  
                  <InfoRow>
                    <InfoLabel>Número de documento:</InfoLabel>
                    <InfoValue>{info.documentNumber}</InfoValue>
                  </InfoRow>
                  
                  <InfoRow>
                    <InfoLabel>Fecha de nacimiento:</InfoLabel>
                    <InfoValue>{info.birthDate}</InfoValue>
                  </InfoRow>
                  
                  <InfoRow>
                    <InfoLabel>Fecha de expiración:</InfoLabel>
                    <InfoValue>{info.expiryDate}</InfoValue>
                  </InfoRow>
                  
                  <InfoRow>
                    <InfoLabel>Sexo:</InfoLabel>
                    <InfoValue>{info.sex}</InfoValue>
                  </InfoRow>
                  
                  {info.address && (
                    <InfoRow>
                      <InfoLabel>Dirección:</InfoLabel>
                      <InfoValue>{info.address}</InfoValue>
                    </InfoRow>
                  )}
                  
                  {showFaceImages && info.face && (
                    <FaceImage 
                      src={info.face} 
                      alt="Imagen facial"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  )}
                </DocumentInfo>
              </DocumentCard>
            );
          })}
        </DocumentsGrid>
      )}
    </ResultsContainer>
  );
};

export default DocumentResults;
