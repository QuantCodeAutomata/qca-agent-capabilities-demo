"""Comprehensive test suite for Analysis Microservice API endpoints."""

import pytest
from datetime import datetime
from fastapi import status
import json


class TestRootEndpoint:
    """Test cases for root endpoint (/)."""
    
    def test_root_endpoint_success(self, client):
        """Test that root endpoint returns welcome message and API info."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["version"] == "1.0.0"
        assert "/health" in str(data["endpoints"])
        
    def test_root_endpoint_content_type(self, client):
        """Test that root endpoint returns JSON content type."""
        response = client.get("/")
        
        assert "application/json" in response.headers["content-type"]


class TestHealthEndpoint:
    """Test cases for health check endpoint (/health)."""
    
    def test_health_check_success(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"
        
    def test_health_check_timestamp_format(self, client):
        """Test that health endpoint returns valid ISO timestamp."""
        response = client.get("/health")
        data = response.json()
        
        timestamp_str = data["timestamp"]
        parsed_timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        assert isinstance(parsed_timestamp, datetime)
        
    def test_health_check_response_schema(self, client):
        """Test that health response matches expected schema."""
        response = client.get("/health")
        data = response.json()
        
        assert set(data.keys()) == {"status", "timestamp"}
        assert isinstance(data["status"], str)
        assert isinstance(data["timestamp"], str)
        
    def test_health_check_multiple_requests(self, client):
        """Test that multiple health checks return consistent results."""
        responses = [client.get("/health") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["status"] == "healthy"
            
    def test_health_check_wrong_method(self, client):
        """Test that health endpoint rejects non-GET methods."""
        response = client.post("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestAnalyzeEndpoint:
    """Test cases for data analysis endpoint (/analyze)."""
    
    def test_analyze_success_with_metadata(self, client, sample_analysis_data):
        """Test successful analysis with complete data and metadata."""
        response = client.post("/analyze", json=sample_analysis_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert "id" in data
        assert "status" in data
        assert "message" in data
        assert "timestamp" in data
        assert data["status"] == "success"
        assert len(data["id"]) > 0
        
    def test_analyze_success_without_metadata(self, client, sample_analysis_data_no_metadata):
        """Test successful analysis with data but no metadata."""
        response = client.post("/analyze", json=sample_analysis_data_no_metadata)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["status"] == "success"
        assert "id" in data
        
    def test_analyze_with_nested_data(self, client, nested_data_payload):
        """Test analysis with complex nested data structures."""
        response = client.post("/analyze", json=nested_data_payload)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        
    def test_analyze_empty_data_dict(self, client, empty_data_payload):
        """Test that empty data dictionary is rejected."""
        response = client.post("/analyze", json=empty_data_payload)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        assert "empty" in data["detail"].lower()
        
    def test_analyze_missing_data_field(self, client):
        """Test that request without data field is rejected."""
        response = client.post("/analyze", json={"metadata": {"source": "test"}})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_analyze_invalid_json(self, client):
        """Test that malformed JSON is rejected."""
        response = client.post(
            "/analyze",
            data="{'invalid': json}",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_analyze_null_data_field(self, client):
        """Test that null data field is rejected."""
        response = client.post("/analyze", json={"data": None})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_analyze_data_not_dict(self, client):
        """Test that non-dictionary data is rejected."""
        response = client.post("/analyze", json={"data": "string_value"})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_analyze_metadata_not_dict(self, client):
        """Test that non-dictionary metadata is rejected."""
        response = client.post("/analyze", json={
            "data": {"value": 42},
            "metadata": "invalid"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_analyze_multiple_requests(self, client, multiple_analysis_records):
        """Test multiple consecutive analysis requests."""
        response_ids = []
        
        for record in multiple_analysis_records:
            response = client.post("/analyze", json=record)
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["status"] == "success"
            response_ids.append(data["id"])
        
        assert len(response_ids) == len(multiple_analysis_records)
        assert len(set(response_ids)) == len(response_ids)
        
    def test_analyze_response_schema(self, client, sample_analysis_data):
        """Test that analyze response matches expected schema."""
        response = client.post("/analyze", json=sample_analysis_data)
        data = response.json()
        
        required_fields = {"id", "status", "message", "timestamp"}
        assert set(data.keys()) == required_fields
        
        assert isinstance(data["id"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
        
    def test_analyze_unique_ids(self, client, sample_analysis_data):
        """Test that each analysis receives a unique ID."""
        ids = []
        for _ in range(10):
            response = client.post("/analyze", json=sample_analysis_data)
            data = response.json()
            ids.append(data["id"])
        
        assert len(set(ids)) == 10
        
    def test_analyze_timestamp_format(self, client, sample_analysis_data):
        """Test that analysis timestamp is in valid ISO format."""
        response = client.post("/analyze", json=sample_analysis_data)
        data = response.json()
        
        timestamp_str = data["timestamp"]
        parsed_timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        assert isinstance(parsed_timestamp, datetime)
        
    def test_analyze_wrong_method(self, client):
        """Test that analyze endpoint rejects non-POST methods."""
        response = client.get("/analyze")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
    def test_analyze_empty_request_body(self, client):
        """Test that completely empty request body is rejected."""
        response = client.post("/analyze", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_analyze_large_data_payload(self, client):
        """Test analysis with large data payload."""
        large_data = {
            "data": {f"field_{i}": f"value_{i}" for i in range(1000)},
            "metadata": {"size": "large"}
        }
        response = client.post("/analyze", json=large_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "success"
        
    def test_analyze_special_characters_in_data(self, client):
        """Test analysis with special characters in data."""
        special_data = {
            "data": {
                "text": "Hello 你好 🌍 @#$%^&*()",
                "unicode": "Ñoño",
                "quotes": 'He said "hello"'
            }
        }
        response = client.post("/analyze", json=special_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "success"
        
    def test_analyze_numeric_values(self, client):
        """Test analysis with various numeric types."""
        numeric_data = {
            "data": {
                "integer": 42,
                "float": 3.14159,
                "negative": -100,
                "zero": 0,
                "large": 9999999999,
                "scientific": 1.23e-10
            }
        }
        response = client.post("/analyze", json=numeric_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "success"
        
    def test_analyze_boolean_values(self, client):
        """Test analysis with boolean values."""
        bool_data = {
            "data": {
                "enabled": True,
                "disabled": False,
                "flag": True
            }
        }
        response = client.post("/analyze", json=bool_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "success"
        
    def test_analyze_array_values(self, client):
        """Test analysis with array values in data."""
        array_data = {
            "data": {
                "readings": [1, 2, 3, 4, 5],
                "tags": ["sensor", "production"],
                "mixed": [1, "two", 3.0, True, None]
            }
        }
        response = client.post("/analyze", json=array_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "success"


class TestReportEndpoint:
    """Test cases for report endpoint (/report)."""
    
    def test_report_empty_storage(self, client):
        """Test report endpoint with no stored records."""
        response = client.get("/report")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "total_records" in data
        assert "records" in data
        assert data["total_records"] == 0
        assert data["records"] == []
        
    def test_report_with_single_record(self, client, sample_analysis_data):
        """Test report endpoint after storing one record."""
        analyze_response = client.post("/analyze", json=sample_analysis_data)
        assert analyze_response.status_code == status.HTTP_201_CREATED
        
        report_response = client.get("/report")
        assert report_response.status_code == status.HTTP_200_OK
        
        data = report_response.json()
        assert data["total_records"] == 1
        assert len(data["records"]) == 1
        
        record = data["records"][0]
        assert "id" in record
        assert "data" in record
        assert "timestamp" in record
        assert "status" in record
        
    def test_report_with_multiple_records(self, client, multiple_analysis_records):
        """Test report endpoint with multiple stored records."""
        for record_data in multiple_analysis_records:
            response = client.post("/analyze", json=record_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        report_response = client.get("/report")
        data = report_response.json()
        
        assert data["total_records"] == len(multiple_analysis_records)
        assert len(data["records"]) == len(multiple_analysis_records)
        
    def test_report_response_schema(self, client, sample_analysis_data):
        """Test that report response matches expected schema."""
        client.post("/analyze", json=sample_analysis_data)
        response = client.get("/report")
        data = response.json()
        
        assert set(data.keys()) == {"total_records", "records"}
        assert isinstance(data["total_records"], int)
        assert isinstance(data["records"], list)
        
    def test_report_record_contains_original_data(self, client, sample_analysis_data):
        """Test that report contains the original data submitted."""
        client.post("/analyze", json=sample_analysis_data)
        
        report_response = client.get("/report")
        data = report_response.json()
        
        stored_record = data["records"][0]
        assert stored_record["data"] == sample_analysis_data["data"]
        
    def test_report_record_contains_metadata(self, client, sample_analysis_data):
        """Test that report contains metadata when provided."""
        client.post("/analyze", json=sample_analysis_data)
        
        report_response = client.get("/report")
        data = report_response.json()
        
        stored_record = data["records"][0]
        assert "metadata" in stored_record
        assert stored_record["metadata"] == sample_analysis_data["metadata"]
        
    def test_report_record_schema_validation(self, client, sample_analysis_data):
        """Test that each record in report has required fields."""
        client.post("/analyze", json=sample_analysis_data)
        
        report_response = client.get("/report")
        data = report_response.json()
        
        for record in data["records"]:
            required_fields = {"id", "data", "timestamp", "status"}
            assert required_fields.issubset(set(record.keys()))
            
    def test_report_preserves_data_order(self, client, multiple_analysis_records):
        """Test that report returns records in order."""
        submitted_ids = []
        
        for record_data in multiple_analysis_records:
            response = client.post("/analyze", json=record_data)
            submitted_ids.append(response.json()["id"])
        
        report_response = client.get("/report")
        data = report_response.json()
        
        reported_ids = [record["id"] for record in data["records"]]
        assert reported_ids == submitted_ids
        
    def test_report_wrong_method(self, client):
        """Test that report endpoint rejects non-GET methods."""
        response = client.post("/report")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
    def test_report_multiple_requests_consistency(self, client, sample_analysis_data):
        """Test that multiple report requests return consistent data."""
        client.post("/analyze", json=sample_analysis_data)
        
        report1 = client.get("/report").json()
        report2 = client.get("/report").json()
        report3 = client.get("/report").json()
        
        assert report1 == report2 == report3


class TestDataPersistence:
    """Test cases for data persistence across endpoints."""
    
    def test_data_persists_between_requests(self, client, sample_analysis_data):
        """Test that analyzed data persists and can be retrieved."""
        analyze_response = client.post("/analyze", json=sample_analysis_data)
        analysis_id = analyze_response.json()["id"]
        
        report_response = client.get("/report")
        records = report_response.json()["records"]
        
        assert len(records) == 1
        assert records[0]["id"] == analysis_id
        
    def test_multiple_analyses_accumulate(self, client, multiple_analysis_records):
        """Test that multiple analyses accumulate in storage."""
        for i, record_data in enumerate(multiple_analysis_records, 1):
            client.post("/analyze", json=record_data)
            
            report = client.get("/report").json()
            assert report["total_records"] == i
            
    def test_data_isolation_between_tests(self, client):
        """Test that storage is clean at test start."""
        report = client.get("/report").json()
        assert report["total_records"] == 0
        assert report["records"] == []


class TestAPIContract:
    """Test cases for API contract validation."""
    
    def test_content_type_json(self, client, sample_analysis_data):
        """Test that API returns JSON content type."""
        endpoints = [
            ("get", "/health"),
            ("post", "/analyze", sample_analysis_data),
            ("get", "/report")
        ]
        
        for method, *args in endpoints:
            if method == "get":
                response = client.get(args[0])
            else:
                response = client.post(args[0], json=args[1])
            
            assert "application/json" in response.headers["content-type"]
            
    def test_cors_headers_present(self, client):
        """Test for CORS headers if needed."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        
    def test_error_responses_have_detail(self, client):
        """Test that error responses contain detail field."""
        response = client.post("/analyze", json={"data": {}})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        
    def test_404_for_unknown_endpoint(self, client):
        """Test that unknown endpoints return 404."""
        response = client.get("/unknown/endpoint")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_method_not_allowed_returns_405(self, client):
        """Test that wrong HTTP methods return 405."""
        response = client.delete("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_concurrent_analyze_requests(self, client, sample_analysis_data):
        """Test handling of rapid consecutive requests."""
        responses = []
        for _ in range(20):
            response = client.post("/analyze", json=sample_analysis_data)
            responses.append(response)
        
        assert all(r.status_code == status.HTTP_201_CREATED for r in responses)
        
        ids = [r.json()["id"] for r in responses]
        assert len(set(ids)) == 20
        
        report = client.get("/report").json()
        assert report["total_records"] == 20
        
    def test_very_deep_nested_structure(self, client):
        """Test with deeply nested data structure."""
        deep_data = {"data": {"level": 1}}
        current = deep_data["data"]
        
        for i in range(2, 11):
            current["nested"] = {"level": i}
            current = current["nested"]
        
        response = client.post("/analyze", json=deep_data)
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_empty_string_values(self, client):
        """Test with empty string values in data."""
        data = {
            "data": {
                "empty": "",
                "whitespace": "   ",
                "valid": "value"
            }
        }
        response = client.post("/analyze", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_null_values_in_data(self, client):
        """Test with null values in data fields."""
        data = {
            "data": {
                "value": 42,
                "nullable": None,
                "exists": True
            }
        }
        response = client.post("/analyze", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_data_with_single_key(self, client):
        """Test with minimal data structure."""
        data = {"data": {"x": 1}}
        response = client.post("/analyze", json=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_metadata_without_data_fails(self, client):
        """Test that metadata alone without data fails."""
        response = client.post("/analyze", json={"metadata": {"source": "test"}})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_extra_fields_in_request(self, client):
        """Test request with extra unexpected fields."""
        data = {
            "data": {"value": 42},
            "metadata": {"source": "test"},
            "extra_field": "should_be_ignored"
        }
        response = client.post("/analyze", json=data)
        assert response.status_code == status.HTTP_201_CREATED


class TestErrorHandling:
    """Test cases for error handling and validation."""
    
    def test_malformed_json_syntax(self, client):
        """Test handling of syntactically invalid JSON."""
        response = client.post(
            "/analyze",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    def test_missing_content_type_header(self, client):
        """Test request without content-type header."""
        response = client.post(
            "/analyze",
            data='{"data": {"value": 42}}'
        )
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        ]
        
    def test_empty_metadata_is_valid(self, client):
        """Test that empty metadata dict is acceptable."""
        data = {
            "data": {"value": 42},
            "metadata": {}
        }
        response = client.post("/analyze", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_analyze_with_list_instead_of_object(self, client):
        """Test that list data type is rejected."""
        response = client.post("/analyze", json={"data": [1, 2, 3]})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestIntegrationScenarios:
    """Integration test scenarios combining multiple operations."""
    
    def test_full_workflow(self, client, sample_analysis_data):
        """Test complete workflow: health check, analyze, report."""
        health = client.get("/health")
        assert health.status_code == status.HTTP_200_OK
        assert health.json()["status"] == "healthy"
        
        analyze = client.post("/analyze", json=sample_analysis_data)
        assert analyze.status_code == status.HTTP_201_CREATED
        analysis_id = analyze.json()["id"]
        
        report = client.get("/report")
        assert report.status_code == status.HTTP_200_OK
        assert report.json()["total_records"] == 1
        assert report.json()["records"][0]["id"] == analysis_id
        
    def test_mixed_data_types_workflow(self, client):
        """Test workflow with various data types."""
        test_cases = [
            {"data": {"type": "numeric", "value": 42}},
            {"data": {"type": "string", "value": "hello"}},
            {"data": {"type": "boolean", "value": True}},
            {"data": {"type": "array", "value": [1, 2, 3]}},
            {"data": {"type": "nested", "value": {"inner": "data"}}}
        ]
        
        for test_data in test_cases:
            response = client.post("/analyze", json=test_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        report = client.get("/report")
        assert report.json()["total_records"] == len(test_cases)
        
    def test_analyze_and_verify_storage(self, client, nested_data_payload):
        """Test that analyzed data is correctly stored and retrievable."""
        analyze_response = client.post("/analyze", json=nested_data_payload)
        analysis_id = analyze_response.json()["id"]
        
        report = client.get("/report").json()
        stored_record = next(r for r in report["records"] if r["id"] == analysis_id)
        
        assert stored_record["data"] == nested_data_payload["data"]
        assert stored_record["metadata"] == nested_data_payload["metadata"]
        assert stored_record["status"] == "processed"
