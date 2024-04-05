# GoldenSource Market - Core

## Overview

The Core extension serves as the foundational component of the GoldenSource Market. It encapsulates essential functionalities and serves as an infrastructural base for other extensions. This extension is vital for maintaining the integrity and standardization of the platform.

## Key Features

- **Standardized Data Model** (`Data` Class): A flexible and dynamic Pydantic model capable of handling various data structures.
- **Standardized Query Params** (`QueryParams` Class): A Pydantic model for handling querying to different providers.
- **Dynamic Field Support**: Enables handling of undefined fields, providing versatility in data processing.
- **Robust Data Validation**: Utilizes Pydantic's validation features to ensure data integrity.
- **API Routing Mechanism** (`Router` Class): Simplifies the process of defining API routes and endpoints - out of the box Python and Web endpoints.

## Getting Started

### Prerequisites

- Python 3.8 or higher.
- Familiarity with FastAPI and Pydantic.