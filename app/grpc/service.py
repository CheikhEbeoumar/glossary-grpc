import grpc
from concurrent import futures
import logging
from sqlalchemy.orm import Session

from app.database.connection import get_db, init_db
from app.models.term import Term
from glossary_pb2 import (
    TermResponse, GetAllTermsResponse, DeleteTermResponse, StatsResponse
)
import glossary_pb2_grpc

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    
    def __init__(self):
        init_db()
    
    def _get_db_session(self) -> Session:
        return next(get_db())
    
    def _term_to_proto(self, term: Term) -> TermResponse:
        return TermResponse(
            id=term.id,
            name=term.name,
            description=term.description,
            rendering_type=term.rendering_type,
            frameworks=term.frameworks,
            use_cases=term.use_cases,
            advantages=term.advantages,
            disadvantages=term.disadvantages
        )
    
    def GetAllTerms(self, request, context):
        db = self._get_db_session()
        limit = request.limit if request.limit > 0 else 100
        offset = request.offset if request.offset >= 0 else 0
        
        terms = db.query(Term).offset(offset).limit(limit).all()
        total_count = db.query(Term).count()
        
        term_responses = [self._term_to_proto(term) for term in terms]
        return GetAllTermsResponse(terms=term_responses, total_count=total_count)
    
    def GetGlossaryStats(self, request, context):
        db = self._get_db_session()
        
        total_terms = db.query(Term).count()
        
        rendering_stats = {}
        rendering_types = db.query(Term.rendering_type).distinct().all()
        for rendering_type, in rendering_types:
            count = db.query(Term).filter(Term.rendering_type == rendering_type).count()
            rendering_stats[rendering_type] = count
        
        all_frameworks = set()
        terms = db.query(Term).all()
        for term in terms:
            all_frameworks.update(term.frameworks)
        
        return StatsResponse(
            total_terms=total_terms,
            rendering_type_distribution=rendering_stats,
            unique_frameworks=list(all_frameworks),
            total_frameworks_covered=len(all_frameworks)
        )
    
    def GetTermsByRenderingType(self, request, context):
        db = self._get_db_session()
        terms = db.query(Term).filter(Term.rendering_type == request.rendering_type).all()
        
        term_responses = [self._term_to_proto(term) for term in terms]
        return GetAllTermsResponse(terms=term_responses, total_count=len(term_responses))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(), server)
    server.add_insecure_port('[::]:50051')
    
    server.start()
    print("gRPC Glossary Server started on port 50051")
    print("Server is running... Press Ctrl+C to stop.")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()