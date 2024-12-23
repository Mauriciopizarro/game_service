import logging
from datadog import DogStatsd

# Configurar el cliente StatsD
statsd = DogStatsd()

# Configurar logging
logger = logging.getLogger('datadog_logger')
logger.setLevel(logging.INFO)

# Configurar handler para enviar logs a DataDog
from datadog import statsd
handler = logging.StreamHandler()
logger.addHandler(handler)

# Enviar un log de prueba
logger.info('Log enviado a DataDog desde Python.')
