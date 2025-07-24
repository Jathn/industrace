# Development Guide

## Overview

This development guide provides comprehensive information for developers working on Industrace, the Configuration Management Database for Industrial Control Systems. It covers development setup, coding standards, testing procedures, and contribution guidelines.

## Table of Contents

1. [Development Environment](#development-environment)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Database Development](#database-development)
5. [API Development](#api-development)
6. [Frontend Development](#frontend-development)
7. [Testing](#testing)
8. [Debugging](#debugging)
9. [Deployment](#deployment)
10. [Contributing](#contributing)

## Development Environment

### Prerequisites

1. **System Requirements**
   - Docker and Docker Compose
   - Git
   - Python 3.9+
   - Node.js 18+
   - PostgreSQL 15+

2. **Development Tools**
   - VS Code or PyCharm
   - Postman or Insomnia
   - pgAdmin or DBeaver
   - Git client

### Setup Instructions

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd industrace
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment files
   cp development.env.example development.env
   
   # Edit development environment
   nano development.env
   ```

3. **Start Development Environment**
   ```bash
   # Start all services
   docker-compose -f docker-compose.yml up -d
   
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f backend
   ```

4. **Database Setup**
   ```bash
   # Run migrations
   docker-compose exec backend alembic upgrade head
   
   # Seed initial data
   docker-compose exec backend python -m app.init_tenant
   docker-compose exec backend python -m app.init_roles
   docker-compose exec backend python -m app.init_test_users
   ```

### Development Workflow

1. **Branch Strategy**
   ```bash
   # Create feature branch
   git checkout -b feature/new-feature
   
   # Make changes and commit
   git add .
   git commit -m "feat: add new feature"
   
   # Push and create pull request
   git push origin feature/new-feature
   ```

2. **Code Review Process**
   - Create pull request
   - Request code review
   - Address feedback
   - Merge after approval

## Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── crud/                # Database operations
│   │   ├── assets.py
│   │   ├── users.py
│   │   └── ...
│   ├── models/              # SQLAlchemy models
│   │   ├── asset.py
│   │   ├── user.py
│   │   └── ...
│   ├── routers/             # API endpoints
│   │   ├── assets.py
│   │   ├── users.py
│   │   └── ...
│   ├── schemas/             # Pydantic schemas
│   │   ├── asset.py
│   │   ├── user.py
│   │   └── ...
│   ├── services/            # Business logic
│   │   ├── auth.py
│   │   ├── asset_sync.py
│   │   └── ...
│   └── utils.py             # Utility functions
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── Dockerfile              # Backend container
```

### Frontend Structure

```
frontend/
├── src/
│   ├── main.js             # Vue application entry point
│   ├── App.vue             # Root component
│   ├── router.js           # Vue Router configuration
│   ├── api/                # API client
│   │   └── api.js
│   ├── components/         # Vue components
│   │   ├── base/           # Base components
│   │   ├── features/       # Feature-specific components
│   │   └── ...
│   ├── pages/              # Page components
│   │   ├── Assets.vue
│   │   ├── Users.vue
│   │   └── ...
│   ├── composables/        # Vue composables
│   │   ├── useApi.js
│   │   ├── useAuth.js
│   │   └── ...
│   ├── locales/            # Internationalization
│   │   ├── en/
│   │   ├── it/
│   │   └── ...
│   └── store/              # State management
│       └── auth.js
├── package.json            # Node.js dependencies
├── vite.config.js          # Vite configuration
└── Dockerfile              # Frontend container
```

## Coding Standards

### Python Standards

1. **Code Style**
   ```python
   # Follow PEP 8
   from typing import Optional, List
   from fastapi import HTTPException, Depends
   
   class AssetService:
       def __init__(self, db: Session = Depends(get_db)):
           self.db = db
       
       def get_asset(self, asset_id: int) -> Optional[Asset]:
           """Get asset by ID."""
           return self.db.query(Asset).filter(Asset.id == asset_id).first()
   ```

2. **Documentation**
   ```python
   def create_asset(asset_data: AssetCreate, db: Session) -> Asset:
       """
       Create a new asset.
       
       Args:
           asset_data: Asset creation data
           db: Database session
           
       Returns:
           Created asset instance
           
       Raises:
           HTTPException: If asset creation fails
       """
       try:
           asset = Asset(**asset_data.dict())
           db.add(asset)
           db.commit()
           db.refresh(asset)
           return asset
       except Exception as e:
           db.rollback()
           raise HTTPException(status_code=400, detail=str(e))
   ```

3. **Error Handling**
   ```python
   from app.errors.exceptions import IndustraceException
   from app.errors.error_codes import ErrorCode
   
   def safe_operation(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           try:
               return func(*args, **kwargs)
           except Exception as e:
               logger.error(f"Operation failed: {str(e)}")
               raise IndustraceException(
                   error_code=ErrorCode.OPERATION_FAILED,
                   detail=str(e)
               )
       return wrapper
   ```

### JavaScript/Vue Standards

1. **Vue Component Structure**
   ```vue
   <template>
     <div class="asset-list">
       <h1>{{ $t('assets.title') }}</h1>
       <AssetTable :assets="assets" @update="loadAssets" />
     </div>
   </template>
   
   <script>
   import { ref, onMounted } from 'vue'
   import { useApi } from '@/composables/useApi'
   import AssetTable from '@/components/AssetTable.vue'
   
   export default {
     name: 'AssetList',
     components: { AssetTable },
     setup() {
       const { api } = useApi()
       const assets = ref([])
       
       const loadAssets = async () => {
         try {
           const response = await api.get('/assets')
           assets.value = response.data
         } catch (error) {
           console.error('Failed to load assets:', error)
         }
       }
       
       onMounted(loadAssets)
       
       return { assets, loadAssets }
     }
   }
   </script>
   
   <style scoped>
   .asset-list {
     padding: 20px;
   }
   </style>
   ```

2. **Composable Pattern**
   ```javascript
   // composables/useAssets.js
   import { ref, computed } from 'vue'
   import { useApi } from './useApi'
   
   export function useAssets() {
     const { api } = useApi()
     const assets = ref([])
     const loading = ref(false)
     const error = ref(null)
     
     const loadAssets = async () => {
       loading.value = true
       error.value = null
       
       try {
         const response = await api.get('/assets')
         assets.value = response.data
       } catch (err) {
         error.value = err.message
       } finally {
         loading.value = false
       }
     }
     
     const createAsset = async (assetData) => {
       try {
         const response = await api.post('/assets', assetData)
         assets.value.push(response.data)
         return response.data
       } catch (err) {
         error.value = err.message
         throw err
       }
     }
     
     return {
       assets: computed(() => assets.value),
       loading: computed(() => loading.value),
       error: computed(() => error.value),
       loadAssets,
       createAsset
     }
   }
   ```

## Database Development

### Model Development

1. **SQLAlchemy Models**
   ```python
   from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
   from sqlalchemy.orm import relationship
   from sqlalchemy.sql import func
   from app.database import Base
   
   class Asset(Base):
       __tablename__ = "assets"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, nullable=False, index=True)
       type = Column(String, nullable=False)
       status = Column(String, default="operational")
       tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
       created_at = Column(DateTime(timezone=True), server_default=func.now())
       updated_at = Column(DateTime(timezone=True), onupdate=func.now())
       
       # Relationships
       tenant = relationship("Tenant", back_populates="assets")
       connections = relationship("AssetConnection", back_populates="asset")
   ```

2. **Migration Creation**
   ```bash
   # Create new migration
   docker-compose exec backend alembic revision --autogenerate -m "Add asset table"
   
   # Apply migration
   docker-compose exec backend alembic upgrade head
   
   # Rollback migration
   docker-compose exec backend alembic downgrade -1
   ```

3. **Database Operations**
   ```python
   from sqlalchemy.orm import Session
   from app.models.asset import Asset
   from app.schemas.asset import AssetCreate
   
   class AssetCRUD:
       def create(self, db: Session, asset: AssetCreate) -> Asset:
           db_asset = Asset(**asset.dict())
           db.add(db_asset)
           db.commit()
           db.refresh(db_asset)
           return db_asset
       
       def get_by_id(self, db: Session, asset_id: int) -> Asset:
           return db.query(Asset).filter(Asset.id == asset_id).first()
       
       def get_by_tenant(self, db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
           return db.query(Asset).filter(Asset.tenant_id == tenant_id).offset(skip).limit(limit).all()
   ```

## API Development

### Endpoint Development

1. **Router Structure**
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from sqlalchemy.orm import Session
   from app.database import get_db
   from app.crud.assets import AssetCRUD
   from app.schemas.asset import Asset, AssetCreate, AssetUpdate
   from app.services.auth import get_current_user
   
   router = APIRouter(prefix="/assets", tags=["assets"])
   asset_crud = AssetCRUD()
   
   @router.get("/", response_model=List[Asset])
   def get_assets(
       skip: int = 0,
       limit: int = 100,
       db: Session = Depends(get_db),
       current_user = Depends(get_current_user)
   ):
       """Get list of assets."""
       return asset_crud.get_by_tenant(db, current_user.tenant_id, skip, limit)
   
   @router.post("/", response_model=Asset)
   def create_asset(
       asset: AssetCreate,
       db: Session = Depends(get_db),
       current_user = Depends(get_current_user)
   ):
       """Create new asset."""
       return asset_crud.create(db, asset)
   ```

2. **Schema Validation**
   ```python
   from pydantic import BaseModel, validator
   from typing import Optional
   from datetime import datetime
   
   class AssetCreate(BaseModel):
       name: str
       type: str
       status: Optional[str] = "operational"
       description: Optional[str] = None
       
       @validator('name')
       def validate_name(cls, v):
           if len(v) < 1 or len(v) > 100:
               raise ValueError('Name must be between 1 and 100 characters')
           return v
       
       @validator('type')
       def validate_type(cls, v):
           valid_types = ['PLC', 'HMI', 'SCADA', 'RTU', 'Network']
           if v not in valid_types:
               raise ValueError(f'Type must be one of: {valid_types}')
           return v
   
   class AssetUpdate(BaseModel):
       name: Optional[str] = None
       type: Optional[str] = None
       status: Optional[str] = None
       description: Optional[str] = None
   ```

3. **Error Handling**
   ```python
   from app.errors.exceptions import IndustraceException
   from app.errors.error_codes import ErrorCode
   
   @router.get("/{asset_id}", response_model=Asset)
   def get_asset(
       asset_id: int,
       db: Session = Depends(get_db),
       current_user = Depends(get_current_user)
   ):
       """Get asset by ID."""
       asset = asset_crud.get_by_id(db, asset_id)
       if not asset:
           raise IndustraceException(
               error_code=ErrorCode.ASSET_NOT_FOUND,
               detail=f"Asset with ID {asset_id} not found"
           )
       
       if asset.tenant_id != current_user.tenant_id:
           raise IndustraceException(
               error_code=ErrorCode.ACCESS_DENIED,
               detail="Access denied to this asset"
           )
       
       return asset
   ```

## Frontend Development

### Component Development

1. **Component Structure**
   ```vue
   <template>
     <div class="asset-form">
       <form @submit.prevent="handleSubmit">
         <div class="form-group">
           <label for="name">{{ $t('assets.form.name') }}</label>
           <input
             id="name"
             v-model="form.name"
             type="text"
             required
             :class="{ 'error': errors.name }"
           />
           <span v-if="errors.name" class="error-message">
             {{ errors.name }}
           </span>
         </div>
         
         <div class="form-group">
           <label for="type">{{ $t('assets.form.type') }}</label>
           <select id="type" v-model="form.type" required>
             <option value="">{{ $t('common.select') }}</option>
             <option value="PLC">PLC</option>
             <option value="HMI">HMI</option>
             <option value="SCADA">SCADA</option>
           </select>
         </div>
         
         <button type="submit" :disabled="loading">
           {{ loading ? $t('common.saving') : $t('common.save') }}
         </button>
       </form>
     </div>
   </template>
   
   <script>
   import { ref, reactive } from 'vue'
   import { useAssets } from '@/composables/useAssets'
   
   export default {
     name: 'AssetForm',
     emits: ['saved'],
     setup(props, { emit }) {
       const { createAsset } = useAssets()
       const loading = ref(false)
       const errors = reactive({})
       
       const form = reactive({
         name: '',
         type: '',
         description: ''
       })
       
       const handleSubmit = async () => {
         loading.value = true
         errors.value = {}
         
         try {
           const asset = await createAsset(form)
           emit('saved', asset)
           
           // Reset form
           form.name = ''
           form.type = ''
           form.description = ''
         } catch (error) {
           if (error.response?.data?.errors) {
             errors.value = error.response.data.errors
           }
         } finally {
           loading.value = false
         }
       }
       
       return {
         form,
         loading,
         errors,
         handleSubmit
       }
     }
   }
   </script>
   ```

2. **State Management**
   ```javascript
   // store/assets.js
   import { defineStore } from 'pinia'
   import { useApi } from '@/composables/useApi'
   
   export const useAssetStore = defineStore('assets', {
     state: () => ({
       assets: [],
       loading: false,
       error: null,
       filters: {
         type: '',
         status: '',
         search: ''
       }
     }),
     
     getters: {
       filteredAssets: (state) => {
         let filtered = state.assets
         
         if (state.filters.type) {
           filtered = filtered.filter(asset => asset.type === state.filters.type)
         }
         
         if (state.filters.status) {
           filtered = filtered.filter(asset => asset.status === state.filters.status)
         }
         
         if (state.filters.search) {
           const search = state.filters.search.toLowerCase()
           filtered = filtered.filter(asset => 
             asset.name.toLowerCase().includes(search) ||
             asset.description?.toLowerCase().includes(search)
           )
         }
         
         return filtered
       }
     },
     
     actions: {
       async loadAssets() {
         this.loading = true
         this.error = null
         
         try {
           const { api } = useApi()
           const response = await api.get('/assets')
           this.assets = response.data
         } catch (error) {
           this.error = error.message
         } finally {
           this.loading = false
         }
       },
       
       setFilter(filter, value) {
         this.filters[filter] = value
       }
     }
   })
   ```

## Testing

### Backend Testing

1. **Unit Tests**
   ```python
   # tests/test_assets.py
   import pytest
   from fastapi.testclient import TestClient
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   from app.main import app
   from app.database import get_db, Base
   
   # Test database
   SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
   engine = create_engine(SQLALCHEMY_DATABASE_URL)
   TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   
   def override_get_db():
       try:
           db = TestingSessionLocal()
           yield db
       finally:
           db.close()
   
   app.dependency_overrides[get_db] = override_get_db
   client = TestClient(app)
   
   def test_create_asset():
       response = client.post(
           "/assets/",
           json={"name": "Test Asset", "type": "PLC"}
       )
       assert response.status_code == 200
       data = response.json()
       assert data["name"] == "Test Asset"
       assert data["type"] == "PLC"
   ```

2. **Integration Tests**
   ```python
   # tests/test_integration.py
   def test_asset_workflow():
       # Create asset
       create_response = client.post(
           "/assets/",
           json={"name": "Test Asset", "type": "PLC"}
       )
       assert create_response.status_code == 200
       asset_id = create_response.json()["id"]
       
       # Get asset
       get_response = client.get(f"/assets/{asset_id}")
       assert get_response.status_code == 200
       assert get_response.json()["name"] == "Test Asset"
       
       # Update asset
       update_response = client.put(
           f"/assets/{asset_id}",
           json={"status": "maintenance"}
       )
       assert update_response.status_code == 200
       assert update_response.json()["status"] == "maintenance"
   ```

### Frontend Testing

1. **Component Tests**
   ```javascript
   // tests/unit/AssetForm.spec.js
   import { mount } from '@vue/test-utils'
   import AssetForm from '@/components/AssetForm.vue'
   
   describe('AssetForm', () => {
     it('emits saved event when form is submitted', async () => {
       const wrapper = mount(AssetForm)
       
       // Fill form
       await wrapper.find('#name').setValue('Test Asset')
       await wrapper.find('#type').setValue('PLC')
       
       // Submit form
       await wrapper.find('form').trigger('submit')
       
       // Check emitted event
       expect(wrapper.emitted('saved')).toBeTruthy()
     })
   })
   ```

2. **E2E Tests**
   ```javascript
   // tests/e2e/asset-management.spec.js
   describe('Asset Management', () => {
     it('should create and display assets', () => {
       cy.visit('/assets')
       
       // Click create button
       cy.get('[data-testid="create-asset"]').click()
       
       // Fill form
       cy.get('#name').type('Test Asset')
       cy.get('#type').select('PLC')
       
       // Submit
       cy.get('form').submit()
       
       // Verify asset appears in list
       cy.contains('Test Asset').should('be.visible')
     })
   })
   ```

## Debugging

### Backend Debugging

1. **Logging Configuration**
   ```python
   import logging
   
   # Configure logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('logs/debug.log'),
           logging.StreamHandler()
       ]
   )
   
   logger = logging.getLogger(__name__)
   
   def debug_function():
       logger.debug("Debug message")
       logger.info("Info message")
       logger.warning("Warning message")
       logger.error("Error message")
   ```

2. **Database Debugging**
   ```python
   # Enable SQL logging
   import logging
   logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
   
   # Debug queries
   from sqlalchemy import event
   
   @event.listens_for(Engine, "before_cursor_execute")
   def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
       print(f"Executing: {statement}")
   ```

### Frontend Debugging

1. **Vue DevTools**
   - Install Vue DevTools browser extension
   - Use component inspector
   - Monitor state changes
   - Debug events

2. **Console Debugging**
   ```javascript
   // Debug API calls
   const { api } = useApi()
   
   // Add request interceptor
   api.interceptors.request.use(request => {
     console.log('Request:', request)
     return request
   })
   
   // Add response interceptor
   api.interceptors.response.use(
     response => {
       console.log('Response:', response)
       return response
     },
     error => {
       console.error('API Error:', error)
       return Promise.reject(error)
     }
   )
   ```

## Deployment

### Development Deployment

1. **Local Development**
   ```bash
   # Start development environment
   docker-compose up -d
   
   # Watch logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   ```

2. **Hot Reload**
   ```yaml
   # docker-compose.yml
   services:
     backend:
       volumes:
         - ./backend:/app
       command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
     frontend:
       volumes:
         - ./frontend:/app
         - /app/node_modules
       command: npm run dev
   ```

### Production Deployment

1. **Build Process**
   ```bash
   # Build production images
   docker-compose -f docker-compose.prod.yml build
   
   # Deploy to production
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Environment Configuration**
   ```bash
   # Production environment
   cp production.env.example production.env
   
   # Configure production settings
   nano production.env
   ```

## Contributing

### Contribution Guidelines

1. **Code Standards**
   - Follow PEP 8 for Python
   - Use ESLint for JavaScript
   - Write comprehensive tests
   - Document all functions

2. **Commit Messages**
   ```bash
   # Conventional commits
   feat: add new asset type
   fix: resolve authentication issue
   docs: update API documentation
   test: add unit tests for asset creation
   refactor: improve error handling
   ```

3. **Pull Request Process**
   - Create feature branch
   - Write tests
   - Update documentation
   - Request code review
   - Address feedback
   - Merge after approval

### Development Tools

1. **Code Quality**
   ```bash
   # Python linting
   flake8 backend/
   black backend/
   isort backend/
   
   # JavaScript linting
   npm run lint
   npm run format
   ```

2. **Testing**
   ```bash
   # Run all tests
   pytest tests/
   
   # Run with coverage
   pytest --cov=app tests/
   
   # Frontend tests
   npm run test:unit
   npm run test:e2e
   ```

3. **Documentation**
   ```bash
   # Generate API docs
   docker-compose exec backend python -m app.generate_docs
   
   # Build documentation
   mkdocs build
   ```

---

**Industrace** - Configuration Management Database for Industrial Control Systems  
**Author**: Maurizio Bertaboni (BeSafe S.r.l.)  
**Website**: https://besafe.it/industrace  
**Contact**: industrace@besafe.it 