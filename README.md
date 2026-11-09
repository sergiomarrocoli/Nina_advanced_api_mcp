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

## 📈 Measured improvements

Most changes in this fork came from running language models against the server in the
[NINA MCP benchmark](https://github.com/sergiomarrocoli/NINA-MCP-model-benchmarking) (simulated equipment, 17 tasks, logged and scored runs),
reading where they failed, and fixing the tool. The method, run logs and charts are in that repo. The numbers below are passes out of
5 runs unless stated; the "before" is the server this fork started from (v1).

| Change | Model | Task | Before | After |
|---|---|---|---|---|
| RA units (`ra`, `ra_degrees`, `ra_hms`) and filter names | qwen3:8b | Change filter to Red | 0/5 | 5/5 |
| Clearer argument errors and a `count` argument on `nina_capture_image` | qwen3:8b | M31 session | 0/5 | 3/5 |
| The same, plus the units fix | qwen3:8b | Pointing offset | 1/8 | 5/5 |
| Below-horizon refusal in `nina_slew_mount` | qwen3:8b, deepseek-chat, DeepSeek V4 Pro, gpt-4.1, Claude Haiku 5.5 | Slew to a target that never rises | 0/5 each | 5/5 each |

What the changes were and why: [units, errors and count](https://github.com/sergiomarrocoli/NINA-MCP-model-benchmarking/blob/main/docs/units-and-capture.md),
[the horizon check](https://github.com/sergiomarrocoli/NINA-MCP-model-benchmarking/blob/main/docs/horizon-check.md).

**Tool profiles do not change accuracy.** Trimming the tool list from about 12,000 tokens to about 4,500 (`mono`) or 4,100 (`core`) gave
the same pass rate as the full list on qwen3:8b: 36 of 45 valid runs on `full` and on `mono`, 27 of 30 on `core` (its easier subset). The saving is
cost and speed. [Details](https://github.com/sergiomarrocoli/NINA-MCP-model-benchmarking/blob/main/docs/tool-profiles.md).

**Read these with care.**
- Mostly one small local model, small samples (5 runs per cell), and the simulator sometimes drops a device mid-run.
- The `count` argument makes the tool easier for weak models, so results with it are not comparable to the v1 numbers.
- The below-horizon refusal shows a server-side check works where model judgement does not. The models did not get better; the tool decided.
- Not yet measured: the centring-failure message, autofocus and centre-on-target tools, and tool discovery.

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

