"""
Entry point for running API server as module.

Usage:
    python -m aiwork.api.server
    python -m aiwork.api.server --port 8080
    python -m aiwork.api.server --debug
    python -m aiwork.api.server --auto-port
"""

from .server import start_server

if __name__ == "__main__":
    import sys
    
    host = "0.0.0.0"
    port = 5000
    debug = False
    auto_port = False
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            try:
                port = int(args[i + 1])
                i += 2
            except ValueError:
                print(f"❌ Invalid port: {args[i + 1]}")
                sys.exit(1)
        elif args[i] == "--debug":
            debug = True
            i += 1
        elif args[i] == "--auto-port":
            auto_port = True
            i += 1
        elif args[i] in ["-h", "--help"]:
            print("AIWork API Server")
            print("\nUsage:")
            print("  python -m aiwork.api.server [options]")
            print("\nOptions:")
            print("  --port PORT     Port to bind to (default: 5000)")
            print("  --debug         Enable debug mode")
            print("  --auto-port     Automatically find available port if specified port is taken")
            print("  -h, --help      Show this help message")
            sys.exit(0)
        else:
            print(f"❌ Unknown argument: {args[i]}")
            print("Run with --help for usage information")
            sys.exit(1)
    
    start_server(host=host, port=port, debug=debug, auto_port=auto_port)
