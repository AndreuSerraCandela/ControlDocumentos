import logging
import os
from datetime import datetime

# Configurar logging
log_file = os.path.join(os.getcwd(), 'test_logs.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Test logging
logger.info("=== TEST LOG ===")
logger.info(f"Timestamp: {datetime.now().isoformat()}")
logger.info("Este es un test de logging")
logger.info("=== FIN TEST ===")

print("Log test completado")
