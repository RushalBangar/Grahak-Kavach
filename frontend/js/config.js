/**
 * GRAHAK KAVACH — Global Configuration & Demo Presets
 * Smart India Hackathon 2026 (SIH26197)
 */

const CONFIG = {
  API_BASE_URL: 'https://grahak-kavach-26.onrender.com',
  APP_NAME: 'Grahak Kavach',
  APP_VERSION: '1.0.0',
  DEMO_MODE_ACTIVE: false, // Automatically toggled if backend is unreachable

  // Test Product Label Presets for SIH Judges Demo
  PRESETS: [
    {
      id: 'energy_drink_violation',
      title: 'Toxic Energy Drink (Major Violations)',
      category: 'Both Violations',
      tagType: 'violation',
      image: 'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=600&auto=format&fit=crop&q=80',
      extracted_text: `VOLT TURBO ENERGY DRINK
Ingredients: Carbonated Water, Sugar, Citric Acid, Caffeine, Tartrazine (E102), Artificial Flavor, High Fructose Corn Syrup, Sodium Benzoate.
Packed by: Unknown Bev Corp
Net Qty: 250ml
(No MRP Listed | No Mfg Date Found | Contains Harmful Synthetic Dye)`,
      legal_metrology: {
        is_compliant: false,
        details: 'Missing mandatory MRP declaration & Manufacturing Date under Rule 6 of Legal Metrology Rules 2011.',
        checklist: {
          has_mrp: false,
          has_qty: true,
          has_mfg_date: false,
          has_expiry_date: false,
          has_manufacturer: true
        }
      },
      food_safety: {
        health_score: 'E',
        harmful_ingredients: ['Tartrazine (E102)', 'High Fructose Corn Syrup', 'Sodium Benzoate'],
        allergens: ['Caffeine Overdose Warning'],
        details: 'Contains Tartrazine linked to hyperactivity in children & high sugar synthetic formulation without mandatory statutory warnings.'
      }
    },
    {
      id: 'organic_cereal_compliant',
      title: 'Organic Oat Flakes (Fully Compliant)',
      category: 'Fully Compliant',
      tagType: 'compliant',
      image: 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=600&auto=format&fit=crop&q=80',
      extracted_text: `NUTRA-NATURAL WHOLE GRAIN OAT FLAKES
Ingredients: 100% Rolled Oats, Chia Seeds, Freeze-Dried Strawberries.
MRP: Rs. 185.00 (Incl. of all taxes)
Net Weight: 500g
Mfg Date: 12/01/2026 | Best Before: 11/01/2027
Mfg by: Pure Earth Foods Ltd, Plot 45, Sector 3, Pune, MH.
FSSAI Lic No: 11522019000456
Consumer Care: support@pureearthfoods.com | 1800-200-9999`,
      legal_metrology: {
        is_compliant: true,
        details: 'All mandatory Legal Metrology 2011 declarations verified (MRP, Net Qty, Mfg Date, Complete Address).',
        checklist: {
          has_mrp: true,
          has_qty: true,
          has_mfg_date: true,
          has_expiry_date: true,
          has_manufacturer: true
        }
      },
      food_safety: {
        health_score: 'A',
        harmful_ingredients: [],
        allergens: ['Contains Oats (Gluten free facility)'],
        details: 'Clean label product with 0 harmful additives, no added refined sugar or artificial preservatives.'
      }
    },
    {
      id: 'mislabeled_snack_lm',
      title: 'Spicy Potato Wafers (Legal Metrology Issue)',
      category: 'Legal Metrology',
      tagType: 'warning',
      image: 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=600&auto=format&fit=crop&q=80',
      extracted_text: `CRUNCHY TANGY POTATO CHIPS
Ingredients: Fresh Potatoes, Refined Sunflower Oil, Iodized Salt, Chili Powder, Cumin, Turmeric, Citric Acid.
MRP: Rs. 30.00
Mfg: 02/2026 | Exp: 08/2026
Mfg by: Desi Snacks Ltd, Delhi
(Missing Net Quantity & Consumer Care Number)`,
      legal_metrology: {
        is_compliant: false,
        details: 'Violation of Rule 6(1)(b): Missing Net Quantity / Net Weight declaration on principal display panel.',
        checklist: {
          has_mrp: true,
          has_qty: false,
          has_mfg_date: true,
          has_expiry_date: true,
          has_manufacturer: true
        }
      },
      food_safety: {
        health_score: 'B',
        harmful_ingredients: [],
        allergens: ['None'],
        details: 'Safe edible ingredients, moderate salt & saturated fat.'
      }
    },
    {
      id: 'expired_noodle_fs',
      title: 'Instant Masala Noodles (Food Safety Issue)',
      category: 'Food Safety',
      tagType: 'violation',
      image: 'https://images.unsplash.com/photo-1612927601601-6638404737ce?w=600&auto=format&fit=crop&q=80',
      extracted_text: `QUICK NOODLES MASALA BLAST
Ingredients: Refined Wheat Flour (Maida), Palm Oil, Salt, Monosodium Glutamate (MSG - E621), Caramel IV, TBHQ.
MRP: Rs. 20.00 | Net Qty: 70g
Mfg Date: 05/01/2025 | Best Before: 9 Months from Mfg (EXPIRED)
Mfg by: FastFoods India Pvt Ltd, Bengaluru`,
      legal_metrology: {
        is_compliant: true,
        details: 'Legal declarations present on the label package.',
        checklist: {
          has_mrp: true,
          has_qty: true,
          has_mfg_date: true,
          has_expiry_date: true,
          has_manufacturer: true
        }
      },
      food_safety: {
        health_score: 'D',
        harmful_ingredients: ['Monosodium Glutamate (MSG)', 'Palm Oil', 'TBHQ Chemical Preservative'],
        allergens: ['Wheat (Gluten)'],
        details: 'Product is EXPIRED past safe consumption date and contains excessive MSG and TBHQ antioxidant additives.'
      }
    }
  ],

  // Mock initial shops for quick demo selection
  INITIAL_SHOPS: [
    { id: 1, name: 'Metro Supermarket - MG Road', address: '42 MG Road, Indiranagar, Bengaluru' },
    { id: 2, name: 'Shree Krishna Daily Provisions', address: 'Shop 14, Main Market, Andheri West, Mumbai' },
    { id: 3, name: 'Annapurna Grocers & Mart', address: 'Shop 8, Sector 18, Noida, UP' },
    { id: 4, name: 'Reliance Smart Superstore', address: 'Galaxy Mall, SG Highway, Ahmedabad' }
  ]
};

// Export configuration
window.CONFIG = CONFIG;
