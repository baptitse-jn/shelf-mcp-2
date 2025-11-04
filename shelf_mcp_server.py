"""
Shelf.im MCP Server - Personal Media Consumption Tracking

This MCP server provides tools to access and query media consumption data from Shelf.im,
enabling AI agents to understand a user's cultural interests and consumption patterns.

IMPORTANT: This server requires access to Shelf.im's API or DataMover platform.
As of November 2025, the DataMover API (https://datamover.org/docs/apis) is in 
early access and requires approval. Contact team@koodos.com to request access.

Features:
- Query recent movies, TV shows, music, books, games watched/read/played
- Get detailed history with timestamps and metadata
- Search across all media types
- Get weekly/monthly recaps
- Find trending items on your shelf
- Discover what friends are consuming (if available)
"""

from typing import Any, Literal, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Constants
CHARACTER_LIMIT = 25000
API_BASE_URL = os.getenv("SHELF_API_BASE_URL", "https://api.shelf.im/v1")
API_KEY = os.getenv("SHELF_API_KEY", "")

# Initialize FastMCP server
mcp = FastMCP("shelf")


# ============================================================================
# Pydantic Models for Input Validation
# ============================================================================

class MediaType(BaseModel):
    """Supported media types on Shelf"""
    type: Literal["movie", "tv_show", "music", "book", "game", "podcast", "all"] = Field(
        default="all",
        description="Type of media to query. Use 'all' to search across all types."
    )


class TimeRange(BaseModel):
    """Time range for querying history"""
    range: Literal["day", "week", "month", "year", "all"] = Field(
        default="week",
        description="Time range to query. Examples: 'day' for last 24 hours, 'week' for last 7 days, 'month' for last 30 days."
    )


class GetRecentHistoryParams(BaseModel):
    """Parameters for getting recent media consumption history"""
    
    media_type: Literal["movie", "tv_show", "music", "book", "game", "podcast", "all"] = Field(
        default="all",
        description="Type of media to retrieve. Use 'all' to get all media types."
    )
    
    time_range: Literal["day", "week", "month", "year", "all"] = Field(
        default="week",
        description="Time period to query. 'day' = last 24h, 'week' = last 7 days, 'month' = last 30 days."
    )
    
    limit: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum number of items to return. Max 200."
    )
    
    format: Literal["json", "markdown"] = Field(
        default="markdown",
        description="Response format: 'json' for structured data, 'markdown' for human-readable text."
    )
    
    include_metadata: bool = Field(
        default=True,
        description="Include additional metadata like ratings, genres, release dates."
    )


class SearchMediaParams(BaseModel):
    """Parameters for searching media in user's history"""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Search query. Can be title, artist, author, genre, or any text. Examples: 'Dune', 'Taylor Swift', 'science fiction'"
    )
    
    media_type: Literal["movie", "tv_show", "music", "book", "game", "podcast", "all"] = Field(
        default="all",
        description="Filter by media type. Use 'all' to search across all types."
    )
    
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results. Max 100."
    )
    
    format: Literal["json", "markdown"] = Field(
        default="markdown",
        description="Response format."
    )


class GetRecapParams(BaseModel):
    """Parameters for getting weekly/monthly recap"""
    
    period: Literal["week", "month"] = Field(
        default="week",
        description="Period for recap: 'week' for weekly recap, 'month' for monthly recap."
    )
    
    weeks_ago: int = Field(
        default=0,
        ge=0,
        le=52,
        description="How many weeks/months ago. 0 = current/most recent, 1 = last week/month, etc."
    )
    
    format: Literal["json", "markdown"] = Field(
        default="markdown",
        description="Response format."
    )


class GetDetailedItemParams(BaseModel):
    """Parameters for getting detailed information about a specific item"""
    
    item_id: str = Field(
        ...,
        description="Unique identifier of the media item. Get this from history or search results."
    )
    
    format: Literal["json", "markdown"] = Field(
        default="markdown",
        description="Response format."
    )


# ============================================================================
# Helper Functions
# ============================================================================

