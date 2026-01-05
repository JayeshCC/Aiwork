# AIWork Web UI Documentation

## Overview

AIWork now includes a modern, lightweight web-based user interface built with **Flask templates + Vanilla JavaScript + Custom CSS**. This UI provides an intuitive way to interact with the AIWork framework without requiring complex frontend frameworks.

## Tech Stack

- **Backend**: Flask (existing server extended with UI routes)
- **Frontend**: HTML5, Vanilla JavaScript, Custom CSS
- **Icons**: Unicode emoji symbols (no external dependencies)
- **Styling**: Custom responsive CSS (no Tailwind/Bootstrap CDN)

### Why This Stack?

✅ **Best Performance**: No JavaScript framework overhead, no build step, instant page loads
✅ **Easy to Learn**: Standard HTML/CSS/JavaScript - no new concepts to learn  
✅ **Easy Development**: No npm, no compilation, direct integration with Flask
✅ **Zero External Dependencies**: Works in air-gapped environments

## Features

### 1. Dashboard (`/ui`)
- **System Overview**: Real-time health status monitoring
- **Statistics Cards**: Total workflows, active workflows, completed workflows, available agents
- **Quick Actions**: Fast access to create workflows, configure agents, test API
- **Recent Workflows**: View recently submitted workflows

### 2. Workflows (`/ui/workflows`)
- **Create Workflows**: Interactive form to build and submit workflows
- **Workflow Management**: List all workflows with filtering (All, Running, Completed, Failed)
- **Task Dependencies**: Define task execution order with dependency management
- **Context Configuration**: Set initial workflow context in JSON format

### 3. Agents (`/ui/agents`)
- **Agent Gallery**: View all available AI agents with their capabilities
- **Agent Details**: Role, goal, backstory, tools, and performance metrics
- **Pre-configured Agents**:
  - Document Processor (OpenVINO OCR, 3.7x speedup)
  - Financial Analyst (Fraud detection, compliance)
  - Compliance Officer (Transaction auditing)
- **Usage Examples**: Code snippets showing how to create agents

### 4. API Explorer (`/ui/api-explorer`)
- **Interactive Testing**: Test all REST API endpoints directly from the browser
- **Request Builder**: Build requests with path parameters and JSON bodies
- **Response Viewer**: View formatted JSON responses
- **Documentation**: Inline endpoint documentation with examples

## Getting Started

### Starting the Server

```bash
# From the repository root
python -m aiwork.api.server

# Or specify a custom port
python -m aiwork.api.server --port 8080

# With auto-port selection
python -m aiwork.api.server --auto-port
```

The server will start on `http://localhost:5000` by default.

### Accessing the UI

Open your browser and navigate to:
- Dashboard: `http://localhost:5000/ui`
- Workflows: `http://localhost:5000/ui/workflows`
- Agents: `http://localhost:5000/ui/agents`  
- API Explorer: `http://localhost:5000/ui/api-explorer`

## Architecture

```
src/aiwork/api/
├── server.py                  # Flask server with API + UI routes
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template with navigation
│   ├── dashboard.html        # Dashboard page
│   ├── workflows.html        # Workflows management
│   ├── agents.html           # Agents explorer
│   └── api_explorer.html     # API testing interface
└── static/
    └── css/
        └── styles.css        # Custom responsive CSS
```

## Creating Workflows via UI

1. Navigate to **Workflows** page
2. Click **Create Workflow** button
3. Fill in workflow details:
   - **Workflow Name**: e.g., `document_processing_pipeline`
   - **Tasks**: Add tasks with dependencies
   - **Context**: Provide initial data in JSON format
4. Click **Create Workflow** to submit
5. View workflow status in the workflows list

## API Integration

The UI communicates with the existing REST API endpoints:

- `GET /health` - System health check
- `POST /workflow` - Submit new workflow
- `GET /workflow/{id}` - Get workflow status
- `GET /workflow/{id}/task/{name}` - Get task status
- `GET /task/{id}` - Get task result (legacy)

## Customization

### Modifying Styles

Edit `/src/aiwork/api/static/css/styles.css` to customize:
- Colors and themes
- Layout and spacing
- Component styles
- Responsive breakpoints

### Adding New Pages

1. Create a new template in `/src/aiwork/api/templates/`
2. Extend `base.html` for consistent navigation
3. Add a route in `/src/aiwork/api/server.py`
4. Update navigation links in `base.html`

Example:
```python
@app.route("/ui/my-page")
def ui_my_page():
    return render_template("my_page.html")
```

## Browser Compatibility

The UI works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

No Internet Explorer support (uses modern JavaScript features).

## Performance

- **Page Load**: < 100ms (no external resources)
- **API Calls**: Asynchronous with fetch API
- **Real-time Updates**: Polling every 5-10 seconds
- **Responsive**: Mobile-friendly layout

## Troubleshooting

### UI Not Loading

1. Ensure Flask server is running: `python -m aiwork.api.server`
2. Check server logs for errors
3. Verify templates exist in `/src/aiwork/api/templates/`
4. Check static files in `/src/aiwork/api/static/`

### Styles Not Applying

1. Clear browser cache
2. Check `styles.css` file exists
3. Verify Flask `static` folder is configured correctly
4. Use browser dev tools to inspect CSS loading

### API Calls Failing

1. Check backend server is running
2. Verify CORS settings (if needed)
3. Open browser console for JavaScript errors
4. Test API endpoints directly with curl

## Future Enhancements

Potential improvements for future versions:

- Real-time workflow execution visualization
- Workflow DAG visual editor (drag-and-drop)
- Agent configuration editor
- Workflow templates library
- Dark mode theme
- Export/import workflows
- Detailed execution logs viewer
- Performance metrics dashboard

## Screenshots

### Dashboard
![Dashboard](https://github.com/user-attachments/assets/2e1d7740-f42f-4d20-8fb0-81001c3f3ed2)

### Workflows
![Workflows](https://github.com/user-attachments/assets/9947638e-465a-4e16-b391-1837ccde03fb)

### Agents
![Agents](https://github.com/user-attachments/assets/fead2d25-9d07-44dd-b2b4-7fe30108892b)

### API Explorer
![API Explorer](https://github.com/user-attachments/assets/70a93f07-b5e9-4d3d-9ed9-884c01b62ecf)

## Contributing

To contribute to the UI:

1. Follow the existing code style
2. Test in multiple browsers
3. Ensure responsive design works on mobile
4. Update documentation for new features
5. Add screenshots for visual changes

## License

Same as the AIWork framework - see main README.md
