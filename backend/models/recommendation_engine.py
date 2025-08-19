import json
import os

class RecommendationEngine:
    def __init__(self):
        self.medicine_database = self.load_medicine_database()
        self.crop_tips_database = self.load_crop_tips_database()
    
    def load_medicine_database(self):
        """Load medicine database"""
        medicine_db = {
            "bacterial_blight": {
                "medicines": [
                    {
                        "name": "Copper Hydroxide",
                        "dosage": "2-3g per liter of water",
                        "application": "Foliar spray every 7-10 days",
                        "precautions": "Avoid spraying during flowering"
                    },
                    {
                        "name": "Streptomycin Sulfate",
                        "dosage": "1g per liter of water",
                        "application": "Spray in early morning or evening",
                        "precautions": "Do not exceed recommended dosage"
                    }
                ],
                "organic_alternatives": [
                    "Neem oil spray (5ml per liter)",
                    "Turmeric powder paste application",
                    "Garlic extract spray"
                ]
            },
            "brown_spot": {
                "medicines": [
                    {
                        "name": "Mancozeb",
                        "dosage": "2.5g per liter of water",
                        "application": "Spray at 15-day intervals",
                        "precautions": "Use protective equipment"
                    },
                    {
                        "name": "Propiconazole",
                        "dosage": "1ml per liter of water",
                        "application": "Apply at first sign of disease",
                        "precautions": "Avoid drift to water bodies"
                    }
                ],
                "organic_alternatives": [
                    "Baking soda spray (1 tsp per liter)",
                    "Milk spray (100ml per liter water)",
                    "Compost tea application"
                ]
            },
            "leaf_blast": {
                "medicines": [
                    {
                        "name": "Tricyclazole",
                        "dosage": "0.6g per liter of water",
                        "application": "Prophylactic spray at tillering stage",
                        "precautions": "Rotate with other fungicides"
                    },
                    {
                        "name": "Isoprothiolane",
                        "dosage": "1.5ml per liter of water",
                        "application": "Apply before symptom appearance",
                        "precautions": "Maintain spray equipment properly"
                    }
                ],
                "organic_alternatives": [
                    "Silicon-based foliar spray",
                    "Trichoderma viride application",
                    "Pseudomonas fluorescens treatment"
                ]
            },
            "healthy": {
                "medicines": [],
                "organic_alternatives": [
                    "Continue regular organic fertilization",
                    "Maintain proper plant nutrition",
                    "Ensure good air circulation"
                ]
            }
        }
        return medicine_db
    
    def load_crop_tips_database(self):
        """Load crop cultivation tips database"""
        tips_db = {
            "wheat": {
                "planting": [
                    "Plant when soil temperature is 50-60°F",
                    "Use certified disease-free seeds",
                    "Maintain 6-8 inch row spacing"
                ],
                "fertilization": [
                    "Apply NPK 120:60:40 kg/hectare",
                    "Split nitrogen application in 2-3 doses",
                    "Apply phosphorus at sowing time"
                ],
                "irrigation": [
                    "Provide 4-6 irrigations during crop season",
                    "Critical stages: crown root initiation, tillering, flowering",
                    "Avoid waterlogging conditions"
                ],
                "pest_management": [
                    "Monitor for aphids and termites",
                    "Use integrated pest management",
                    "Rotate crops to break pest cycles"
                ]
            },
            "rice": {
                "planting": [
                    "Transplant 25-30 day old seedlings",
                    "Maintain 2-3 seedlings per hill",
                    "Keep 20x15 cm spacing between plants"
                ],
                "fertilization": [
                    "Apply NPK 100:50:50 kg/hectare",
                    "Use urea in split doses",
                    "Apply zinc sulfate if deficient"
                ],
                "irrigation": [
                    "Maintain 2-5 cm standing water",
                    "Drain field before harvesting",
                    "Alternate wetting and drying in later stages"
                ],
                "pest_management": [
                    "Monitor for stem borers and leaf folders",
                    "Use pheromone traps",
                    "Practice crop rotation"
                ]
            }
        }
        return tips_db
    
    def get_medicine_suggestions(self, disease):
        """Get medicine suggestions for a specific disease"""
        if disease in self.medicine_database:
            return self.medicine_database[disease]
        else:
            return {
                "medicines": [],
                "organic_alternatives": ["Consult agricultural extension officer for specific treatment"]
            }
    
    def get_treatment_tips(self, disease):
        """Get general treatment tips for disease management"""
        general_tips = [
            "Remove and destroy infected plant parts",
            "Improve air circulation around plants",
            "Avoid overhead watering",
            "Apply treatments during cooler parts of the day",
            "Monitor plants regularly for early detection"
        ]
        
        disease_specific_tips = {
            "bacterial_blight": [
                "Use disease-free seeds",
                "Avoid working in wet fields",
                "Copper-based fungicides are effective"
            ],
            "brown_spot": [
                "Ensure proper plant nutrition",
                "Avoid water stress",
                "Remove crop residues after harvest"
            ],
            "leaf_blast": [
                "Avoid excessive nitrogen fertilization",
                "Maintain proper plant spacing",
                "Use resistant varieties when available"
            ]
        }
        
        if disease in disease_specific_tips:
            return general_tips + disease_specific_tips[disease]
        else:
            return general_tips
    
    def get_crop_recommendations(self, crop_type, season, location):
        """Get cultivation recommendations for specific crop and conditions"""
        recommendations = {
            "general_tips": [
                "Conduct soil testing before planting",
                "Use quality seeds from certified sources",
                "Follow recommended planting dates",
                "Implement integrated pest management"
            ]
        }
        
        if crop_type in self.crop_tips_database:
            recommendations.update(self.crop_tips_database[crop_type])
        
        # Season-specific recommendations
        season_tips = {
            "spring": [
                "Prepare soil when it's workable",
                "Watch for late frost warnings",
                "Begin pest monitoring early"
            ],
            "summer": [
                "Ensure adequate irrigation",
                "Monitor for heat stress",
                "Increase disease surveillance"
            ],
            "fall": [
                "Time harvest properly",
                "Prepare for storage",
                "Plan cover crops"
            ],
            "winter": [
                "Plan next season's crops",
                "Maintain equipment",
                "Analyze previous season's data"
            ]
        }
        
        if season in season_tips:
            recommendations["seasonal_tips"] = season_tips[season]
        
        return recommendations