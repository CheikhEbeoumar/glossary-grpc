from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    rendering_type = Column(String(20), nullable=False)  # SSR, SSG, CSR, etc.
    frameworks = Column(JSON, nullable=False)
    use_cases = Column(JSON, nullable=False)
    advantages = Column(JSON, nullable=False)
    disadvantages = Column(JSON, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rendering_type": self.rendering_type,
            "frameworks": self.frameworks,
            "use_cases": self.use_cases,
            "advantages": self.advantages,
            "disadvantages": self.disadvantages
        }