# 📦 Escáner de Códigos de Barras

Aplicación web para escanear códigos de barras usando la cámara del celular y almacenarlos en archivos CSV.

## 🚀 Características

- ✅ **Autenticación con Google** - Login seguro sin restricciones
- 📷 **Escaneo de códigos** - Soporta todos los formatos (EAN-13, Code 128, QR, etc.)
- 💾 **Almacenamiento en CSV** - Archivos organizados por fecha con versiones
- 🔢 **Contador en tiempo real** - Visualización de lecturas válidas
- ⚠️ **Detección de duplicados** - Alerta al usuario pero permite guardar
- 📱 **Responsive** - Optimizado para dispositivos móviles

## 🛠️ Stack Tecnológico

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** React 19 + html5-qrcode
- **Base de datos:** MongoDB
- **Autenticación:** Emergent OAuth (Google)
- **Deployment:** Docker + Coolify

## 📋 Requisitos

- MongoDB (local o remoto)
- Node.js 18+ y Yarn
- Python 3.11+

## 🐳 Deployment en Coolify

### 1. Configurar repositorio Git

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <tu-repositorio-git>
git push -u origin main
```

### 2. Configurar Coolify

1. En Coolify, crear un nuevo proyecto
2. Seleccionar "Deploy from Git"
3. Conectar tu repositorio
4. Coolify detectará automáticamente el `Dockerfile`

### 3. Variables de entorno en Coolify

Configurar las siguientes variables de entorno:

```bash
# MongoDB
MONGO_URL=mongodb://localhost:27017
# O usar MongoDB remoto:
# MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/

DB_NAME=barcode_scanner

# CORS
CORS_ORIGINS=https://barras.facore.cloud

# Backend URL (para el frontend)
REACT_APP_BACKEND_URL=https://barras.facore.cloud
```

### 4. Configurar volumen persistente

Para mantener los archivos CSV, configurar un volumen:

```yaml
/app/data:/path/to/host/data
```

### 5. Configurar dominio

En Coolify, configurar el dominio: `barras.facore.cloud`

### 6. Deploy

Coolify construirá la imagen Docker y desplegará automáticamente.

## 🖥️ Desarrollo Local

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### Frontend

```bash
cd frontend
yarn install
yarn start
```

### MongoDB

```bash
# Instalar MongoDB localmente o usar Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## 📁 Estructura de archivos CSV

Los archivos CSV se generan en el directorio `/data` con el siguiente formato:

**Nombre:** `barras_YYYYMMDD_v{n}.csv`

**Ejemplo:** `barras_20250130_v1.csv`

**Columnas:**
```csv
timestamp,codigo,usuario
2025-01-30 10:30:45,1234567890123,user@example.com
2025-01-30 10:31:02,9876543210987,user@example.com
```

## 🎨 Paleta de Colores

La aplicación utiliza una paleta de tonos marrones:

```css
--primary-color: #5f2e0a;      /* Marrón silla de montar */
--secondary-color: #5f2e0a;    /* Marrón tierra */
--accent-color: #dec290;       /* Beige claro */
--background-color: #d1b684;   /* Beige muy claro */
--text-color: #5D4037;         /* Marrón oscuro */
--text-light: #8D6E63;         /* Marrón medio */
--white: #FFFFFF;              /* Blanco */
```

## 🔐 Autenticación

La aplicación utiliza **Emergent-managed Google OAuth** que:

- ✅ No requiere configurar credenciales de Google OAuth
- ✅ Funciona con cualquier cuenta de Google
- ✅ Sesiones de 7 días
- ✅ Cookies httpOnly seguras

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
yarn test
```

## 📝 API Endpoints

### Autenticación
- `POST /api/auth/session` - Exchange session_id for token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Códigos de barras
- `GET /api/current-session` - Get or create barcode session
- `POST /api/barcode` - Save scanned barcode
- `GET /api/session-stats` - Get session statistics
- `POST /api/finalize-session` - Finalize and generate CSV

## 🤝 Soporte

Para dudas o problemas, contactar al equipo de desarrollo.

## 📄 Licencia

Propietario - Todos los derechos reservados
