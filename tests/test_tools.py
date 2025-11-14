"""Test suite for tool functions with mocking for external APIs."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import httpx
from typing import List

from agents.tools import (
    search_brave_api,
    validate_search_query,
    format_search_results,
    extract_key_insights,
    RateLimiter,
    retry_with_backoff,
    RetryConfig
)
from agents.models import SearchResult


@pytest.fixture
def sample_search_results():
    """Create sample search results for testing."""
    return [
        SearchResult(
            title="AI Agents Overview",
            url="https://example.com/ai-agents",
            description="Comprehensive guide to AI agents and their applications",
            score=0.95
        ),
        SearchResult(
            title="Machine Learning Basics",
            url="https://example.com/ml-basics", 
            description="Introduction to machine learning concepts",
            score=0.87
        ),
        SearchResult(
            title="Future of AI",
            url="https://example.com/ai-future",
            description="Predictions and trends in artificial intelligence",
            score=0.82
        )
    ]


class TestSearchQueryValidation:
    """Test search query validation."""
    
    def test_valid_query(self):
        """Test validation of valid queries."""
        query = "AI agents and machine learning"
        result = validate_search_query(query)
        assert result.query == query
        assert result.max_results > 0
    
    def test_empty_query(self):
        """Test validation fails for empty queries."""
        with pytest.raises(ValueError, match="Query must be a non-empty string"):
            validate_search_query("")
    
    def test_whitespace_cleanup(self):
        """Test that extra whitespace is cleaned up."""
        query = "  AI   agents   "
        result = validate_search_query(query)
        assert result.query == "AI agents"
    
    def test_long_query(self):
        """Test validation fails for overly long queries."""
        long_query = "a" * 501  # Exceeds 500 character limit
        with pytest.raises(ValueError, match="Query is too long"):
            validate_search_query(long_query)


class TestBraveAPISearch:
    """Test Brave API search functionality with mocking."""
    
    @pytest.mark.asyncio
    async def test_successful_search(self):
        """Test successful API search with mocked response."""
        
        mock_response_data = {
            "web": {
                "results": [
                    {
                        "title": "AI Agents Guide",
                        "url": "https://example.com/guide",
                        "description": "Complete guide to AI agents",
                        "score": 0.95
                    }
                ]
            }
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            # Mock the async context manager and response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            results = await search_brave_api(
                query="AI agents",
                api_key="test_key",
                max_results=5
            )
            
            assert len(results) == 1
            assert results[0].title == "AI Agents Guide"
            assert results[0].url == "https://example.com/guide"
            assert results[0].score == 0.95
    
    @pytest.mark.asyncio
    async def test_api_key_validation(self):
        """Test API key validation."""
        
        with pytest.raises(ValueError, match="API key is required"):
            await search_brave_api("test query", "")
    
    @pytest.mark.asyncio
    async def test_query_validation(self):
        """Test query validation in search function."""
        
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await search_brave_api("", "test_key")
    
    @pytest.mark.asyncio
    async def test_max_results_validation(self):
        """Test max_results parameter validation."""
        
        with pytest.raises(ValueError, match="max_results must be between 1 and 50"):
            await search_brave_api("test", "key", max_results=0)
        
        with pytest.raises(ValueError, match="max_results must be between 1 and 50"):
            await search_brave_api("test", "key", max_results=51)
    
    @pytest.mark.asyncio
    async def test_http_error_handling(self):
        """Test handling of HTTP errors."""
        
        with patch('httpx.AsyncClient') as mock_client:
            # Mock 401 unauthorized error
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.request = Mock()
            
            mock_get = AsyncMock()
            mock_get.side_effect = httpx.HTTPStatusError(
                "Unauthorized", 
                request=mock_response.request, 
                response=mock_response
            )
            
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            with pytest.raises(httpx.HTTPStatusError):
                await search_brave_api("test", "invalid_key")

    @pytest.mark.asyncio
    async def test_empty_results(self):
        """Test handling of empty search results."""
        
        mock_response_data = {"web": {"results": []}}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            results = await search_brave_api("nonexistent topic", "test_key")
            
            assert len(results) == 0


class TestResultFormatting:
    """Test result formatting functions."""
    
    def test_format_search_results(self, sample_search_results):
        """Test formatting of search results."""
        
        formatted = format_search_results(sample_search_results, "AI agents")
        
        assert "AI agents" in formatted
        assert "3 results" in formatted
        assert "AI Agents Overview" in formatted
        assert "https://example.com/ai-agents" in formatted
    
    def test_format_empty_results(self):
        """Test formatting of empty results."""
        
        formatted = format_search_results([], "nonexistent")
        
        assert "No search results found" in formatted
        assert "nonexistent" in formatted
    
    @pytest.mark.asyncio
    async def test_extract_key_insights(self, sample_search_results):
        """Test extraction of key insights from results."""
        
        insights = await extract_key_insights(sample_search_results, max_insights=5)
        
        assert len(insights) <= 5
        assert any("3 relevant sources" in insight for insight in insights)
        assert any("multiple independent sources" in insight for insight in insights)
    
    @pytest.mark.asyncio
    async def test_extract_insights_empty_results(self):
        """Test insight extraction with empty results."""
        
        insights = await extract_key_insights([], max_insights=3)
        
        assert len(insights) == 1
        assert "No search results available" in insights[0]


class TestRateLimiter:
    """Test rate limiting functionality."""
    
    def test_rate_limiter_creation(self):
        """Test rate limiter initialization."""
        
        limiter = RateLimiter(max_calls=10, time_window=60)
        
        assert limiter.max_calls == 10
        assert limiter.time_window == 60
        assert len(limiter.calls) == 0
    
    def test_can_make_request_initially(self):
        """Test that requests are allowed initially."""
        
        limiter = RateLimiter(max_calls=5, time_window=60)
        
        assert limiter.can_make_request() == True
    
    def test_rate_limit_exceeded(self):
        """Test rate limit enforcement."""
        
        limiter = RateLimiter(max_calls=2, time_window=60)
        
        # Make maximum requests
        limiter.record_request()
        limiter.record_request()
        
        assert limiter.can_make_request() == False
    
    @pytest.mark.asyncio
    async def test_wait_if_needed(self):
        """Test waiting behavior when not rate limited."""
        
        limiter = RateLimiter(max_calls=5, time_window=60)  # Allow multiple calls
        
        # Record one request - still under limit
        limiter.record_request()
        
        # Should not need to wait since we're under the limit
        import time
        start_time = time.time()
        await limiter.wait_if_needed()
        end_time = time.time()
        
        # Should be very quick if not waiting
        assert (end_time - start_time) < 1.0


class TestRetryLogic:
    """Test retry logic with exponential backoff."""
    
    @pytest.mark.asyncio
    async def test_successful_operation_no_retry(self):
        """Test that successful operations don't retry."""
        
        async def success_func():
            return "success"
        
        result = await retry_with_backoff(success_func)
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_on_failure(self):
        """Test retry behavior on failures."""
        
        call_count = 0
        
        async def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise httpx.RequestError("Network error")
            return "success after retries"
        
        retry_config = RetryConfig(max_retries=3, base_delay=0.01)  # Very short delay for testing
        
        result = await retry_with_backoff(
            failing_func,
            retry_config=retry_config
        )
        
        assert result == "success after retries"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self):
        """Test behavior when max retries are exceeded."""
        
        async def always_failing_func():
            raise httpx.RequestError("Persistent error")
        
        retry_config = RetryConfig(max_retries=2, base_delay=0.01)
        
        with pytest.raises(httpx.RequestError, match="Persistent error"):
            await retry_with_backoff(
                always_failing_func,
                retry_config=retry_config
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])