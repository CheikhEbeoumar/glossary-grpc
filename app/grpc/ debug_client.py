cat > debug_client.py << 'EOF'
#!/usr/bin/env python3
print("🚀 Starting debug client...")

try:
    print("1. Importing grpc...")
    import grpc
    print("   ✅ grpc imported")
    
    print("2. Importing protobuf modules...")
    import glossary_pb2
    import glossary_pb2_grpc
    print("   ✅ protobuf modules imported")
    
    print("3. Creating channel...")
    channel = grpc.insecure_channel('localhost:50051')
    print("   ✅ channel created")
    
    print("4. Testing connection...")
    try:
        grpc.channel_ready_future(channel).result(timeout=5)
        print("   ✅ Connected to server!")
    except grpc.FutureTimeoutError:
        print("   ❌ Connection timeout - server not running")
        exit(1)
    
    print("5. Creating stub...")
    stub = glossary_pb2_grpc.GlossaryServiceStub(channel)
    print("   ✅ stub created")
    
    print("6. Making RPC call...")
    response = stub.GetGlossaryStats(glossary_pb2.GetStatsRequest())
    print(f"   ✅ Response received: {response.total_terms} terms")
    
    print("🎉 Debug client completed successfully!")
    
except Exception as e:
    print(f"💥 Error: {e}")
    import traceback
    traceback.print_exc()
EOF