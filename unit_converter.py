import re

class UnitConverter:
    """
    Utility class to convert culinary volumetric units to metric weight (grams)
    based on the specific product density.
    """
    
    # Common culinary volumetric units and their approximate volume in milliliters (ml)
    VOLUME_UNITS_ML = {
        'tsp': 5.0,
        'teaspoon': 5.0,
        'tbsp': 15.0,
        'tablespoon': 15.0,
        'cup': 240.0,
        'fl oz': 30.0,
        'fluid ounce': 30.0,
        'pint': 473.0,
        'quart': 946.0,
        'gallon': 3785.0,
        'cm3': 1.0,
        'cl': 10.0,
        'dl': 100.0,
        'l': 1000.0,
        'liter': 1000.0,
        'pinch': 0.36, # rough estimate
        'dash': 0.72,
        'xl': 64.0,
        'l': 50.0,
        'm': 44.0,
        's': 38.0,
        'extra': 64.0,
        'extra large': 64.0,
        'big': 64.0,
        'b': 64.0,
        'large': 50.0,
        'medium': 44.0,
        'small': 38.0,
    }

    # Densities in grams per milliliter (g/ml)
    PRODUCT_DENSITIES = {
        # Baking and flours
        'flour': 0.53,
        'all-purpose flour': 0.53,
        'wheat flour': 0.53,
        'sugar': 0.85,
        'white sugar': 0.85,
        'granulated sugar': 0.85,
        'powdered sugar': 0.50,
        'icing sugar': 0.50,
        'brown sugar': 0.83,
        'salt': 1.20,
        'table salt': 1.20,
        'baking powder': 0.90,
        'baking soda': 1.10,
        'cocoa powder': 0.42,
        
        # Liquids
        'water': 1.0,
        'milk': 1.03,
        'heavy cream': 0.99,
        'vegetable oil': 0.92,
        'olive oil': 0.92,
        'honey': 1.42,
        'maple syrup': 1.32,
        'butter': 0.96, # melted or solid approx
        'melted butter': 0.94,
        
        # Grains and dry goods
        'rice': 0.85,
        'white rice': 0.85,
        'oats': 0.38,
        'rolled oats': 0.38,
        'quinoa': 0.72,
        'couscous': 0.72,
        'lentils': 0.85,
        
        # Condiments
        'ketchup': 1.15,
        'mustard': 1.05,
        'mayonnaise': 0.95,
        'peanut butter': 1.08,
        
        # Default density for unknown items (approximate density of water/mixed food)
        'default': 1.0
    }
    
    # Direct weight conversions (already in weight, just need unit conversion)
    WEIGHT_UNITS_G = {
        'g': 1.0,
        'gram': 1.0,
        'kg': 1000.0,
        'kilo': 1000.0,
        'kilogram': 1000.0,
        'oz': 28.35,
        'ounce': 28.35,
        'lb': 453.59,
        'pound': 453.59,
        'mg': 0.001
    }

    @classmethod
    def get_density(cls, product_name):
        if not product_name:
            return cls.PRODUCT_DENSITIES['default']
            
        product_name = str(product_name).lower().strip()
        
        # Exact match
        if product_name in cls.PRODUCT_DENSITIES:
            return cls.PRODUCT_DENSITIES[product_name]
            
        # Partial match
        for key, density in cls.PRODUCT_DENSITIES.items():
            if key in product_name:
                return density
                
        return cls.PRODUCT_DENSITIES['default']

    @classmethod
    def convert_to_grams(cls, amount, unit, product_name=None):
        """
        Converts an amount and unit of a specific product to grams.
        """
        unit = str(unit).lower().strip()
        
        # If it's already a weight unit, simple scalar conversion
        for w_unit, g_factor in cls.WEIGHT_UNITS_G.items():
            if unit == w_unit or unit == f"{w_unit}s":
                return amount * g_factor
                
        # If it's a volumetric unit, use density
        volume_ml = None
        for v_unit, ml_factor in cls.VOLUME_UNITS_ML.items():
            if unit == v_unit or unit == f"{v_unit}s":
                volume_ml = amount * ml_factor
                break
                
        if volume_ml is not None:
            density = cls.get_density(product_name)
            return volume_ml * density
            
        # Unrecognized unit
        return None

    @classmethod
    def parse_and_convert(cls, recipe_string, product_name=None):
        """
        Parses a string like "1.5 cups" or "2 tbsp" and converts to grams.
        """
        # Match number (including decimals/fractions roughly) followed by text
        match = re.match(r'^([\d\.]+)\s*([a-zA-Z\s]+)$', str(recipe_string).strip())
        if match:
            try:
                amount = float(match.group(1))
                unit = match.group(2).strip()
                result = cls.convert_to_grams(amount, unit, product_name)
                if result is not None:
                    return round(result, 2)
            except ValueError:
                pass
        return None

if __name__ == '__main__':
    # Tests
    print("1 cup of all-purpose flour:", UnitConverter.parse_and_convert("1 cup", "all-purpose flour"), "g")
    print("1 cup of white sugar:", UnitConverter.parse_and_convert("1 cup", "white sugar"), "g")
    print("1 cup of water:", UnitConverter.parse_and_convert("1 cup", "water"), "g")
    print("2 tbsp of olive oil:", UnitConverter.parse_and_convert("2 tbsp", "olive oil"), "g")
    print("1 pound of generic food:", UnitConverter.parse_and_convert("1 pound", "unknown"), "g")
    print("1 pinch of salt:", UnitConverter.parse_and_convert("1 pinch", "salt"), "g")
    print("1 xl egg:", UnitConverter.parse_and_convert("1 xl", "egg"), "g")
    print("2 large eggs:", UnitConverter.parse_and_convert("2 large", "egg"), "g")
