# Shelf MCP Server - Smithery Deployment Guide

[![Smithery](https://img.shields.io/badge/Smithery-MCP%20Server-blue)](https://smithery.ai)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-v1.0-green)](https://github.com/modelcontextprotocol/python-sdk)

Personal Engine for AI Cultural Discovery - Access your Shelf.im media consumption data through MCP.

## 🌟 What is Shelf MCP Server?

The Shelf MCP Server enables AI assistants to access your personal cultural consumption data from [Shelf.im](https://shelf.im) - including movies, TV shows, music, books, and games you've watched, listened to, or played.

### Key Features

- 🎬 **Media History** - Access your complete consumption history
- 🔍 **Smart Search** - Search across all your media
- 📊 **Recaps** - Get weekly/monthly summaries
- 📈 **Trending** - Discover what's popular on Shelf
- 🎯 **Personalized** - AI understands your cultural tastes

### 5 MCP Tools

1. `get_recent_history` - Retrieve recent media consumption
2. `search_media_history` - Search your history
3. `get_recap` - Get weekly/monthly recaps
4. `get_item_details` - Detailed item information
5. `get_trending_on_shelf` - Platform-wide trends

---

## 📦 Installation via Smithery

### Quick Install

```bash
# Install via Smithery CLI
npx @smithery/cli install shelf --client claude

# Or for other clients
npx @smithery/cli install shelf --client cursor
```

### Configuration

When prompted, provide:

1. **Shelf API Key** (required)
   - Contact team@koodos.com to request access
   - The API is currently in early access

2. **API Base URL** (optional)
   - Defaults to `https://api.shelf.im/v1`
   - Only change if using a custom endpoint

### Verification

After installation, verify the server is working:

```bash
# List installed servers
smithery list --client claude

# Check if shelf is listed and active
```

---

## 🔑 Getting API Access

⚠️ **Important:** Shelf.im's API is currently in **early access**.

### Request Access

1. **Email:** team@koodos.com
2. **Subject:** "Shelf API Access for MCP Server"
3. **Include:**
   - Your use case
   - Why you want to build with Shelf
   - Your technical background

### Template Email

```
Subject: Shelf API Access for MCP Server

Hello Koodos Team,

I would like to request access to the Shelf.im / DataMover API to use 
with the Shelf MCP Server on Smithery.

Use Case: [Describe how you'll use the API]
Background: [Your technical experience]

I understand the API is in early access and I'm excited to help test 
and provide feedback.

Thank you!
[Your name]
```

### Timeline

- Response time: Usually 3-7 business days
- Koodos is a small team, so please be patient
- Follow up politely after 1 week if no response

---

## 💡 Usage Examples

Once installed, you can ask your AI assistant:

### Basic Queries
```
"What did I watch on Shelf this week?"
"Show me my recent music history"
"What books have I read this month?"
```

### Advanced Analysis
```
"Analyze my music taste over the last 3 months"
"Find all sci-fi movies I've watched"
"Compare my current interests with last month"
```

### Personalized Recommendations
```
"Based on my Shelf history, recommend a movie for tonight"
"Suggest books similar to what I've been reading"
"What's trending that matches my taste?"
```

---

## 🏗️ Deploying Your Own

Want to deploy a modified version or contribute?

### Prerequisites

- Python 3.10+
- Shelf API key
- Smithery account ([smithery.ai](https://smithery.ai))

### Steps

1. **Fork the Repository**
   ```bash
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/shelf-mcp-server
   cd shelf-mcp-server
   ```

2. **Test Locally**
   ```bash
   # Install dependencies
   pip install -r requirements.txt

   # Set API key
   export SHELF_API_KEY="your-key-here"

   # Run HTTP server (default transport for Smithery)
   python shelf_mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8000

   # Or run via stdio when testing with the MCP CLI locally
   python shelf_mcp_server.py --transport stdio
   ```

3. **Deploy to Smithery**
   ```bash
   # Login to Smithery
   npx @smithery/cli login
   
   # Deploy
   npx @smithery/cli deploy
   ```

### Configuration Files

- `smithery.yaml` - Smithery configuration
- `Dockerfile` - Container definition
- `requirements.txt` - Python dependencies

---

## 🔧 Configuration Schema

The server accepts the following configuration:

```json
{
  "shelfApiKey": {
    "type": "string",
    "required": true,
    "description": "Your Shelf API key"
  },
  "apiBaseUrl": {
    "type": "string",
    "required": false,
    "default": "https://api.shelf.im/v1",
    "description": "API base URL"
  }
}
```

---

## 🛠️ Troubleshooting

### "Authentication failed"

**Problem:** Invalid or missing API key

**Solution:**
1. Verify your API key is correct
2. Check that you have API access from Koodos
3. Try reinstalling: `smithery uninstall shelf && smithery install shelf`

### "Connection timeout"

**Problem:** Cannot reach Shelf API

**Solution:**
1. Check your internet connection
2. Verify Shelf.im is operational
3. Check if API base URL is correct

### "No data returned"

**Problem:** Empty responses from tools

**Solution:**
1. Ensure you have media in your Shelf
2. Try with a broader time range
3. Check API key permissions

### Getting Help

- **Smithery Discord:** [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- **Shelf Support:** team@koodos.com
- **GitHub Issues:** [Create an issue](https://github.com/YOUR_USERNAME/shelf-mcp-server/issues)

---

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| Recent History | Access consumption history | ✅ Ready |
| Search | Search across all media | ✅ Ready |
| Recaps | Weekly/monthly summaries | ✅ Ready |
| Item Details | Detailed media information | ✅ Ready |
| Trending | Platform-wide trends | ✅ Ready |
| Social | Friends' activities | 🚧 Planned |
| Recommendations | ML-based suggestions | 🚧 Planned |

---

## 🔒 Privacy & Security

### Data Handling

- **API Key Security:** Keys are stored locally, never on Smithery servers
- **Read-Only Access:** Server only reads data, never modifies
- **No Data Storage:** No caching of your Shelf data
- **HTTPS Only:** All API communication encrypted

### Smithery Privacy

According to [Smithery's Data Policy](https://smithery.ai/privacy):
- Configuration data is ephemeral
- No persistent storage of API keys
- Anonymous usage tracking (opt-in)
- Developer-owned servers maintain control

---

## 🤝 Contributing

We welcome contributions!

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/shelf-mcp-server

# Install dev dependencies
pip install -r requirements.txt

# Run tests
python test_installation.py

# Test locally with Smithery CLI
smithery dev
```

---

## 📚 Resources

### Official Links

- **Shelf.im:** https://www.shelf.im
- **Koodos Labs:** https://koodos.com
- **DataMover:** https://datamover.org
- **Smithery:** https://smithery.ai

### Documentation

- **MCP Protocol:** https://modelcontextprotocol.io
- **Smithery Docs:** https://smithery.ai/docs
- **Python SDK:** https://github.com/modelcontextprotocol/python-sdk

### Community

- **Smithery Discord:** [Join](https://discord.gg/Afd38S5p9A)
- **MCP Community:** [GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **Anthropic** - For the Model Context Protocol
- **Koodos Labs** - For Shelf.im and DataMover
- **Smithery** - For MCP server hosting platform
- **Community** - For feedback and contributions

---

## ⭐ Star History

If you find this useful, please consider starring the repository!

---

**Built with ❤️ for the Shelf.im and MCP communities**

*Version 1.0 | Last updated: November 2025*
