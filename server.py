import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, cast

import aiohttp
from mcp import (
    MCPContext,
    MCPMetaParams,
    MCPParams,
    MCPRequest,
    MCPResponse,
    MCPService,
    MCPServiceConfig,
    MCPServiceError,
    MCPServiceLoadError,
    run_server,
)


@dataclass
class PaperlessConfig:
    """Configuration for the Paperless-ngx MCP service."""
    
    base_url: str
    token: str
    timeout: float = 30.0


class PaperlessClient:
    """Client for interacting with the Paperless-ngx API."""
    
    def __init__(self, config: PaperlessConfig):
        self.config = config
        self.headers = {
            "Authorization": f"Token {config.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = aiohttp.ClientTimeout(total=config.timeout)
    
    async def _request(
        self, method: str, path: str, params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a request to the Paperless-ngx API."""
        url = f"{self.config.base_url.rstrip('/')}/api/{path.lstrip('/')}"
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.request(
                method, url, headers=self.headers, params=params, json=data
            ) as response:
                if response.status >= 400:
                    response_text = await response.text()
                    raise MCPServiceError(
                        f"Paperless-ngx API request failed: {response.status} {response_text}"
                    )
                
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    response_text = await response.text()
                    if response_text:
                        return {"response": response_text}
                    return {}
    
    async def get_documents(self, query: Optional[str] = None, page: int = 1, page_size: int = 25) -> Dict[str, Any]:
        """Get a list of documents, optionally filtered by a search query."""
        params = {
            "page": page,
            "page_size": page_size,
        }
        if query:
            params["query"] = query
        
        return await self._request("GET", "documents/", params=params)
    
    async def get_document(self, document_id: int) -> Dict[str, Any]:
        """Get a specific document by ID."""
        return await self._request("GET", f"documents/{document_id}/")
    
    async def get_document_download(self, document_id: int) -> Dict[str, Any]:
        """Get download information for a specific document."""
        return await self._request("GET", f"documents/{document_id}/download/")
    
    async def search_documents(self, query: str) -> Dict[str, Any]:
        """Search for documents using a query string."""
        return await self.get_documents(query=query)
    
    async def get_correspondents(self) -> Dict[str, Any]:
        """Get a list of all correspondents."""
        return await self._request("GET", "correspondents/")
    
    async def get_tags(self) -> Dict[str, Any]:
        """Get a list of all tags."""
        return await self._request("GET", "tags/")
    
    async def get_document_types(self) -> Dict[str, Any]:
        """Get a list of all document types."""
        return await self._request("GET", "document_types/")


class PaperlessMCPService(MCPService):
    """MCP service for interacting with Paperless-ngx."""
    
    def __init__(self):
        self.client: Optional[PaperlessClient] = None
    
    @property
    def name(self) -> str:
        return "paperlessngx"
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    async def load(self, config: MCPServiceConfig) -> None:
        """Load and configure the Paperless-ngx service."""
        if not config.get("base_url"):
            raise MCPServiceLoadError("Paperless-ngx base URL is required")
        
        if not config.get("token"):
            raise MCPServiceLoadError("Paperless-ngx API token is required")
        
        self.client = PaperlessClient(
            PaperlessConfig(
                base_url=str(config["base_url"]),
                token=str(config["token"]),
                timeout=float(config.get("timeout", 30.0)),
            )
        )
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle an MCP request and return a response."""
        if not self.client:
            raise MCPServiceError("Paperless-ngx service is not initialized")
        
        method = request.method
        
        if method == "list_documents":
            return await self._list_documents(request.params, request.context)
        elif method == "get_document":
            return await self._get_document(request.params, request.context)
        elif method == "search_documents":
            return await self._search_documents(request.params, request.context)
        elif method == "list_correspondents":
            return await self._list_correspondents(request.params, request.context)
        elif method == "list_tags":
            return await self._list_tags(request.params, request.context)
        elif method == "list_document_types":
            return await self._list_document_types(request.params, request.context)
        else:
            return MCPResponse(
                error=f"Unknown method: {method}",
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
    
    async def _list_documents(self, params: MCPParams, context: MCPContext) -> MCPResponse:
        """List documents with optional pagination."""
        page = int(params.get("page", 1))
        page_size = int(params.get("page_size", 25))
        
        try:
            response = await self.client.get_documents(page=page, page_size=page_size)
            return MCPResponse(
                response=response,
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except Exception as e:
            return MCPResponse(
                error=str(e),
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
    
    async def _get_document(self, params: MCPParams, context: MCPContext) -> MCPResponse:
        """Get details for a specific document by ID."""
        document_id = params.get("id")
        if not document_id:
            return MCPResponse(
                error="Document ID is required",
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        
        try:
            document_id_int = int(document_id)
            response = await self.client.get_document(document_id_int)
            return MCPResponse(
                response=response,
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except ValueError:
            return MCPResponse(
                error="Invalid document ID format, must be an integer",
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except Exception as e:
            return MCPResponse(
                error=str(e),
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
    
    async def _search_documents(self, params: MCPParams, context: MCPContext) -> MCPResponse:
        """Search for documents using a query string."""
        query = params.get("query")
        if not query:
            return MCPResponse(
                error="Search query is required",
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        
        try:
            response = await self.client.search_documents(query)
            return MCPResponse(
                response=response,
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except Exception as e:
            return MCPResponse(
                error=str(e),
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
    
    async def _list_correspondents(self, params: MCPParams, context: MCPContext) -> MCPResponse:
        """List all correspondents."""
        try:
            response = await self.client.get_correspondents()
            return MCPResponse(
                response=response,
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except Exception as e:
            return MCPResponse(
                error=str(e),
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
    
    async def _list_tags(self, params: MCPParams, context: MCPContext) -> MCPResponse:
        """List all tags."""
        try:
            response = await self.client.get_tags()
            return MCPResponse(
                response=response,
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except Exception as e:
            return MCPResponse(
                error=str(e),
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
    
    async def _list_document_types(self, params: MCPParams, context: MCPContext) -> MCPResponse:
        """List all document types."""
        try:
            response = await self.client.get_document_types()
            return MCPResponse(
                response=response,
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )
        except Exception as e:
            return MCPResponse(
                error=str(e),
                meta=MCPMetaParams(
                    usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                ),
            )


def main() -> None:
    """Run the Paperless-ngx MCP server."""
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    service = PaperlessMCPService()
    run_server(service)


if __name__ == "__main__":
    main()

