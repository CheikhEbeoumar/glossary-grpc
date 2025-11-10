from app.database.connection import SessionLocal, init_db
from app.models.term import Term

def initialize_data():
    init_db()
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Term).count() > 0:
            print("Database already has data, skipping initialization")
            return
        
        # Initial terms for your thesis research
        initial_terms = [
            {
                "name": "Server-Side Rendering (SSR)",
                "description": "Technique where the HTML is generated on the server for each request",
                "rendering_type": "SSR",
                "frameworks": ["Next.js", "Nuxt.js", "Angular Universal", "Laravel"],
                "use_cases": ["Dynamic content", "SEO-critical applications", "Personalized pages"],
                "advantages": ["Better SEO", "Fast initial load", "Social media sharing"],
                "disadvantages": ["Server load", "TTFB can be slower", "More complex caching"]
            },
            {
                "name": "Static Site Generation (SSG)",
                "description": "Pre-renders pages at build time, serving static HTML files",
                "rendering_type": "SSG",
                "frameworks": ["Next.js", "Gatsby", "VuePress", "Jekyll"],
                "use_cases": ["Blogs", "Documentation", "Marketing sites", "Portfolios"],
                "advantages": ["Excellent performance", "Great SEO", "Easy CDN caching", "High security"],
                "disadvantages": ["Build time grows with content", "Not suitable for highly dynamic content"]
            },
            {
                "name": "Client-Side Rendering (CSR)",
                "description": "Renders content in the browser using JavaScript",
                "rendering_type": "CSR",
                "frameworks": ["React", "Vue.js", "Angular", "Svelte"],
                "use_cases": ["Web applications", "Dashboards", "Admin panels", "Highly interactive apps"],
                "advantages": ["Rich interactivity", "Fast navigation after load", "Better developer experience"],
                "disadvantages": ["Poor SEO", "Slow initial load", "Blank page issue"]
            }
        ]
        
        for term_data in initial_terms:
            term = Term(**term_data)
            db.add(term)
        
        db.commit()
        print("Initial terms added to database")
        
    except Exception as e:
        print(f"Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_data()