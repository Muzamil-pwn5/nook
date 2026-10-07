const image = (url, id) => `${url}?auto=format&fit=crop&w=900&q=82&sig=${id}`;

const IMAGE_POOLS = {
  Clothing: ["https://images.unsplash.com/photo-1490481651871-ab68de25d43d", "https://images.unsplash.com/photo-1529139574466-a303027c1d8b", "https://images.unsplash.com/photo-1483985988355-763728e1935b"],
  Dresses: ["https://images.unsplash.com/photo-1496747611176-843222e1e57c", "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446", "https://images.unsplash.com/photo-1539008835657-9e8e9680c956"],
  Tops: ["https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc", "https://images.unsplash.com/photo-1564257577054-2e0b6f7e9f8a", "https://images.unsplash.com/photo-1576566588028-4147f3842f27"],
  Bottoms: ["https://images.unsplash.com/photo-1541099649105-f69ad21f3246", "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f", "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3"],
  Outerwear: ["https://images.unsplash.com/photo-1551028719-00167b16eac5", "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f", "https://images.unsplash.com/photo-1529139574466-a303027c1d8b"],
  Shoes: ["https://images.unsplash.com/photo-1549298916-b41d501d3772", "https://images.unsplash.com/photo-1542291026-7eec264c27ff", "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77"],
  Sneakers: ["https://images.unsplash.com/photo-1495555961986-6d4c1ecb7be3", "https://images.unsplash.com/photo-1552346154-21d32810aba3", "https://images.unsplash.com/photo-1460353581641-37baddab0fa2"],
  Bags: ["https://images.unsplash.com/photo-1553062407-98eeb64c6a62", "https://images.unsplash.com/photo-1584917865442-de89df76afd3", "https://images.unsplash.com/photo-1590874103328-eac38a683ce7"],
  Accessories: ["https://images.unsplash.com/photo-1523779917675-b6ed3a42a561", "https://images.unsplash.com/photo-1511499767150-a48a237f0083", "https://images.unsplash.com/photo-1509695507497-903c140c43b0"],
  Jewellery: ["https://images.unsplash.com/photo-1515562141207-7a88fb7ce338", "https://images.unsplash.com/photo-1611652022419-a9419f74343d", "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908"],
  Perfume: ["https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc", "https://images.unsplash.com/photo-1594035910387-fea47794261f", "https://images.unsplash.com/photo-1588405748880-12d1d2a5c9a0"],
  Beauty: ["https://images.unsplash.com/photo-1556228720-195a672e8a03", "https://images.unsplash.com/photo-1596462502278-27bfdc403348", "https://images.unsplash.com/photo-1571781926291-c477ebfd024b"]
};

