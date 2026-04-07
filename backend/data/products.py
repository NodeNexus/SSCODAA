"""
Sample product dataset with prices across 5 platforms.
"""

PRODUCTS = [
    {
        "id": 1,
        "name": "Samsung Galaxy S23 Ultra",
        "category": "Smartphones",
        "image": "https://placehold.co/300x300/1a1a2e/a5b4fc?text=S23+Ultra",
        "description": "Flagship smartphone with 200MP camera and S-Pen support.",
        "rating": 4.7,
        "reviewCount": 23450,
        "specs": ["6.8\" QHD+ Display", "200MP Camera", "5000mAh Battery", "12GB RAM"],
        "platforms": {
            "amazon":   {"price": 124999, "deliveryDays": 2, "deliveryCost": 0,   "available": True},
            "flipkart": {"price": 119999, "deliveryDays": 3, "deliveryCost": 0,   "available": True},
            "meesho":   {"price": 115999, "deliveryDays": 5, "deliveryCost": 49,  "available": True},
            "snapdeal": {"price": 121999, "deliveryDays": 4, "deliveryCost": 99,  "available": False},
            "myntra":   {"price": 117999, "deliveryDays": 3, "deliveryCost": 0,   "available": False}
        },
        "priceHistory": [125999, 122999, 119999, 121999, 118999, 115999, 117999, 119999]
    },
    {
        "id": 2,
        "name": "Apple MacBook Air M2",
        "category": "Laptops",
        "image": "https://placehold.co/300x300/0f3460/a5b4fc?text=MacBook+Air+M2",
        "description": "Ultra-thin laptop with Apple M2 chip and 18-hour battery life.",
        "rating": 4.9,
        "reviewCount": 18920,
        "specs": ["13.6\" Liquid Retina", "Apple M2 Chip", "18hr Battery", "8GB RAM"],
        "platforms": {
            "amazon":   {"price": 114900, "deliveryDays": 1, "deliveryCost": 0,   "available": True},
            "flipkart": {"price": 112990, "deliveryDays": 2, "deliveryCost": 0,   "available": True},
            "meesho":   {"price": 109999, "deliveryDays": 6, "deliveryCost": 149, "available": True},
            "snapdeal": {"price": 113500, "deliveryDays": 4, "deliveryCost": 0,   "available": True},
            "myntra":   {"price": 118000, "deliveryDays": 3, "deliveryCost": 0,   "available": False}
        },
        "priceHistory": [119900, 116900, 114900, 113900, 112990, 111990, 112990, 114900]
    },
    {
        "id": 3,
        "name": "Sony WH-1000XM5 Headphones",
        "category": "Audio",
        "image": "https://placehold.co/300x300/16213e/a5b4fc?text=WH-1000XM5",
        "description": "Industry-leading noise cancellation with 30hr battery life.",
        "rating": 4.8,
        "reviewCount": 34200,
        "specs": ["Active Noise Cancellation", "30hr Battery", "Bluetooth 5.2", "Hi-Res Audio"],
        "platforms": {
            "amazon":   {"price": 29990, "deliveryDays": 2, "deliveryCost": 0,  "available": True},
            "flipkart": {"price": 28490, "deliveryDays": 3, "deliveryCost": 0,  "available": True},
            "meesho":   {"price": 26999, "deliveryDays": 5, "deliveryCost": 49, "available": True},
            "snapdeal": {"price": 27990, "deliveryDays": 4, "deliveryCost": 0,  "available": True},
            "myntra":   {"price": 30999, "deliveryDays": 2, "deliveryCost": 0,  "available": True}
        },
        "priceHistory": [32000, 30990, 29990, 28490, 27990, 26999, 28000, 29990]
    },
    {
        "id": 4,
        "name": "Nike Air Max 270",
        "category": "Footwear",
        "image": "https://placehold.co/300x300/533483/a5b4fc?text=Nike+Air+Max",
        "description": "Iconic air cushioning with large Max Air unit for all-day comfort.",
        "rating": 4.5,
        "reviewCount": 87650,
        "specs": ["Air Max Cushioning", "Mesh Upper", "Foam Midsole", "12 Colors"],
        "platforms": {
            "amazon":   {"price": 12995, "deliveryDays": 2, "deliveryCost": 0,  "available": True},
            "flipkart": {"price": 11999, "deliveryDays": 3, "deliveryCost": 0,  "available": True},
            "meesho":   {"price": 10499, "deliveryDays": 4, "deliveryCost": 49, "available": True},
            "snapdeal": {"price": 11499, "deliveryDays": 5, "deliveryCost": 99, "available": True},
            "myntra":   {"price": 12995, "deliveryDays": 1, "deliveryCost": 0,  "available": True}
        },
        "priceHistory": [13995, 12995, 11999, 12499, 11499, 10999, 11999, 12995]
    },
    {
        "id": 5,
        "name": "LG 55\" OLED C3 TV",
        "category": "TVs",
        "image": "https://placehold.co/300x300/1a1a2e/a5b4fc?text=LG+OLED+C3",
        "description": "55-inch OLED evo display with α9 Gen6 AI Processor.",
        "rating": 4.8,
        "reviewCount": 12340,
        "specs": ["55\" OLED evo", "4K 120Hz", "Dolby Vision IQ", "HDMI 2.1"],
        "platforms": {
            "amazon":   {"price": 139999, "deliveryDays": 3, "deliveryCost": 0,   "available": True},
            "flipkart": {"price": 134999, "deliveryDays": 4, "deliveryCost": 0,   "available": True},
            "meesho":   {"price": 129999, "deliveryDays": 7, "deliveryCost": 299, "available": True},
            "snapdeal": {"price": 136999, "deliveryDays": 5, "deliveryCost": 199, "available": True},
            "myntra":   {"price": 140000, "deliveryDays": 3, "deliveryCost": 0,   "available": False}
        },
        "priceHistory": [149999, 144999, 139999, 137999, 134999, 132999, 134999, 139999]
    },
    {
        "id": 6,
        "name": "Lenovo IdeaPad Gaming 3",
        "category": "Laptops",
        "image": "https://placehold.co/300x300/0f3460/a5b4fc?text=Lenovo+Gaming",
        "description": "Gaming laptop with RTX 3050, 144Hz display and Ryzen 5.",
        "rating": 4.3,
        "reviewCount": 28900,
        "specs": ["15.6\" 144Hz IPS", "AMD Ryzen 5 6600H", "RTX 3050 4GB", "16GB RAM"],
        "platforms": {
            "amazon":   {"price": 69990, "deliveryDays": 2, "deliveryCost": 0,   "available": True},
            "flipkart": {"price": 67990, "deliveryDays": 3, "deliveryCost": 0,   "available": True},
            "meesho":   {"price": 64999, "deliveryDays": 6, "deliveryCost": 199, "available": True},
            "snapdeal": {"price": 68990, "deliveryDays": 4, "deliveryCost": 0,   "available": True},
            "myntra":   {"price": 71000, "deliveryDays": 3, "deliveryCost": 0,   "available": False}
        },
        "priceHistory": [74990, 72990, 69990, 67990, 65990, 64999, 66990, 69990]
    },
    {
        "id": 7,
        "name": "boAt Airdopes 141",
        "category": "Audio",
        "image": "https://placehold.co/300x300/16213e/a5b4fc?text=boAt+Airdopes",
        "description": "True wireless earbuds with 42 hours total playback.",
        "rating": 4.1,
        "reviewCount": 156780,
        "specs": ["42hr Total Playback", "Bluetooth 5.1", "8mm Drivers", "IPX4"],
        "platforms": {
            "amazon":   {"price": 1299, "deliveryDays": 2, "deliveryCost": 0,  "available": True},
            "flipkart": {"price": 999,  "deliveryDays": 3, "deliveryCost": 0,  "available": True},
            "meesho":   {"price": 849,  "deliveryDays": 5, "deliveryCost": 49, "available": True},
            "snapdeal": {"price": 1099, "deliveryDays": 4, "deliveryCost": 0,  "available": True},
            "myntra":   {"price": 1199, "deliveryDays": 2, "deliveryCost": 0,  "available": True}
        },
        "priceHistory": [1499, 1299, 1099, 999, 899, 849, 999, 1299]
    },
    {
        "id": 8,
        "name": "Canon EOS R50 Camera",
        "category": "Cameras",
        "image": "https://placehold.co/300x300/533483/a5b4fc?text=Canon+EOS+R50",
        "description": "Mirrorless camera with 24.2MP sensor and 4K video.",
        "rating": 4.6,
        "reviewCount": 8920,
        "specs": ["24.2MP APS-C", "4K 30fps Video", "Dual Pixel AF II", "DIGIC X"],
        "platforms": {
            "amazon":   {"price": 79990, "deliveryDays": 2, "deliveryCost": 0,   "available": True},
            "flipkart": {"price": 76990, "deliveryDays": 3, "deliveryCost": 0,   "available": True},
            "meesho":   {"price": 73999, "deliveryDays": 6, "deliveryCost": 149, "available": False},
            "snapdeal": {"price": 78500, "deliveryDays": 4, "deliveryCost": 0,   "available": True},
            "myntra":   {"price": 81000, "deliveryDays": 3, "deliveryCost": 0,   "available": False}
        },
        "priceHistory": [84990, 82990, 79990, 78000, 76990, 75990, 76990, 79990]
    },
    {
        "id": 9,
        "name": "Apple iPhone 15 Pro",
        "category": "Smartphones",
        "image": "https://placehold.co/300x300/1a1a2e/a5b4fc?text=iPhone+15+Pro",
        "description": "Titanium design with A17 Pro chip and 48MP camera system.",
        "rating": 4.8,
        "reviewCount": 41230,
        "specs": ["6.1\" Super Retina XDR", "A17 Pro Chip", "48MP Camera", "Action Button"],
        "platforms": {
            "amazon":   {"price": 134900, "deliveryDays": 1, "deliveryCost": 0,  "available": True},
            "flipkart": {"price": 129999, "deliveryDays": 2, "deliveryCost": 0,  "available": True},
            "meesho":   {"price": 127999, "deliveryDays": 5, "deliveryCost": 99, "available": True},
            "snapdeal": {"price": 131999, "deliveryDays": 4, "deliveryCost": 0,  "available": True},
            "myntra":   {"price": 135000, "deliveryDays": 2, "deliveryCost": 0,  "available": False}
        },
        "priceHistory": [139900, 136900, 134900, 131000, 129999, 127999, 130000, 134900]
    },
    {
        "id": 10,
        "name": "Fossil Gen 6 Smartwatch",
        "category": "Wearables",
        "image": "https://placehold.co/300x300/0f3460/a5b4fc?text=Fossil+Gen+6",
        "description": "Premium smartwatch with Wear OS and rapid charging.",
        "rating": 4.2,
        "reviewCount": 19870,
        "specs": ["1.28\" AMOLED", "Snapdragon 4100+", "Rapid Charging", "GPS+SpO2"],
        "platforms": {
            "amazon":   {"price": 22995, "deliveryDays": 2, "deliveryCost": 0,  "available": True},
            "flipkart": {"price": 20990, "deliveryDays": 3, "deliveryCost": 0,  "available": True},
            "meesho":   {"price": 18999, "deliveryDays": 5, "deliveryCost": 49, "available": True},
            "snapdeal": {"price": 21500, "deliveryDays": 4, "deliveryCost": 0,  "available": True},
            "myntra":   {"price": 23999, "deliveryDays": 2, "deliveryCost": 0,  "available": True}
        },
        "priceHistory": [25995, 23995, 21990, 20990, 19990, 18999, 20500, 22995]
    },
    {
        "id": 11,
        "name": "OnePlus Nord CE 3 Lite",
        "category": "Smartphones",
        "image": "https://placehold.co/300x300/533483/a5b4fc?text=OnePlus+Nord",
        "description": "Budget flagship with 108MP camera and 67W SuperVOOC charging.",
        "rating": 4.3,
        "reviewCount": 67890,
        "specs": ["6.72\" 120Hz LCD", "Snapdragon 695", "108MP Camera", "67W Fast Charge"],
        "platforms": {
            "amazon":   {"price": 19999, "deliveryDays": 2, "deliveryCost": 0,  "available": True},
            "flipkart": {"price": 18999, "deliveryDays": 3, "deliveryCost": 0,  "available": True},
            "meesho":   {"price": 17499, "deliveryDays": 5, "deliveryCost": 49, "available": True},
            "snapdeal": {"price": 19499, "deliveryDays": 4, "deliveryCost": 0,  "available": True},
            "myntra":   {"price": 20999, "deliveryDays": 2, "deliveryCost": 0,  "available": False}
        },
        "priceHistory": [21999, 20999, 19999, 18999, 17999, 17499, 18999, 19999]
    },
    {
        "id": 12,
        "name": "Whirlpool 1.5 Ton 5-Star AC",
        "category": "Appliances",
        "image": "https://placehold.co/300x300/0f3460/a5b4fc?text=Whirlpool+AC",
        "description": "Inverter split AC with Intellisense technology and Wi-Fi.",
        "rating": 4.4,
        "reviewCount": 32100,
        "specs": ["1.5 Ton Capacity", "5 Star Rating", "Smart Diagnosis", "Wi-Fi Enabled"],
        "platforms": {
            "amazon":   {"price": 44990, "deliveryDays": 3, "deliveryCost": 0,   "available": True},
            "flipkart": {"price": 42990, "deliveryDays": 4, "deliveryCost": 0,   "available": True},
            "meesho":   {"price": 40999, "deliveryDays": 6, "deliveryCost": 299, "available": False},
            "snapdeal": {"price": 43999, "deliveryDays": 5, "deliveryCost": 0,   "available": True},
            "myntra":   {"price": 45000, "deliveryDays": 3, "deliveryCost": 0,   "available": False}
        },
        "priceHistory": [47990, 45990, 44990, 43990, 42990, 41990, 42990, 44990]
    }
]

PLATFORM_META = {
    "amazon":   {"city": "Mumbai",    "deliveryDays": 2, "baseCost": 0},
    "flipkart": {"city": "Bangalore", "deliveryDays": 3, "baseCost": 0},
    "meesho":   {"city": "Gurugram",  "deliveryDays": 5, "baseCost": 49},
    "snapdeal": {"city": "New Delhi", "deliveryDays": 4, "baseCost": 99},
    "myntra":   {"city": "Bangalore", "deliveryDays": 3, "baseCost": 0}
}
