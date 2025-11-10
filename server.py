from app.grpc.service import serve
from initial_data import initialize_data

if __name__ == '__main__':
    # Initialize database with sample data
    initialize_data()
    # Start gRPC server
    serve()