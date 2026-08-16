import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_bookstore.settings')
django.setup()

from store.models import Category, Book

def seed():
    print("Starting database seeding...")

    # Create Categories
    categories_data = [
        {"name": "Fiction", "description": "Atmospheric novels, short stories, and legendary tales of imagination."},
        {"name": "Technology & Sci-Fi", "description": "Cutting-edge software design, quantum architectures, and future speculations."},
        {"name": "Education & Learning", "description": "Textbooks, reference manuals, and practical guides to sharpen your skills."},
        {"name": "Biography & Memoirs", "description": "Personal narratives, memoirs, and historic chronicles of great minds."}
    ]

    categories = {}
    for cat in categories_data:
        obj, created = Category.objects.get_or_create(
            name=cat["name"],
            defaults={"description": cat["description"]}
        )
        categories[cat["name"]] = obj
        if created:
            print(f"Created Category: {obj.name}")
        else:
            print(f"Category already exists: {obj.name}")

    # Create Books
    books_data = [
        {
            "title": "The Midnight Odyssey",
            "author": "Arthur Pendelton",
            "category": categories["Fiction"],
            "price": 14.99,
            "description": "An atmospheric, highly poetic journey through a subterranean library where books are treated as living, breathing elements. The protagonist, a young cartographer named Silas, must map out the forgotten archives while dodging shadows that speak in whispers. This rich tale explores the boundaries between memory, reality, and literary imagination.",
            "is_best_seller": True,
            "is_featured": True,
            "is_new_arrival": False,
            "is_audiobook": False
        },
        {
            "title": "Architectures of Infinity",
            "author": "Sarah Connor",
            "category": categories["Technology & Sci-Fi"],
            "price": 24.99,
            "description": "A deep dive into structural scaling, quantum computing paradigms, and the architectural baselines of super-intelligent systems. Written by an active industry practitioner, this book strips away the mathematical jargon and provides clear, digestible visual concepts of future computation. An absolute essential for engineers and technologists looking to build tomorrow's infrastructures.",
            "is_best_seller": False,
            "is_featured": True,
            "is_new_arrival": True,
            "is_audiobook": False
        },
        {
            "title": "Lyrical Echoes",
            "author": "Emily Bronte",
            "category": categories["Fiction"],
            "price": 12.50,
            "description": "A collection of beautiful, melancholic short stories centered around life on the remote northern moors. Each story weaves intricate elements of natural symbolism and intense emotional depth, exploring characters who live at the edge of societal bounds. Bronte's prose is breathtakingly poetic, leaving a lasting resonance on every reader's mind.",
            "is_best_seller": False,
            "is_featured": False,
            "is_new_arrival": True,
            "is_audiobook": False
        },
        {
            "title": "Deep Learning Sandbox",
            "author": "Dr. Julian Vance",
            "category": categories["Technology & Sci-Fi"],
            "price": 39.99,
            "description": "A hands-on engineering playbook detailing neural networks, reinforcement loops, and natural language transformers. With clean code snippets and real-world sandbox examples, this textbook helps professional developers transition from baseline statistics into building operational AI models. Packed with diagrams, step-by-step guides, and optimization tips.",
            "is_best_seller": True,
            "is_featured": False,
            "is_new_arrival": True,
            "is_audiobook": False
        },
        {
            "title": "The Echoing Sea",
            "author": "Captain Gabriel Stone",
            "category": categories["Fiction"],
            "price": 19.99,
            "description": "A riveting adventure story detailing the isolated life of a lightkeeper on a rocky crag in the North Atlantic. After hearing odd signals on a forgotten radio channel, he is drawn into an oceanic mystery that challenges his sanity. This audiobook version contains soundscape elements and marine atmospheres to fully immerse the listener.",
            "is_best_seller": False,
            "is_featured": False,
            "is_new_arrival": False,
            "is_audiobook": True,
            "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        },
        {
            "title": "Building Quantum Minds",
            "author": "Linus Turing",
            "category": categories["Technology & Sci-Fi"],
            "price": 45.00,
            "description": "A theoretical exploration of organic synapses combined with silicon quantum gates. Turing proposes a new model of hybrid computing, charting a clear course toward artificial generalized intelligence. This audiobook edition includes exclusive author commentary segments, providing listeners with a personal tour of the mathematical milestones.",
            "is_best_seller": True,
            "is_featured": False,
            "is_new_arrival": False,
            "is_audiobook": True,
            "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
        },
        {
            "title": "Mastering Django Core",
            "author": "Andrew Django",
            "category": categories["Education & Learning"],
            "price": 29.99,
            "description": "An exhaustive, highly detailed reference guide covering advanced Django routing, custom middle-wares, database optimization, and high-security configurations. Written for intermediate developers wanting to master full-stack deployment, it explains the internals of Django's ORM engine and details clean patterns for professional software delivery.",
            "is_best_seller": False,
            "is_featured": True,
            "is_new_arrival": False,
            "is_audiobook": False
        },
        {
            "title": "Memoirs of a Codebreaker",
            "author": "Ada Lovelace",
            "category": categories["Biography & Memoirs"],
            "price": 18.50,
            "description": "A historic, inspiring personal narrative of the life, obstacles, and breakthroughs of the world's first programmer. Lovelace details her correspondence with Babbage, her inner mathematical insights, and the challenge of navigating Victorian society while laying down the philosophical and technical foundations of the software age.",
            "is_best_seller": True,
            "is_featured": False,
            "is_new_arrival": False,
            "is_audiobook": False
        }
    ]

    for book in books_data:
        obj, created = Book.objects.get_or_create(
            title=book["title"],
            defaults={
                "author": book["author"],
                "category": book["category"],
                "price": book["price"],
                "description": book["description"],
                "is_best_seller": book["is_best_seller"],
                "is_featured": book["is_featured"],
                "is_new_arrival": book["is_new_arrival"],
                "is_audiobook": book["is_audiobook"],
                "audio_url": book.get("audio_url")
            }
        )
        if created:
            print(f"Created Book: {obj.title}")
        else:
            print(f"Book already exists: {obj.title}")

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
