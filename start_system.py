#!/usr/bin/env python3
"""
System Launcher for Multi-Perspective LLM Ensemble
Starts both backend WebSocket server and frontend development server simultaneously
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class SystemLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
        # Paths
        self.venv_python = self.project_root / ".venv" / "bin" / "python"
        self.backend_script = self.project_root / "backend_websocket_server.py"
        self.frontend_dir = self.project_root / "fontend"
        
        # Check if paths exist
        self._validate_paths()
    
    def _validate_paths(self):
        """Validate that all required paths exist"""
        if not self.venv_python.exists():
            print("❌ Virtual environment not found. Please create it first:")
            print("   python -m venv .venv")
            print("   source .venv/bin/activate")
            print("   pip install -r requirements.txt")
            sys.exit(1)
        
        if not self.backend_script.exists():
            print("❌ Backend script not found at:", self.backend_script)
            sys.exit(1)
        
        if not self.frontend_dir.exists():
            print("❌ Frontend directory not found at:", self.frontend_dir)
            sys.exit(1)
        
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            print("❌ Frontend package.json not found. Please run 'npm install' in the frontend directory.")
            sys.exit(1)
    
    def start_backend(self):
        """Start the backend WebSocket server"""
        print("🚀 Starting Backend WebSocket Server...")
        try:
            self.backend_process = subprocess.Popen(
                [str(self.venv_python), str(self.backend_script)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor backend output in a separate thread
            backend_thread = threading.Thread(
                target=self._monitor_process,
                args=(self.backend_process, "BACKEND", "🔧"),
                daemon=True
            )
            backend_thread.start()
            
            # Wait a bit for backend to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend server started successfully")
                return True
            else:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend development server"""
        print("🎨 Starting Frontend Development Server...")
        try:
            # Check if node_modules exists
            node_modules = self.frontend_dir / "node_modules"
            if not node_modules.exists():
                print("📦 Installing frontend dependencies...")
                npm_install = subprocess.run(
                    ["npm", "install"],
                    cwd=str(self.frontend_dir),
                    capture_output=True,
                    text=True
                )
                if npm_install.returncode != 0:
                    print("❌ Failed to install frontend dependencies")
                    print(npm_install.stderr)
                    return False
                print("✅ Frontend dependencies installed")
            
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=str(self.frontend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor frontend output in a separate thread
            frontend_thread = threading.Thread(
                target=self._monitor_process,
                args=(self.frontend_process, "FRONTEND", "🌐"),
                daemon=True
            )
            frontend_thread.start()
            
            # Wait a bit for frontend to start
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                print("✅ Frontend server started successfully")
                return True
            else:
                print("❌ Frontend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
    
    def _monitor_process(self, process, name, icon):
        """Monitor process output and print with prefix"""
        try:
            for line in process.stdout:
                if self.running and line.strip():
                    print(f"{icon} {name}: {line.strip()}")
        except Exception as e:
            if self.running:
                print(f"❌ Error monitoring {name}: {e}")
    
    def stop_services(self):
        """Stop both backend and frontend services"""
        print("\n🛑 Stopping services...")
        self.running = False
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("🔨 Backend server force-killed")
            except Exception as e:
                print(f"❌ Error stopping backend: {e}")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("🔨 Frontend server force-killed")
            except Exception as e:
                print(f"❌ Error stopping frontend: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n🔄 Received signal {signum}, shutting down...")
        self.stop_services()
        sys.exit(0)
    
    def run(self):
        """Start both services and keep them running"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("=" * 80)
        print("🚀 Multi-Perspective LLM Ensemble System Launcher")
        print("=" * 80)
        print("📁 Project root:", self.project_root)
        print("🐍 Python virtual env:", self.venv_python)
        print("🔧 Backend script:", self.backend_script)
        print("🌐 Frontend directory:", self.frontend_dir)
        print("=" * 80)
        
        try:
            # Start backend first
            if not self.start_backend():
                print("❌ Failed to start backend. Exiting.")
                sys.exit(1)
            
            # Start frontend
            if not self.start_frontend():
                print("❌ Failed to start frontend. Stopping backend and exiting.")
                self.stop_services()
                sys.exit(1)
            
            print("\n" + "=" * 80)
            print("🎉 SYSTEM SUCCESSFULLY STARTED!")
            print("=" * 80)
            print("🔧 Backend WebSocket Server: ws://localhost:8001")
            print("🌐 Frontend Application: http://localhost:5173")
            print("📊 Multi-Perspective Analysis: Economic, Environmental, Technological")
            print("🧠 Chain of Thought: Universal + Perspective-specific")
            print("=" * 80)
            print("📝 Features Available:")
            print("   • Real-time agent output visualization")
            print("   • Multi-step perspective analysis")
            print("   • Baseline vs ensemble comparison")
            print("   • Live progress tracking")
            print("   • Performance metrics")
            print("=" * 80)
            print("⚡ Press Ctrl+C to stop both services")
            print("🌐 Open your browser to http://localhost:5173 to use the application")
            print("=" * 80)
            
            # Keep the main thread alive
            try:
                while self.running:
                    # Check if processes are still running
                    if self.backend_process and self.backend_process.poll() is not None:
                        print("❌ Backend process has stopped unexpectedly")
                        break
                    
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        print("❌ Frontend process has stopped unexpectedly")
                        break
                    
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            self.stop_services()

def main():
    """Main entry point"""
    launcher = SystemLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
