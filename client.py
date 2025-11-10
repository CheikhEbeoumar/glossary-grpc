#!/usr/bin/env python3

import grpc
import glossary_pb2
import glossary_pb2_grpc

class GlossaryClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = glossary_pb2_grpc.GlossaryServiceStub(self.channel)
    
    def get_all_terms(self, limit=100, offset=0):
        request = glossary_pb2.GetAllTermsRequest(limit=limit, offset=offset)
        return self.stub.GetAllTerms(request)
    
    def get_stats(self):
        request = glossary_pb2.GetStatsRequest()
        return self.stub.GetGlossaryStats(request)
    
    def get_terms_by_type(self, rendering_type):
        request = glossary_pb2.GetByRenderingTypeRequest(rendering_type=rendering_type)
        return self.stub.GetTermsByRenderingType(request)

def main():
    client = GlossaryClient()
    
    print("=== gRPC Glossary Client ===")
    
    try:
        # Test getting stats
        print("\n1. Getting glossary stats:")
        stats = client.get_stats()
        print(f"Total terms: {stats.total_terms}")
        print(f"Rendering types: {dict(stats.rendering_type_distribution)}")
        
        # Test getting all terms
        print("\n2. Getting all terms:")
        response = client.get_all_terms(limit=5)
        for term in response.terms:
            print(f"- {term.name} ({term.rendering_type})")
        
        # Test getting terms by type
        print("\n3. Getting SSR terms:")
        ssr_terms = client.get_terms_by_type("SSR")
        for term in ssr_terms.terms:
            print(f"- {term.name}")
            
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code().name}: {e.details()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()