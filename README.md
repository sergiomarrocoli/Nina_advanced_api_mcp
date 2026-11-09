[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/padev1-nina-advanced-api-mcp-badge.png)](https://mseep.ai/app/padev1-nina-advanced-api-mcp)

# Nina_advanced_api_mcp
Interface for AI agents to use your astrophotography setup using N.I.N.A (Beta)
# N.I.N.A Model Context Protocol Server for Advanced API Plugin v2 (MCP)

A powerful interface for controlling N.I.N.A. (Nighttime Imaging 'N' Astronomy) software through its Advanced API [NINA Advanced API](https://github.com/christian-photo/ninaAPI) . This Model Context Protocol Server (MCP) enables AI agents to interact with NINA using tools, providing new way to interact with your setup. Usage with your own responsibility.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NINA](https://img.shields.io/badge/NINA-3.0+-green.svg)](https://nighttime-imaging.eu/)

</div>

## 🌟 Features

- **Complete Equipment Control for AI agents**
  - Cameras (capture, cooling, settings, connecting ....)
  - Mounts (slewing, parking, tracking...)
  - Focusers (movement, temperature compensation ... )
  - Filter Wheels (filter selection, info ...)
  - Domes (rotation, shutter control ...)
  - Rotators (movement, sync...)
  - ...

- **AI Integration**
  - Natural language command processing
  - Contextual help system
  - Intelligent error responses
  - Automated decision making
    
- **Most of the NINA advanced API v2 api interface endpoints supported

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NINA software with Advanced API plugin
- `uv` package manager
- AI agent with MCP support (e.g., Claude)

### Installation

1. **Install NINA Advanced API Plugin**
   ```bash
   # Install the plugins in NINA
   # Enable and configure in NINA settings
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/PaDev1/Nina_advanced_api_mcp.git
   cd nina-mcp
   ```

3. **Set Environment Variables**
   ```bash
   # Create .env file
   NINA_HOST=your_nina_host
   NINA_PORT=1888
   LOG_LEVEL=INFO
   IMAGE_SAVE_DIR=~/Desktop/NINA_Images
   ```

### Configuration

#### MCP Server Setup
Add to your AI agent's MCP configuration:
```json
{
  "mcpServers": {
    "nina_advanced_mcp_api": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp,fastapi,uvicorn,pydantic,aiohttp,requests,python-dotenv",
        "fastmcp",
        "run",
        "path/nina_advanced_mcp.py"
      ],
      "env": {
        "NINA_HOST": "NINA_IP",
        "NINA_PORT": "1888",
        "LOG_LEVEL": "INFO",
        "IMAGE_SAVE_DIR": "~/Desktop/NINA_Images"
      }
    }
  }
}
```

#### Tool profiles

By default the server lists all 106 tools, about 12,000 tokens of tool descriptions on every model turn. Set
`NINA_MCP_PROFILE` to list fewer:

| Profile | Tools | Tool list (approx.) | For |
|---|---|---|---|
| `full` (default) | 106 | 12,000 tokens | everything |
| `mono` | 39 | 4,500 tokens | `core` plus the filter wheel |
| `core` | 34 | 4,100 tokens | connecting, guiding, cooling, slewing, focusing, capturing (no filter wheel, so it suits a one-shot colour camera) |

A tool outside the profile is not listed and cannot be called. With a profile set, two extra tools are listed:
`nina_list_tool_groups` shows the hidden groups (camera, dome, rotator, flats and so on) and `nina_enable_tools` adds one
group's tools to the list, and sends the client a tool-list-changed notice. The change applies to the whole server, which over
stdio has one client. [docs/tools.md](docs/tools.md) shows which tools are in which.

## 📚 Usage

### Basic AI Examples with Claude Destop
- Connect to nina
- read the setup
- connect my camera, mount, filter wheel and guider
- read the sequesces and let me select the sequence to start

### AI Agent Commands

```plaintext
- "Take a 30-second exposure of M31"
- "Connect all equipment and start cooling the camera to -10°C"
- "Start a sequence targeting NGC 7000"
- "Get the current equipment status"
```



## 📖 API Documentation

### Core Modules

#### Equipment Control
- Camera operations
- Mount control
- Focuser management
- Filter wheel control
- Dome automation
- Rotator functions

#### Imaging
- Capture configuration
- Image processing
- File management
- Statistics gathering

#### System
- Connection handling
- Status monitoring
- Error management
- Configuration

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Detailed description
- Steps to reproduce
- Expected vs actual behavior
- System information

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NINA](https://nighttime-imaging.eu/) - The core astronomy software
- [NINA Advanced API](https://bump.sh/christian-photo/doc/advanced-api) - API documentation

## 🔗 Related Projects

- [Touch'N'Stars](https://github.com/Touch-N-Stars/Touch-N-Stars) - WebApp for Mobile Control of NINA
- [NINA Plugins](https://nighttime-imaging.eu/plugins/) - Official NINA plugin repository

