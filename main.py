import httpx
from typing import Any, Dict, Optional
from mcp.server.fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging

# ---- Config ----
API_BASE = "https://api.vincario.com/3.2"

mcp = FastMCP(
    name="Vincario VIN Tools",
    instructions="VIN decode, decode info, market value, and stolen check via Vincario API v3.2",
    host="0.0.0.0",
    port=8080,
    stateless_http=True
)

# ---- Helpers ----

def _get_api_key_from_header() -> str:
    headers = get_http_headers()
    key = headers.get("x-api-key") or headers.get("X-API-Key") or ""

    if not key:
        raise RuntimeError("Missing X-API-Key header")

    return key

def _build_url(path: str) -> str:
    return f"{API_BASE}/{path}"

async def _get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(url, headers={"X-API-Key": _get_api_key_from_header()}, params=params)
        res.raise_for_status()
        return res.json()

# ---- Custom route ----

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})

# ---- Tools ----

@mcp.tool(
    name="vin_decode",
    title="Vin Decode",
    description="Decode a VIN and return detailed information about the vehicle."
)
async def vin_decode(vin: str) -> Dict[str, Any]:
    url = _build_url(f"decode/{vin.upper()}.json")
    return await _get_json(url)

@mcp.tool(
    name="vin_decode_info",
    title="Vin Decode Info",
    description="List which fields are available for decoding a given VIN (free endpoint)."
)
async def vin_decode_info(vin: str) -> Dict[str, Any]:
    url = _build_url(f"decode/info/{vin.upper()}.json")
    return await _get_json(url)

@mcp.tool(
    name="stolen_check",
    title="Stolen Check",
    description="Check if a VIN appears in supported police/Vincario stolen databases."
)
async def stolen_check(vin: str) -> Dict[str, Any]:
    url = _build_url(f"stolen-check/{vin.upper()}.json")
    return await _get_json(url)

@mcp.tool(
    name="vehicle_market_value",
    title="Vehicle Market Value",
    description=(
        "Vehicle Market Value for a VIN. Accepts query parameters: odometer (int), odometer_unit (str)."
        "Pass them via 'params' dictionary."
    )
)
async def vehicle_market_value(
    vin: str,
    odometer: Optional[int] = None,
    odometer_unit: Optional[str] = None
) -> Dict[str, Any]:
    url = _build_url(f"vehicle-market-value/{vin.upper()}.json")
    # Ensure keys are strings for safety and do not pass None values
    q = {}
    if odometer is not None:
        q['odometer'] = odometer
    if odometer_unit is not None:
        q['odometer_unit'] = odometer_unit
    return await _get_json(url, q)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
