# Visual PR Activity Tracker

Visually analyze and track Pull Request activity on any public GitHub repository using an interactive 3D graph!

## Overview
This project dynamically analyzes a GitHub repository by ingesting its Pull Requests, accurately distinguishing between human and bot contributors, and providing an interactive 3D visualization of the repository's contributor network.

Features:
- **Dynamic Repository Ingestion**: Enter any public GitHub repository URL or name (e.g., `microsoft/vscode`) to fetch and analyze its active PRs.
- **3D Network Visualization**: An interactive, galaxy-like 3D graph using React Three Fiber and D3 Force that maps contributors (nodes) and their connections through reviewed or authored PRs.
- **Contributor Differentiation**: Visually distinct styling for human vs. bot contributors, with unique colors assigned to each human contributor.
- **Robust Backend**: A FastAPI backend that intelligently manages GitHub API rate limits and caches repository data locally for fast subsequent loads.

## Tech Stack
- **Frontend**: Next.js, React, TailwindCSS, React Three Fiber, D3 Force 3D
- **Backend**: FastAPI, Python, GitHub REST API 

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- GitHub Personal Access Token (for the backend API requests)

### Running the Backend
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Install the requirements (if using `pip` or `uv`):
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `backend/` directory and add your GitHub token:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   ```
4. Start the FastAPI server:
   ```bash
   python api.py
   ```
   *The backend will be available at `http://localhost:8000`.*

### Running the Frontend
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   # or
   pnpm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```
   *The frontend will be available at `http://localhost:3000`.*

## Usage
1. Open up the frontend in your browser.
2. Enter a GitHub repository (e.g., `facebook/react`) in the input field.
3. Click "Analyze" and watch the PRs map out in a dynamic 3D graph!

## Credits & Acknowledgements
This project wouldn't be possible without the following amazing open-source libraries and tools:
- [Next.js](https://nextjs.org/) & [React](https://react.dev/) - The core frontend framework.
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber) & [Three.js](https://threejs.org/) - Powering the immersive 3D visualization.
- [D3 Force 3D](https://github.com/vasturiano/d3-force-3d) - For the physics-based graph layout calculations.
- [FastAPI](https://fastapi.tiangolo.com/) - The lightning-fast Python backend framework.
- [Tailwind CSS](https://tailwindcss.com/) - For beautiful, utility-first styling.
- [shadcn/ui](https://ui.shadcn.com/) - For beautifully designed, accessible React components.

## Related Repositories

- **Backend / graph‑generation**: [code‑graph‑rag](https://github.com/vitali87/code-graph-rag) – the original PR‑graph ingestor and FastAPI server.
- **Frontend / 3‑D UI**: [graphrag‑workbench](https://github.com/ChristopherLyon/graphrag-workbench) – the Next.js + React‑Three‑Fiber visual‑workbench you adapted.



## License
This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
