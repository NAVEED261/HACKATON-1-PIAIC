# MCP (Model Context Protocol) Setup Guide

## Overview
This project is configured with MCP servers to enhance Claude Code's capabilities. The configuration has been updated to work with your hackathon project.

## Configured MCP Servers

### 1. **Filesystem Server** ✅ (Ready to use)
- **Purpose**: Allows Claude to access and work with files in your project
- **Path**: `D:\PIAIC HACKATON PRACTICE\hackaton_1`
- **Status**: Configured and ready
- **No additional setup required**

### 2. **Memory Server** ✅ (Ready to use)
- **Purpose**: Maintains context and memory across conversations
- **Status**: Configured and ready
- **No additional setup required**

### 3. **GitHub Server** ⚙️ (Requires API key)
- **Purpose**: Work with GitHub repositories, issues, and PRs
- **Setup Required**:
  1. Create a GitHub Personal Access Token:
     - Go to https://github.com/settings/tokens
     - Click "Generate new token (classic)"
     - Select scopes: `repo`, `read:org`, `read:user`
  2. Add token to `.claude/mcp.json`:
     ```json
     "env": {
       "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
     }
     ```

### 4. **Brave Search Server** ⚙️ (Requires API key)
- **Purpose**: Search the web for documentation and solutions
- **Setup Required**:
  1. Get Brave Search API key from https://brave.com/search/api/
  2. Add key to `.claude/mcp.json`:
     ```json
     "env": {
       "BRAVE_API_KEY": "your_api_key_here"
     }
     ```

### 5. **PostgreSQL Server** ⚙️ (Optional - if using PostgreSQL)
- **Purpose**: Query and manage PostgreSQL databases
- **Current Config**: `postgresql://localhost/hackaton_db`
- **Setup Required**:
  - Update the connection string in `.claude/mcp.json` to match your database
  - Format: `postgresql://username:password@host:port/database`
  - Or remove this server if not using PostgreSQL

## How to Apply Configuration

After updating `.claude/mcp.json`:

1. **Restart Claude Code**:
   - Close the current Claude Code session
   - Reopen Claude Code in your project directory

2. **Verify MCP Servers**:
   - Run `/mcp` command to see active servers
   - Check for any error messages

## Current Issues Fixed

✅ **Fixed filesystem path** - Now points to your project root instead of test directory
✅ **Removed unused servers** - Removed Playwright, Puppeteer, Context7 (not needed for this project)
✅ **Added PostgreSQL server** - For database operations (configure connection string as needed)
✅ **Properly structured configuration** - Added env variables where needed

## Next Steps

1. **For immediate use**: Restart Claude Code to load the filesystem and memory servers
2. **For GitHub integration**: Add your GitHub token to the configuration
3. **For web search**: Get a Brave Search API key
4. **For database work**: Update PostgreSQL connection string if using a database

## Troubleshooting

If you see "No MCP servers configured":
1. Make sure `.claude/mcp.json` exists and is valid JSON
2. Restart Claude Code completely
3. Check that Node.js is installed (verified: v22.15.0 ✅)
4. Run `/doctor` command for diagnostics

## Environment Variables (Optional)

You can also set environment variables instead of hardcoding tokens:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
export BRAVE_API_KEY="your_key"
```

Then in `.claude/mcp.json`, reference them with `${VAR_NAME}` syntax.
