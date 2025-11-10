#!/usr/bin/env python3

import subprocess
import sys
import os

def generate_grpc_code():
    """Generate gRPC Python code from .proto file"""
    
    # Check if .proto file exists
    if not os.path.exists('glossary.proto'):
        print("Error: glossary.proto file not found!")
        return False
    
    try:
        # Use grpc_tools.protoc to generate code
        result = subprocess.run([
            sys.executable, '-m', 'grpc_tools.protoc',
            '-I.',
            '--python_out=.',
            '--grpc_python_out=.',
            'glossary.proto'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ gRPC code generated successfully!")
            print("Generated files:")
            if os.path.exists('glossary_pb2.py'):
                print("  - glossary_pb2.py")
            if os.path.exists('glossary_pb2_grpc.py'):
                print("  - glossary_pb2_grpc.py")
            return True
        else:
            print("❌ Error generating gRPC code:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False

if __name__ == '__main__':
    generate_grpc_code()