async def make_api_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[dict] = None,
    json_body: Optional[dict] = None
) -> dict[str, Any]:
    """
    Make authenticated API request to Shelf API.
    
    Args:
        endpoint: API endpoint (e.g., '/history')
        method: HTTP method
        params: Query parameters
        json_body: JSON request body
        
    Returns:
        JSON response from API
        
    Raises:
        Exception: If API request fails
    """
    if not API_KEY:
        raise ValueError(
            "SHELF_API_KEY environment variable not set. "
            "Please set your Shelf.im API key or contact team@koodos.com for DataMover API access."
        )
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Shelf-MCP-Server/1.0"
    }
    
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_body,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise Exception(
                    "Authentication failed. Please verify your SHELF_API_KEY. "
                    "If you don't have API access, contact team@koodos.com for DataMover platform access."
                )
            elif e.response.status_code == 429:
                raise Exception(
                    "Rate limit exceeded. Please wait a moment before trying again."
                )
            elif e.response.status_code == 404:
                raise Exception(
                    f"API endpoint not found: {endpoint}. "
                    "The Shelf.im API may have changed. Please check documentation or contact support."
                )
            else:
                raise Exception(f"API request failed with status {e.response.status_code}: {e.response.text}")
                
        except httpx.TimeoutException:
            raise Exception("Request timed out. The Shelf.im API may be experiencing issues.")
            
        except httpx.RequestError as e:
            raise Exception(f"Network error: {str(e)}")


def format_media_item_markdown(item: dict[str, Any]) -> str:
    """Format a single media item as markdown"""
    media_type = item.get("type", "unknown")
    title = item.get("title", "Unknown Title")
    
    lines = [f"### {title}"]
    lines.append(f"**Type:** {media_type.replace('_', ' ').title()}")
    
    if creator := item.get("creator"):
        if media_type == "music":
            lines.append(f"**Artist:** {creator}")
        elif media_type == "book":
            lines.append(f"**Author:** {creator}")
        elif media_type in ["movie", "tv_show"]:
            lines.append(f"**Director/Creator:** {creator}")
    
    if added_date := item.get("added_at"):
        lines.append(f"**Added:** {added_date}")
    
    if status := item.get("status"):
        lines.append(f"**Status:** {status}")
    
    if rating := item.get("user_rating"):
        lines.append(f"**Your Rating:** {rating}/5 ⭐")
    
    if genres := item.get("genres"):
        lines.append(f"**Genres:** {', '.join(genres)}")
    
    if progress := item.get("progress"):
        lines.append(f"**Progress:** {progress}%")
    
    if notes := item.get("notes"):
        lines.append(f"**Notes:** {notes}")
    
    return "\n".join(lines)


def format_history_markdown(items: list[dict[str, Any]], time_range: str) -> str:
    """Format history items as markdown"""
    if not items:
        return f"No media consumption found in the last {time_range}."
    
    lines = [f"# Your Shelf - Last {time_range.title()}"]
    lines.append(f"\nFound {len(items)} items:\n")
    
    # Group by media type
    by_type: dict[str, list] = {}
    for item in items:
        media_type = item.get("type", "other")
        if media_type not in by_type:
            by_type[media_type] = []
        by_type[media_type].append(item)
    
    # Format each type
    for media_type, type_items in by_type.items():
        lines.append(f"\n## {media_type.replace('_', ' ').title()} ({len(type_items)} items)")
        lines.append("")
        for item in type_items:
            lines.append(format_media_item_markdown(item))
            lines.append("")
    
    return "\n".join(lines)


