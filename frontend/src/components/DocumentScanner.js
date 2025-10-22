import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';

const ScannerContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
`;

const ScannerButton = styled.button`
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 20px 40px;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const VideoContainer = styled.div`
  width: 100%;
  max-width: 500px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  background: #000;
`;

const Video = styled.video`
  width: 100%;
  height: auto;
  display: block;
`;

const Instructions = styled.div`
  background: #e3f2fd;
  border: 1px solid #2196f3;
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
`;

const InstructionTitle = styled.h3`
  color: #1976d2;
  margin: 0 0 10px 0;
  font-size: 1.3rem;
`;

const InstructionList = styled.ul`
  color: #1976d2;
  text-align: left;
  margin: 0;
  padding-left: 20px;
`;

const ErrorMessage = styled.div`
  background: #ffebee;
  border: 1px solid #f44336;
  color: #c62828;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
  text-align: center;
`;

const SuccessMessage = styled.div`
  background: #e8f5e8;
  border: 1px solid #4caf50;
  color: #2e7d32;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
  text-align: center;
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const DocumentScanner = ({ onDocumentScanned, loading, error }) => {
  const [isScanning, setIsScanning] = useState(false);
  const [stream, setStream] = useState(null);
  const [facephiSDK, setFacephiSDK] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Configuración del SDK de Facephi
  const facephiConfig = {
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

  useEffect(() => {
    // Inicializar el SDK de Facephi cuando el componente se monta
    initializeFacephiSDK();
    
    return () => {
      // Limpiar recursos cuando el componente se desmonta
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const initializeFacephiSDK = async () => {
    try {
      // Aquí cargarías el SDK de Facephi desde el CDN o npm
      // Por ahora simularemos la inicialización
      console.log('Inicializando SDK de Facephi...');
      setFacephiSDK({
        initialized: true,
        config: facephiConfig
      });
    } catch (error) {
      console.error('Error al inicializar SDK de Facephi:', error);
    }
  };

  const startScanning = async () => {
    try {
      setIsScanning(true);
      
      // Solicitar acceso a la cámara
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment', // Usar cámara trasera en móviles
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });
      
      setStream(mediaStream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      
    } catch (error) {
      console.error('Error al acceder a la cámara:', error);
      alert('No se pudo acceder a la cámara. Por favor, permite el acceso a la cámara y recarga la página.');
    }
  };

  const stopScanning = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsScanning(false);
  };

  const captureDocument = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Configurar el canvas con las dimensiones del video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Capturar el frame actual
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convertir a base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    
    // Simular el procesamiento del documento con Facephi SDK
    const documentData = await processDocumentWithFacephi(imageData);
    
    // Enviar los datos al componente padre
    onDocumentScanned(documentData);
    
    // Detener el escaneo
    stopScanning();
  };

  const processDocumentWithFacephi = async (imageData) => {
    // Simulación del procesamiento con Facephi SDK
    // En una implementación real, aquí usarías el SDK de Facephi
    
    const mockDocumentData = {
      transactionId: generateTransactionId(),
      dni: "10873694F", // Este valor vendría del SDK
      clientData: {
        customerId: generateCustomerId()
      },
      deviceInfo: {
        osVersion: navigator.userAgent,
        model: "Web Browser",
        brand: "Web",
        browser: navigator.userAgent,
        osName: navigator.platform
      },
      resultJSON: {
        DocumentData: {
          serviceTransactionId: generateTransactionId(),
          serviceDocument: {
            CHECKS: {
              PERSONAL_NUMBER_SIDE_MATCH: true,
              SEX_SIDE_MATCH: true,
              BACKSIDE_AGE_IS_ADULT: true,
              BACKSIDE_EXPIRATION_DATE_VALID: true,
              BACKSIDE_PERSONAL_NUMBER_CHECK_DIGIT_VALID: true,
              DATE_OF_BIRTH_SIDE_MATCH: true,
              DATE_OF_EXPIRY_SIDE_MATCH: true,
              FRONTSIDE_AGE_IS_ADULT: true,
              FRONTSIDE_EXPIRATION_DATE_VALID: true,
              FRONTSIDE_PERSONAL_NUMBER_CHECK_DIGIT_VALID: true,
              FULLNAME_SIDE_MATCH: true,
              MRZ_CHECK_DIGIT_DOB: "1",
              MRZ_CHECK_DIGIT_DOB_IS_VALID: true,
              MRZ_CHECK_DIGIT_DOCUMENT_NUMBER: "4",
              MRZ_CHECK_DIGIT_DOCUMENT_NUMBER_IS_VALID: true,
              MRZ_CHECK_DIGIT_EXPIRY: "5",
              MRZ_CHECK_DIGIT_EXPIRY_IS_VALID: true,
              MRZ_CHECK_DIGIT_FINALCHECK: "1",
              MRZ_CHECK_DIGIT_FINALCHECK_IS_VALID: true,
              NATIONALITY_CODE_SIDE_MATCH: true
            },
            FRONTSIDE: {
              FIELD_DATA: {
                PERSONAL_NUMBER: "10873694F",
                SEX: "F",
                SURNAME: ["ALVAREZ", "ALVAREZ"],
                CARD_ACCESS_NUMBER: "199616",
                DATE_OF_BIRTH: "11/11/1970",
                DATE_OF_EXPIRY: "17/03/2031",
                DOCUMENT_NUMBER: "BOE191477",
                FIRST_SURNAME: "ALVAREZ",
                GIVEN_NAMES: "INES",
                NATIONALITY_CODE: "ESP",
                SECOND_SURNAME: "ALVAREZ"
              }
            },
            BACKSIDE: {
              FIELD_DATA: {
                ADDRESS: ["C. CONCEJO DE CARAVIA 2 P02", "GIJÓN", "ASTURIAS"],
                AUTHORITY_CODE: "33277L6D2",
                E_ID_PLACE_OF_BIRTH_CITY: ["GIJÓN", "ASTURIAS"],
                PARENTS_GIVEN_NAMES: "ALBERTO SUSANA"
              },
              MRZ_DATA: {
                BIRTH_DATE: "11/11/1970",
                EXPIRATION_DATE: "17/03/2031",
                IDENTITY_NUMBER: "80E191477",
                ISSUING_COUNTRY: "ESP",
                NAME: "INES",
                NATIONALITY: "ESP",
                PERSONAL_NUMBER: "10873694F",
                SEX: "F",
                SURNAME: "ALVAREZ ALVAREZ"
              }
            },
            DECOMPOSED: {
              FACE: imageData // Imagen capturada
            }
          }
        }
      }
    };

    return mockDocumentData;
  };

  const generateTransactionId = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };

  const generateCustomerId = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };

  return (
    <ScannerContainer>
      <Instructions>
        <InstructionTitle>📋 Instrucciones para escanear</InstructionTitle>
        <InstructionList>
          <li>Asegúrate de tener buena iluminación</li>
          <li>Coloca el documento sobre una superficie plana</li>
          <li>Mantén la cámara estable y perpendicular al documento</li>
          <li>El documento debe ocupar la mayor parte del marco</li>
        </InstructionList>
      </Instructions>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      {!isScanning ? (
        <ScannerButton onClick={startScanning} disabled={loading}>
          {loading ? <LoadingSpinner /> : '📷'} Iniciar Escaneo
        </ScannerButton>
      ) : (
        <>
          <VideoContainer>
            <Video
              ref={videoRef}
              autoPlay
              playsInline
              muted
            />
          </VideoContainer>
          
          <ScannerButton onClick={captureDocument} disabled={loading}>
            {loading ? <LoadingSpinner /> : '📸'} Capturar Documento
          </ScannerButton>
          
          <ScannerButton onClick={stopScanning} style={{ background: '#dc3545' }}>
            ❌ Cancelar
          </ScannerButton>
        </>
      )}

      {/* Canvas oculto para capturar frames */}
      <canvas
        ref={canvasRef}
        style={{ display: 'none' }}
      />
    </ScannerContainer>
  );
};

export default DocumentScanner;
