# Paperless MCP - Document Management System

<p align="center">
<img src="https://via.placeholder.com/200x200?text=Paperless+MCP" alt="Paperless MCP Logo" width="200" height="200">
</p>

<p align="center">
A modern, efficient document management system for the digital workplace
</p>

<p align="center">
<a href="#features">Features</a> •
<a href="#installation">Installation</a> •
<a href="#usage">Usage</a> •
<a href="#api-documentation">API</a> •
<a href="#configuration">Configuration</a> •
<a href="#contributing">Contributing</a> •
<a href="#license">License</a>
</p>

## Overview

Paperless MCP is an open-source document management system designed to streamline the handling of digital documents in enterprise environments. It provides a comprehensive solution for storing, organizing, searching, and processing documents, eliminating the need for physical paperwork and simplifying document workflows.

The system offers robust document processing capabilities, including OCR (Optical Character Recognition), metadata extraction, and automated document classification, all while maintaining strict security and access controls.

## Features

**Document Storage & Organization**
- Secure cloud or on-premises document storage
- Hierarchical folder structure
- Custom metadata and tagging
- Advanced search capabilities

**Document Processing**
- OCR for scanned documents
- Automated document classification
- Metadata extraction
- PDF processing and manipulation

**Security & Compliance**
- Role-based access control
- Audit logging for all document activities
- Encryption of sensitive data
- Compliance with industry standards (GDPR, HIPAA, etc.)

**Integration & Extensibility**
- RESTful API for third-party integration
- Webhook support for automation
- Customizable workflow engine
- Plugin architecture for extending functionality

**User Experience**
- Intuitive web-based user interface
- Mobile-responsive design
- Document preview and annotation
- Batch operations for efficient document handling

## Installation

### Prerequisites

- Node.js (v16 or later)
- npm or yarn
- PostgreSQL (v13 or later)
- Docker (optional, for containerized deployment)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/paperless-mcp.git
cd paperless-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
npm run migrate
```

5. Start the development server:
```bash
npm run dev
```

### Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/paperless-mcp.git
cd paperless-mcp
```

2. Build and start the Docker containers:
```bash
docker-compose up -d
```

The application will be available at http://localhost:3000.

## Usage

### Basic Operations

#### Document Upload

```typescript
import { DocumentService } from 'paperless-mcp';

const documentService = new DocumentService();
const result = await documentService.uploadDocument({
file: fileBuffer,
metadata: {
    title: 'Invoice #12345',
    category: 'Finance',
    tags: ['invoice', '2023', 'vendor-abc']
}
});
```

#### Document Retrieval

```typescript
const document = await documentService.getDocument(documentId);
```

#### Document Search

```typescript
const searchResults = await documentService.searchDocuments({
query: 'invoice',
filters: {
    category: 'Finance',
    dateRange: {
    from: '2023-01-01',
    to: '2023-12-31'
    }
},
page: 1,
limit: 20
});
```

### CLI Usage

Paperless MCP also provides a command-line interface for administrative tasks:

```bash
# Display help
npx paperless-mcp --help

# Initialize the system
npx paperless-mcp init

# Import documents from a directory
npx paperless-mcp import --source /path/to/documents

# Run system diagnostics
npx paperless-mcp diagnose
```

## API Documentation

Paperless MCP exposes a RESTful API for integration with other systems. The API is available at `/api/v1` and requires authentication via API keys or JWT tokens.

### Authentication

```
POST /api/v1/auth/login
```

Request body:
```json
{
"username": "admin",
"password": "your-password"
}
```

Response:
```json
{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"expiresAt": "2023-12-31T23:59:59Z"
}
```

### Documents API

#### Create Document

```
POST /api/v1/documents
```

Request body:
```json
{
"title": "Invoice #12345",
"content": "Base64 encoded file content...",
"metadata": {
    "category": "Finance",
    "tags": ["invoice", "2023"]
}
}
```

#### Get Document

```
GET /api/v1/documents/:id
```

#### Search Documents

```
GET /api/v1/documents/search?q=invoice&category=Finance&from=2023-01-01&to=2023-12-31&page=1&limit=20
```

For a complete API reference, see the [API Documentation](docs/api/README.md).

## Configuration

Paperless MCP can be configured through environment variables, configuration files, or the `smithery.yaml` file.

### Environment Variables

- `PORT`: The port the server will listen on (default: 3000)
- `DATABASE_URL`: PostgreSQL connection string
- `STORAGE_TYPE`: Storage backend ('local', 's3', 'azure', etc.)
- `STORAGE_PATH`: Local storage path (if STORAGE_TYPE=local)
- `LOG_LEVEL`: Logging level ('debug', 'info', 'warn', 'error')
- `JWT_SECRET`: Secret for JWT token generation
- `OCR_ENGINE`: OCR engine to use ('tesseract', 'azure', etc.)

### Configuration File

For more advanced configuration, create a `config.js` or `config.json` file in the project root. Example:

```json
{
"server": {
    "port": 3000,
    "host": "0.0.0.0",
    "cors": {
    "enabled": true,
    "origins": ["https://example.com"]
    }
},
"database": {
    "url": "postgresql://user:password@localhost:5432/paperless",
    "pool": {
    "min": 2,
    "max": 10
    }
},
"storage": {
    "type": "s3",
    "config": {
    "bucket": "paperless-documents",
    "region": "us-west-2"
    }
}
}
```

## Contributing

We welcome contributions to Paperless MCP! Please feel free to submit issues, feature requests, and pull requests.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/paperless-mcp.git`
3. Create a feature branch: `git checkout -b feature/my-feature`
4. Make your changes
5. Run tests: `npm test`
6. Commit your changes: `git commit -m 'Add my feature'`
7. Push to the branch: `git push origin feature/my-feature`
8. Submit a pull request

### Coding Standards

- We follow the [TypeScript Coding Guidelines](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines)
- All code should be properly typed
- Unit tests are required for new features
- Documentation should be updated with any changes

### Documentation

- API documentation is generated using TypeDoc
- Update the README.md if you add or change features
- Add examples for new functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for the tools and libraries that make this project possible

---

<p align="center">
Made with ❤️ by the Paperless MCP Team
</p>