const CATEGORY_DEFS = [
  ["Clothing", "shirt", ["Atelier", "Serein", "Form", "Lumen", "North", "Quiet", "Edition", "Morrow", "Archive", "Line"], ["Organic cotton", "Washed linen", "Merino wool", "Tencel twill"]],
  ["Dresses", "dress", ["Silhouette", "Column", "Sunday", "Contour", "Muse", "Gather", "Cove", "Drift", "Satin", "Interval"], ["Silk blend", "Fluid crepe", "Brushed jersey", "Linen voile"]],
  ["Tops", "top", ["Softline", "Rib", "Essential", "Frame", "Studio", "Second", "Poise", "Daily", "Arc", "Halo"], ["Supima cotton", "Cashmere knit", "Silk jersey", "Ribbed modal"]],
  ["Bottoms", "trouser", ["Pleat", "Wide", "Taper", "Ease", "Column", "Drawn", "Flow", "Utility", "Tailored", "Relaxed"], ["Wool gabardine", "Cotton poplin", "Recycled nylon", "Linen blend"]],
  ["Outerwear", "jacket", ["Transit", "Shelter", "Cloud", "Field", "Longline", "Weather", "Atelier", "Civic", "Padded", "Studio"], ["Recycled down", "Waxed cotton", "Alpaca wool", "Technical nylon"]],
  ["Shoes", "shoe", ["Loafer", "Muse", "Sculpt", "Court", "Stride", "Ballet", "Sling", "Tread", "Lace", "Form"], ["Italian leather", "Suede", "Nappa leather", "Recycled canvas"]],
  ["Sneakers", "sneaker", ["Cloud", "Run", "Motion", "Tonal", "Daylight", "Vector", "Low", "Court", "Trail", "Studio"], ["Mesh knit", "Leather / rubber", "Recycled knit", "Canvas"]],
  ["Bags", "bag", ["Carry", "Fold", "Frame", "Archive", "Day", "Market", "Sling", "Weekender", "Mini", "Tote"], ["Vegetable-tanned leather", "Waxed canvas", "Recycled nylon", "Soft suede"]],
  ["Accessories", "accessory", ["Frame", "Shade", "Silk", "Knot", "Loop", "Signal", "Wrap", "Studio", "Line", "Pocket"], ["Acetate", "Silk twill", "Brushed metal", "Fine wool"]],
  ["Jewellery", "jewel", ["Signet", "Arc", "Orb", "Thread", "Trace", "Link", "Cuff", "Drop", "Stack", "Halo"], ["Sterling silver", "18k gold vermeil", "Recycled brass", "Freshwater pearl"]],
  ["Perfume", "eau de parfum", ["Noir", "Sillage", "Fleur", "Cedar", "Moss", "Dusk", "Verve", "Skin", "Tide", "Lumen"], ["Eau de parfum", "Extrait", "Botanical mist", "Discovery set"]],
  ["Beauty", "beauty", ["Veil", "Dew", "Sculpt", "Tint", "Bare", "Glow", "Cloud", "Ritual", "Soft", "Petal"], ["Vegan formula", "Mineral pigment", "Botanical blend", "Plant wax"]]
];

const COLORS = ["Black", "Ivory", "Red", "Cobalt", "Sage", "Sand", "Blush", "Chocolate", "Silver", "Gold"];
const CLOTHING = new Set(["Clothing", "Dresses", "Tops", "Bottoms", "Outerwear"]);
const SHOES = new Set(["Shoes", "Sneakers"]);
export const CATEGORY_NAMES = CATEGORY_DEFS.map(([name]) => name);
export const DEMO_PRODUCTS = CATEGORY_DEFS.flatMap(([category, singular, names, materials], categoryIndex) => Array.from({ length: 24 }, (_, index) => {
  const id = categoryIndex * 20 + index + 1;
  const color = COLORS[(index + categoryIndex) % COLORS.length];
  const sizes = CLOTHING.has(category) ? ["XS", "S", "M", "L", "XL"] : SHOES.has(category) ? ["36", "37", "38", "39", "40", "41", "42"] : ["One size"];
  const priceBase = category === "Jewellery" ? 120 : category === "Perfume" ? 96 : category === "Beauty" ? 48 : SHOES.has(category) ? 165 : 88;
  return {
    id, name: `${names[index % names.length]} ${String(index + 1).padStart(2, "0")}`, category, price: priceBase + ((index * 17 + categoryIndex * 13) % 180), stock_quantity: 6 + ((index * 3 + categoryIndex) % 28), material: materials[index % materials.length], edition: `${category} / ${String(index + 1).padStart(2, "0")}`, tagline: `${color} ${singular}, considered.`, description: `A considered ${singular} in ${color.toLowerCase()}, designed for an easy wardrobe and a longer life.`, image: image(IMAGE_POOLS[category][index % IMAGE_POOLS[category].length], id), color, colors: [color, COLORS[(index + 3) % COLORS.length]], sizes
  };
}));

export const DEMO_MESSAGES = [{ id: "message-1", role: "assistant", text: "Tell me what you are looking for, and I’ll reason through the options with you.", time: "09:41" }];
export const DEMO_ORDERS = [];
export const DEMO_ACTIVITY = [];
export const TOOL_META = {};
