const image = (category, id) => `https://loremflickr.com/900/1100/${encodeURIComponent(category.toLowerCase())}?lock=${id}`;

const CATEGORY_DEFS = [
  ["Clothing", "shirt", ["Uniqlo", "COS", "Everlane", "Arket", "Levi's", "Mango", "Zara", "Massimo Dutti", "J.Crew", "Gap"], ["Organic cotton", "Washed linen", "Merino wool", "Tencel twill"]],
  ["Dresses", "dress", ["Reformation", "Faithfull the Brand", "Ganni", "Diane von Furstenberg", "Rixo", "Mango", "Zara", "Aritzia", "Sézane", "& Other Stories"], ["Silk blend", "Fluid crepe", "Brushed jersey", "Linen voile"]],
  ["Tops", "top", ["Aritzia", "Everlane", "Uniqlo", "COS", "Madewell", "Abercrombie", "J.Crew", "Arket", "Zara", "Reiss"], ["Supima cotton", "Cashmere knit", "Silk jersey", "Ribbed modal"]],
  ["Bottoms", "trouser", ["Levi's", "AG Jeans", "Madewell", "Everlane", "Uniqlo", "COS", "Abercrombie", "J.Crew", "Reiss", "Zara"], ["Wool gabardine", "Cotton poplin", "Recycled nylon", "Linen blend"]],
  ["Outerwear", "jacket", ["Patagonia", "The North Face", "Barbour", "Mackage", "Aritzia", "Canada Goose", "Uniqlo", "COS", "Moncler", "Columbia"], ["Recycled down", "Waxed cotton", "Alpaca wool", "Technical nylon"]],
  ["Shoes", "shoe", ["Clarks", "Dr. Martens", "Sam Edelman", "Aldo", "Cole Haan", "Vagabond", "Everlane", "Gucci", "Tod's", "Charles & Keith"], ["Italian leather", "Suede", "Nappa leather", "Recycled canvas"]],
  ["Sneakers", "sneaker", ["Nike", "Adidas", "New Balance", "Veja", "On", "Asics", "Puma", "Converse", "Vans", "Reebok"], ["Mesh knit", "Leather / rubber", "Recycled knit", "Canvas"]],
  ["Bags", "bag", ["Coach", "Longchamp", "Cuyana", "Polène", "Tory Burch", "Michael Kors", "Fossil", "Kate Spade", "Telfar", "Dagne Dover"], ["Vegetable-tanned leather", "Waxed canvas", "Recycled nylon", "Soft suede"]],
  ["Accessories", "accessory", ["Ray-Ban", "Le Specs", "Madewell", "Baggu", "Herschel", "Lululemon", "Uniqlo", "Free People", "Anthropologie", "Urban Outfitters"], ["Acetate", "Silk twill", "Brushed metal", "Fine wool"]],
  ["Jewellery", "jewel", ["Pandora", "Mejuri", "Missoma", "Cartier", "Tiffany & Co.", "Swarovski", "Monica Vinader", "Kendra Scott", "Aurate", "Ana Luisa"], ["Sterling silver", "18k gold vermeil", "Recycled brass", "Freshwater pearl"]],
  ["Perfume", "fragrance", ["Chanel", "Dior", "Jo Malone", "Le Labo", "Byredo", "Tom Ford", "Diptyque", "Maison Margiela", "Gucci", "Yves Saint Laurent"], ["Eau de parfum", "Extrait", "Botanical mist", "Discovery set"]],
  ["Beauty", "beauty", ["The Ordinary", "CeraVe", "Glossier", "Rare Beauty", "Fenty Beauty", "Drunk Elephant", "La Roche-Posay", "Kiehl's", "MAC", "NARS"], ["Vegan formula", "Mineral pigment", "Botanical blend", "Plant wax"]]
];

const COLORS = ["Black", "Ivory", "Red", "Cobalt", "Sage", "Sand", "Blush", "Chocolate", "Silver", "Gold"];
const CLOTHING = new Set(["Clothing", "Dresses", "Tops", "Bottoms", "Outerwear"]);
const SHOES = new Set(["Shoes", "Sneakers"]);
export const CATEGORY_NAMES = CATEGORY_DEFS.map(([name]) => name);
export const DEMO_PRODUCTS = CATEGORY_DEFS.flatMap(([category, singular, brands, materials], categoryIndex) => Array.from({ length: 50 }, (_, index) => {
  const id = categoryIndex * 50 + index + 1;
  const brand = brands[index % brands.length];
  const color = COLORS[(index + categoryIndex) % COLORS.length];
  const sizes = CLOTHING.has(category) ? ["XS", "S", "M", "L", "XL"] : SHOES.has(category) ? ["36", "37", "38", "39", "40", "41", "42"] : ["One size"];
  const priceBase = category === "Jewellery" ? 120 : category === "Perfume" ? 96 : category === "Beauty" ? 48 : SHOES.has(category) ? 165 : 88;
  return {
    id, name: `${brand} ${singular[0].toUpperCase() + singular.slice(1)} ${String(index + 1).padStart(2, "0")}`, brand, category, price: priceBase + ((index * 17 + categoryIndex * 13) % 180), stock_quantity: 6 + ((index * 3 + categoryIndex) % 28), material: materials[index % materials.length], edition: `${brand} / ${category}`, tagline: `${color} ${singular} from ${brand}.`, description: `${brand}'s ${singular} in ${color.toLowerCase()}, made in ${materials[index % materials.length].toLowerCase()} for everyday wear.`, image: image(category, id), color, colors: [color, COLORS[(index + 3) % COLORS.length]], sizes
  };
}));

export const DEMO_MESSAGES = [{ id: "message-1", role: "assistant", text: "Tell me what you are looking for, and I’ll reason through the options with you.", time: "09:41" }];
export const DEMO_ORDERS = [];
export const DEMO_ACTIVITY = [];
export const TOOL_META = {};
