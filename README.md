# API Contract Testing Framework

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![OpenAPI](https://img.shields.io/badge/OpenAPI-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

> Professional contract testing framework for microservices - OpenAPI 3.0 + Newman

## 🎯 Project Purpose

Comprehensive API contract testing suite ensuring API implementations match their OpenAPI specifications. Detects breaking changes before production.

## 🗂️ Project Structure
```
api-contract-testing/
├── contracts/
│   ├── openapi-specs/       # OpenAPI 3.0 specifications
│   ├── json-schemas/        # JSON Schema definitions
│   └── examples/            # Example requests/responses
├── tests/
│   ├── test_openapi_validation.py
│   └── schema_validation/
├── postman/
│   ├── collections/
│   └── environments/
└── reports/
```

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run OpenAPI validation tests
pytest tests/test_openapi_validation.py -v -s
```

## 📊 Test Coverage (Day 1)

- [x] OpenAPI spec validation
- [ ] Schema compliance testing
- [ ] Breaking change detection
- [ ] Consumer contract tests

**Status:** In Progress (Day 1/7)
```

---
