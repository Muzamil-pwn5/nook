from decimal import Decimal

from app.database.models import Product


def storefront_products() -> list[Product]:
    """Return the seeded commerce catalog used by the hosted concierge."""
    return [
        Product(
            name="Dell Inspiron 15",
            description="15-inch productivity laptop with a bright display and all-day battery.",
            price=Decimal("699.99"),
            stock_quantity=12,
            category="Laptops",
        ),
        Product(
            name="HP Pavilion 14",
            description="Slim everyday laptop for customer teams, study, and hybrid work.",
            price=Decimal("649.99"),
            stock_quantity=8,
            category="Laptops",
        ),
        Product(
            name="Logitech MX Master 3S",
            description="Quiet ergonomic mouse with precise tracking and multi-device support.",
            price=Decimal("89.99"),
            stock_quantity=25,
            category="Tech Accessories",
        ),
        Product(
            name="Keychron K2",
            description="Compact mechanical keyboard with wireless connectivity.",
            price=Decimal("99.99"),
            stock_quantity=15,
            category="Tech Accessories",
        ),
        Product(
            name="Sony WH-1000XM5",
            description="Adaptive noise-cancelling headphones tuned for long work sessions.",
            price=Decimal("349.99"),
            stock_quantity=6,
            category="Audio",
        ),
        Product(
            name="Frame 01",
            description="Slim acetate sunglasses with a softly architectural frame and considered everyday finish.",
            price=Decimal("78.00"),
            stock_quantity=18,
            category="Accessories",
        ),
        Product(
            name="Silk Knot 02",
            description="A lightweight silk twill scarf in a quiet geometric print for layering through the week.",
            price=Decimal("95.00"),
            stock_quantity=11,
            category="Accessories",
        ),
        Product(
            name="Shade 03",
            description="A compact brushed-metal hair clip with a sculpted profile and easy daily hold.",
            price=Decimal("65.00"),
            stock_quantity=22,
            category="Accessories",
        ),
        Product(
            name="Signet Halo 01",
            description="A minimal sterling silver signet with a softened oval face and hand-finished edge.",
            price=Decimal("120.00"),
            stock_quantity=9,
            category="Jewellery",
        ),
        Product(
            name="Noir 01",
            description="An eau de parfum built around cedar, soft smoke, and a clean skin finish.",
            price=Decimal("96.00"),
            stock_quantity=14,
            category="Perfume",
        ),
        Product(
            name="Loafer 01",
            description="A polished leather loafer with a low sculpted heel and an easy everyday shape.",
            price=Decimal("148.00"),
            stock_quantity=7,
            category="Shoes",
        ),
        Product(
            name="Court 02",
            description="A clean nappa leather court shoe with a softly squared toe and balanced low heel.",
            price=Decimal("165.00"),
            stock_quantity=5,
            category="Shoes",
        ),
        Product(
            name="Cloud 01",
            description="A tonal recycled-knit sneaker with a responsive sole for long days in motion.",
            price=Decimal("145.00"),
            stock_quantity=13,
            category="Sneakers",
        ),
        Product(
            name="Fold Tote 01",
            description="A structured vegetable-tanned leather tote designed to move from workday to weekend.",
            price=Decimal("138.00"),
            stock_quantity=10,
            category="Bags",
        ),
        Product(
            name="Column 01",
            description="A fluid crepe column dress in a deep ink tone with a calm, easy drape.",
            price=Decimal("142.00"),
            stock_quantity=8,
            category="Dresses",
        ),
        Product(
            name="Drift 02",
            description="A linen voile dress with an understated waist and movement made for warmer days.",
            price=Decimal("132.00"),
            stock_quantity=12,
            category="Dresses",
        ),
    ]