def truncate_response(text: str, limit: int = CHARACTER_LIMIT) -> str:
    """Truncate response to character limit"""
    if len(text) <= limit:
        return text
    
    truncated = text[:limit - 100]
    return truncated + f"\n\n... [Response truncated at {limit} characters]"


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_recent_history(params: GetRecentHistoryParams) -> str:
    """
    Get recent media consumption history from user's Shelf.
    
    This tool retrieves what the user has been watching, reading, listening to,
    or playing recently. Perfect for understanding someone's current interests
    and cultural consumption patterns.
    
    Use cases:
    - "What have I been watching lately?"
    - "Show me my recent music listening history"
    - "What books have I read this month?"
    
    Time ranges:
    - 'day': Last 24 hours
    - 'week': Last 7 days (default)
    - 'month': Last 30 days  
    - 'year': Last 365 days
    - 'all': Complete history
    
    Args:
        params: GetRecentHistoryParams with media_type, time_range, limit, format, include_metadata
        
    Returns:
        Formatted history of media consumption. In markdown format by default,
        or JSON for structured data processing.
        
    Error handling:
        - If API key is invalid, suggests contacting team@koodos.com
        - If rate limited, advises to wait before retrying
        - If time_range returns too much data, suggests narrowing the scope
    """
    try:
        # Calculate date range
        time_ranges = {
            "day": timedelta(days=1),
            "week": timedelta(days=7),
            "month": timedelta(days=30),
            "year": timedelta(days=365),
            "all": None
        }
        
        api_params = {
            "media_type": params.media_type if params.media_type != "all" else None,
            "limit": params.limit,
            "include_metadata": params.include_metadata
        }
        
        if time_ranges[params.time_range]:
            since_date = datetime.now() - time_ranges[params.time_range]
            api_params["since"] = since_date.isoformat()
        
        # Make API request
        response = await make_api_request(
            endpoint="/history",
            params={k: v for k, v in api_params.items() if v is not None}
        )
        
        items = response.get("items", [])
        
        if params.format == "json":
            import json
            result = {
                "time_range": params.time_range,
                "media_type": params.media_type,
                "count": len(items),
                "items": items
            }
            return truncate_response(json.dumps(result, indent=2))
        else:
            return truncate_response(format_history_markdown(items, params.time_range))
            
    except Exception as e:
        return f"Error retrieving history: {str(e)}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def search_media_history(params: SearchMediaParams) -> str:
    """
    Search through user's media consumption history.
    
    Powerful search tool to find specific items, artists, genres, or topics
    in the user's Shelf history. Searches across titles, creators, genres,
    and tags.
    
    Use cases:
    - "Have I watched any Dune movies?"
    - "Find all Taylor Swift songs I've listened to"
    - "Show me science fiction books I've read"
    - "What Miyazaki films are on my shelf?"
    
    Search tips:
    - Searches are case-insensitive
    - Partial matches work (e.g., "Swift" matches "Taylor Swift")
    - Can search by genre, creator, or title
    - Use specific media_type to narrow results
    
    Args:
        params: SearchMediaParams with query, media_type, limit, format
        
    Returns:
        Matching items from user's history, formatted as markdown or JSON
        
    Error handling:
        - If no matches found, suggests broadening search or checking spelling
        - If too many matches, suggests adding media_type filter or being more specific
    """
    try:
        api_params = {
            "q": params.query,
            "media_type": params.media_type if params.media_type != "all" else None,
            "limit": params.limit
        }
        
        response = await make_api_request(
            endpoint="/search",
            params={k: v for k, v in api_params.items() if v is not None}
        )
        
        items = response.get("items", [])
        
        if not items:
            return (
                f"No results found for '{params.query}'. "
                f"Try:\n"
                f"- Broadening your search terms\n"
                f"- Checking spelling\n"
                f"- Searching without media type filter (use 'all')\n"
                f"- Using partial matches (e.g., just last name)"
            )
        
        if params.format == "json":
            import json
            result = {
                "query": params.query,
                "media_type": params.media_type,
                "count": len(items),
                "items": items
            }
            return truncate_response(json.dumps(result, indent=2))
        else:
            lines = [f"# Search Results for '{params.query}'"]
            lines.append(f"\nFound {len(items)} matching items:\n")
            
            for item in items:
                lines.append(format_media_item_markdown(item))
                lines.append("")
            
            return truncate_response("\n".join(lines))
            
    except Exception as e:
        return f"Error searching history: {str(e)}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_recap(params: GetRecapParams) -> str:
    """
    Get weekly or monthly recap of media consumption.
    
    Shelf automatically generates recaps showing what you consumed during
    a specific week or month. This is similar to Spotify Wrapped but available
    for any time period.
    
    Use cases:
    - "What was my recap this week?"
    - "Show me what I watched last month"
    - "Get my media consumption summary"
    
    Recaps include:
    - Top items consumed
    - New discoveries
    - Time spent with each media type
    - Trends and patterns
    
    Args:
        params: GetRecapParams with period ('week' or 'month'), weeks_ago offset, format
        
    Returns:
        Formatted recap with statistics and highlights
        
    Error handling:
        - If recap not available for requested period, explains when recaps are generated
        - If too far back, suggests using get_recent_history instead
    """
    try:
        api_params = {
            "period": params.period,
            "offset": params.weeks_ago
        }
        
        response = await make_api_request(
            endpoint="/recap",
            params=api_params
        )
        
        recap_data = response.get("recap", {})
        
        if not recap_data:
            offset_text = f"{params.weeks_ago} {params.period}s ago" if params.weeks_ago > 0 else f"this {params.period}"
            return (
                f"No recap available for {offset_text}. "
                f"Recaps are generated at the end of each {params.period}. "
                f"Try using get_recent_history for more recent data."
            )
        
        if params.format == "json":
            import json
            return truncate_response(json.dumps(recap_data, indent=2))
        else:
            period_name = recap_data.get("period_name", params.period)
            lines = [f"# Your Shelf Recap - {period_name}"]
            lines.append("")
            
            if summary := recap_data.get("summary"):
                lines.append(f"**Summary:** {summary}")
                lines.append("")
            
            if stats := recap_data.get("statistics"):
                lines.append("## Statistics")
                lines.append(f"- Total items consumed: {stats.get('total_items', 0)}")
                lines.append(f"- Hours watched/listened: {stats.get('total_hours', 0):.1f}")
                lines.append(f"- New discoveries: {stats.get('new_items', 0)}")
                lines.append("")
            
            if top_items := recap_data.get("top_items"):
                lines.append("## Top Items")
                for idx, item in enumerate(top_items[:5], 1):
                    lines.append(f"{idx}. {item.get('title')} ({item.get('type')})")
                lines.append("")
            
            if by_type := recap_data.get("by_type"):
                lines.append("## By Media Type")
                for media_type, count in by_type.items():
                    lines.append(f"- {media_type.replace('_', ' ').title()}: {count} items")
                lines.append("")
            
            return truncate_response("\n".join(lines))
            
    except Exception as e:
        return f"Error retrieving recap: {str(e)}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_item_details(params: GetDetailedItemParams) -> str:
    """
    Get detailed information about a specific media item on user's Shelf.
    
    Retrieves comprehensive details about a single item including user notes,
    ratings, consumption history, and metadata.
    
    Use cases:
    - "Tell me more about that movie I watched"
    - "Get details for item ID xyz123"
    - "Show me my notes on that book"
    
    Includes:
    - Full metadata (cast, genre, release date, etc.)
    - User's personal notes and ratings
    - When it was added and last updated
    - Consumption progress (for books, TV shows, games)
    - Related items or recommendations
    
    Args:
        params: GetDetailedItemParams with item_id and format
        
    Returns:
        Comprehensive item details in markdown or JSON
        
    Error handling:
        - If item_id not found, suggests using search_media_history to find the correct ID
        - If item was removed, explains and suggests alternatives
    """
    try:
        response = await make_api_request(
            endpoint=f"/items/{params.item_id}"
        )
        
        item = response.get("item", {})
        
        if not item:
            return (
                f"Item with ID '{params.item_id}' not found. "
                f"Use search_media_history to find the correct item ID."
            )
        
        if params.format == "json":
            import json
            return truncate_response(json.dumps(item, indent=2))
        else:
            lines = [f"# {item.get('title', 'Unknown Title')}"]
            lines.append("")
            
            # Basic info
            lines.append("## Basic Information")
            lines.append(f"**Type:** {item.get('type', 'unknown').replace('_', ' ').title()}")
            if creator := item.get('creator'):
                lines.append(f"**Creator:** {creator}")
            if release_date := item.get('release_date'):
                lines.append(f"**Release Date:** {release_date}")
            if genres := item.get('genres'):
                lines.append(f"**Genres:** {', '.join(genres)}")
            lines.append("")
            
            # User data
            lines.append("## Your Data")
            if added_at := item.get('added_at'):
                lines.append(f"**Added to Shelf:** {added_at}")
            if user_rating := item.get('user_rating'):
                lines.append(f"**Your Rating:** {user_rating}/5 ⭐")
            if status := item.get('status'):
                lines.append(f"**Status:** {status}")
            if progress := item.get('progress'):
                lines.append(f"**Progress:** {progress}%")
            if notes := item.get('notes'):
                lines.append(f"**Your Notes:** {notes}")
            lines.append("")
            
            # Extended metadata
            if description := item.get('description'):
                lines.append("## Description")
                lines.append(description)
                lines.append("")
            
            if cast := item.get('cast'):
                lines.append("## Cast/Contributors")
                lines.append(", ".join(cast[:10]))
                lines.append("")
            
            return truncate_response("\n".join(lines))
            
    except Exception as e:
        return f"Error retrieving item details: {str(e)}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_trending_on_shelf() -> str:
    """
    Get currently trending items across all of Shelf.
    
    Shows what's popular on Shelf right now - what other users are watching,
    reading, listening to, or playing the most. Great for discovering new content.
    
    Use cases:
    - "What's trending on Shelf right now?"
    - "Show me popular movies on Shelf"
    - "What are people listening to?"
    
    Trending data includes:
    - Most added items this week
    - Fastest growing items
    - Current cultural moments
    - Trending by category
    
    Note: This shows platform-wide trends, not just your friends or your own history.
    
    Returns:
        Formatted list of trending items with popularity metrics
        
    Error handling:
        - If trending data unavailable, explains when it's updated
    """
    try:
        response = await make_api_request(endpoint="/trending")
        
        trending_data = response.get("trending", {})
        
        if not trending_data:
            return (
                "Trending data is not currently available. "
                "Trending information is updated every few hours. Please try again later."
            )
        
        lines = ["# Trending on Shelf"]
        lines.append(f"\nUpdated: {trending_data.get('updated_at', 'Recently')}\n")
        
        if overall := trending_data.get("overall"):
            lines.append("## Overall Trending")
            for idx, item in enumerate(overall[:10], 1):
                title = item.get('title', 'Unknown')
                media_type = item.get('type', 'unknown')
                trend_score = item.get('trend_score', 0)
                lines.append(f"{idx}. **{title}** ({media_type}) - Trend Score: {trend_score}")
            lines.append("")
        
        # By category
        for category in ["movie", "tv_show", "music", "book", "game"]:
            if category_items := trending_data.get(f"trending_{category}"):
                lines.append(f"## Trending {category.replace('_', ' ').title()}s")
                for idx, item in enumerate(category_items[:5], 1):
                    lines.append(f"{idx}. {item.get('title')}")
                lines.append("")
        
        return truncate_response("\n".join(lines))
        
    except Exception as e:
        return f"Error retrieving trending data: {str(e)}"


# ============================================================================
# Server Initialization
# ============================================================================

def main():
    """Run the Shelf MCP server"""
    import asyncio
    
    # Verify API key is set
    if not API_KEY:
        print("=" * 70)
        print("⚠️  WARNING: SHELF_API_KEY environment variable not set")
        print("=" * 70)
        print("\nThis MCP server requires access to Shelf.im's API.")
        print("\nTo get started:")
        print("1. Contact team@koodos.com to request DataMover API access")
        print("2. Once approved, set your API key:")
        print("   export SHELF_API_KEY='your-api-key-here'")
        print("\nThe server will start but tools will return errors without valid credentials.")
        print("=" * 70)
        print()
    
    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
