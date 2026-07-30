import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestVectorStoreAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_chroma_health_check(self):
        """Test ChromaDB vector store health check endpoint."""
        response = self.client.get("/api/v1/vector-store/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("mode", data)
        self.assertIn("collections_count", data)
        self.assertIsInstance(data["collections_count"], int)

    def test_chroma_add_and_query_flow(self):
        """Test adding documents, querying vector store, and cleaning up."""
        collection_name = "test_health_collection"
        
        # 1. Add document
        add_payload = {
            "collection_name": collection_name,
            "documents": [
                {
                    "id": "doc1",
                    "content": "ChromaDB health check test document",
                    "metadata": {"category": "test"}
                }
            ]
        }
        add_response = self.client.post("/api/v1/vector-store/add", json=add_payload)
        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.json()["added_count"], 1)

        # 2. Query document
        query_payload = {
            "collection_name": collection_name,
            "query_texts": ["health check test"],
            "n_results": 1
        }
        query_response = self.client.post("/api/v1/vector-store/query", json=query_payload)
        self.assertEqual(query_response.status_code, 200)
        query_data = query_response.json()
        self.assertEqual(query_data["collection_name"], collection_name)
        self.assertGreater(len(query_data["results"]), 0)

        # 3. Clean up collection
        delete_response = self.client.delete(f"/api/v1/vector-store/collections/{collection_name}")
        self.assertEqual(delete_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
