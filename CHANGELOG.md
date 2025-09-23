# Version 1.5.0
## 🔄 Provider Refactoring & RAG Agent Implementation

This version introduces a major refactoring of the provider system with a new RAG agent implementation for improved modularity and maintainability.

### 🔧 Provider Architecture

* ✅ **Refactored provider system** with new modular architecture
* ✅ **Implemented RAG agent** for enhanced retrieval capabilities
* ✅ **Improved code organization** with separated provider concerns

### 📦 Project Structure

* ✅ **Updated project metadata** with enhanced description and keywords
* ✅ **Enhanced documentation** with updated setup instructions

# Version 1.4.0
## 📢 Slack Notification System

This version introduces Slack notification integration for automated monitoring and alerting capabilities.

### 📢 Notification System

* ✅ **Added Slack notification utility** (`utils/slack_notificator.py`) for real-time monitoring alerts.
* ✅ **Integrated Slack notifications** into health check system for automated status reporting.

# Version 1.3.0
## 🔍 Health Check & Chat Session Improvements

This version introduces health check functionality and improves chat session management for better system monitoring and reliability.

### 🏥 Health Check System

* ✅ **Added comprehensive health check script** (`scripts/health_check.py`) for verifying AI Agent context and functionality.
* ✅ **Implemented health check endpoint integration** with validation logic to ensure proper system operation.
* ✅ **Added English documentation** with detailed method comments following project specifications.

### 💬 Chat Session Management

* ✅ **Enhanced session handling** in Together provider with conditional chat history storage.
* ✅ **Improved health check isolation** - health check requests no longer affect regular chat sessions.
* ✅ **Added debug logging** for better chat history monitoring and troubleshooting.

### 🔧 Development & Maintenance

* ✅ **Enhanced .gitignore** with Python bytecode file exclusion (`**/*.pyc`).
* ✅ **Version bump** to 1.3.0 reflecting new health check capabilities.
* ✅ **Improved system reliability** with better separation of health checks and regular operations.

# Version 1.2.0
## ✨ Source Synchronization & Data Management

This version introduces automated source synchronization capabilities and enhanced data management features to keep the knowledge base up-to-date automatically.

### 🔄 Source Synchronization

* ✅ **Added automated source synchronization** for real-time content updates from external sources.
* ✅ **Implemented MD5 hash comparison** to detect changes in source documents and update only modified content.
* ✅ **Added selective vector replacement** - removes obsolete vectors and adds new ones only when content changes.
* ✅ **Enhanced document tracking** with intelligent parsing and source change detection.

### 🗄️ Database & Vector Management

* ✅ **Enhanced ChromaDB utilities** with improved vector deletion and source-based filtering capabilities.
* ✅ **Improved document storage operations** with better metadata handling and retrieval performance.
* ✅ **Optimized ingestion pipeline** for more efficient document processing and vector generation.

### 🔧 Core Improvements

* ✅ **Enhanced application stability** with improved dialog handling and processing capabilities.
* ✅ **Updated AI provider integration** with better context management and response handling.
* ✅ **Refined text processing utilities** for improved chunking and content analysis.

### 📚 Documentation & Maintenance

* ✅ **Updated setup documentation** with latest installation and configuration instructions.
* ✅ **Enhanced code documentation** with improved docstrings and development guidelines.
* ✅ **Code quality improvements** with better error handling and performance optimizations.

# Version 1.1.0
## ✨ Refactor & RAG Pipeline Improvements

This PR includes a major update to the RAG-based assistant system, improving accuracy, performance, and maintainability.

### 🔧 Core Changes

* ✅ **Switched LLM to `Llama-4-Maverick`** for improved contextual reasoning and instruction-following behavior.
* ✅ **Redesigned main assistant prompt** for clarity, structure, and response consistency.
* ✅ **Added message trimming** to avoid excessive context growth over long conversations.
* ✅ **Implemented additional context getter** using a rewritten-query approach for enhanced retrieval relevance and answer completeness.

### 🧠 Semantic Chunking & Ingestion

* 🔁 Replaced text-based splitter with `MarkdownHeaderSplitter` to produce semantically meaningful chunks.
* 🧹 Removed obsolete scripts related to deprecated text ingestion logic.
* 🗂️ Updated `scraper` script to support latest HTML structure of Geomotiv.com.
* 📥 Refactored ingestion pipeline for modularity and maintainability.

### 🗃️ Storage & Structure

* 🏗️ Restructured project layout for better clarity and modularity.
* 📦 Migrated document storage from file system to **SQLite3** for lightweight persistence and faster lookups.