# Paperless-MCP-Server

# Paperless-ngx MCP Server

This server allows Large Language Models (LLMs) to interact with your [Paperless-ngx](https://paperless-ngx.com/) document management system through the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/servers).

## What is Paperless-ngx?

Paperless-ngx is a document management system that takes your physical documents, scans them, and transforms them into searchable PDFs. It helps you organize your documents, tag them, and find them easily later.

## What is MCP?

The Model Context Protocol (MCP) is a standard that allows LLMs like ChatGPT to interact with external tools and services. This server implements the MCP protocol for Paperless-ngx, allowing LLMs to search, retrieve, and manipulate your documents.

## Features

- Search for documents in your Paperless-ngx library
- Retrieve document details and content
- List documents by tags, correspondents, or document types
- Upload new documents to your Paperless-ngx system
- Update document metadata

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Access to a Paperless-ngx instance
- API token from your Paperless-ngx instance

### Step 1: Install the MCP Server

```bash
pip install mcp-server-paperlessngx
```

### Step 2: Configure Authentication

Create a configuration file named `.paperlessngx.json` in your home directory:

```json
{
"url": "https://your-paperless-ngx-url.com",
"token": "your-api-token"
}
```

To get your API token:
1. Log in to your Paperless-ngx web interface
2. Go to your user profile
3. Navigate to the "API Tokens" section
4. Create a new token

### Step 3: Start the Server

```bash
mcp-server-paperlessngx
```

By default, the server runs on port 8000. You can specify a different port with the `--port` option:

```bash
mcp-server-paperlessngx --port 8080
```

## Using with LLMs

Once your MCP server is running, you can connect it to compatible LLMs using their MCP integration features. The exact steps depend on the LLM platform you're using.

### Example Commands

The following commands are available to LLMs that connect to your Paperless-ngx MCP server:

- `search_documents(query)`: Search for documents matching a query
- `get_document(id)`: Get details for a specific document
- `list_documents(tags=None, correspondent=None, document_type=None)`: List documents with optional filters
- `get_document_content(id)`: Get the text content of a document
- `upload_document(file_path, title, tags=None)`: Upload a new document
- `update_document(id, title=None, tags=None)`: Update document metadata

## Troubleshooting

### Connection Issues

- Verify your Paperless-ngx instance is running and accessible
- Check that your API token is valid and not expired
- Ensure your configuration file has the correct URL format (including http/https)

### Authentication Errors

- Regenerate your API token in the Paperless-ngx web interface
- Verify that your token has the necessary permissions

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies with `pip install -e ".[dev]"`
3. Run tests with `pytest`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

