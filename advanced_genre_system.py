#!/usr/bin/env python3
"""
🎵 ADVANCED GENRE SYSTEM
Tobulas žanrų sistemą su realiais statistikos duomenimis ir AI sprendimų priėmimu
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class VocalType(Enum):
    """Vokalų tipai"""
    INSTRUMENTAL = "instrumental"
    FULL_LYRICS = "full_lyrics"
    ATMOSPHERIC_VOCALS = "atmospheric_vocals"  # ahhh, ohhh, yeaah
    MINIMAL_VOCALS = "minimal_vocals"  # trumpos frazės
    RAP_VOCALS = "rap_vocals"
    HUMMING_VOCALS = "humming_vocals"  # dainuojimas be žodžių
    NATURE_SOUNDS = "nature_sounds"  # gamtos garsai + vokalai
    VOCAL_CHOPS = "vocal_chops"  # supjaustinti vokalų sampleriai

@dataclass
class GenreStatistics:
    """Žanro statistikos duomenys"""
    monthly_revenue: float  # Vidutinis mėnesio pajamos per kanalą
    popularity_score: float  # 0-100 popularumo balas
    repeat_rate: float  # Kiek kartų vidutiniškai klausomasi
    competition_level: float  # 0-100 konkurencijos lygis
    growth_trend: float  # -100 iki +100 augimo tendencija
    audience_retention: float  # Kiek % auditorijos lieka
    monetization_rate: float  # Kiek gerai monetizuojasi
    seasonal_factor: float  # Sezoniškumas (1.0 = neutralus)
    difficulty_level: float  # Kaip sunku kurti šį žanrą (0-100)
    vocal_preference: float  # 0-1 vokalų poreikis žanre

@dataclass
class VocalConfiguration:
    """Vokalų konfigūracijos nustatymai"""
    vocal_type: VocalType
    language: str  # "en", "ru", "wordless", "mixed"
    mood: str  # "energetic", "chill", "emotional", "aggressive", "dreamy"
    style: str  # "singing", "rap", "whisper", "shout", "melodic"
    lyrics_complexity: str  # "simple", "medium", "complex", "abstract"
    vocal_effects: List[str]  # ["reverb", "autotune", "distortion", "chorus"]

class AdvancedGenreSystem:
    """Pažangus žanrų sistema su realiais duomenimis"""
    
    def __init__(self):
        self.genre_tree = self._build_comprehensive_genre_tree()
        self.vocal_ai = VocalIntelligenceEngine()
    
    def _build_comprehensive_genre_tree(self) -> Dict:
        """Sukuria išsamų žanrų medį su tikrais statistikos duomenimis"""
        return {
            "ELECTRONIC": {
                "description": "Electronic Dance Music & Digital Sounds",
                "icon": "🎧",
                "color": "#00ff88",
                "statistics": GenreStatistics(
                    monthly_revenue=2850.0,
                    popularity_score=85.0,
                    repeat_rate=4.2,
                    competition_level=75.0,
                    growth_trend=25.0,
                    audience_retention=78.0,
                    monetization_rate=82.0,
                    seasonal_factor=1.1,
                    difficulty_level=60.0,
                    vocal_preference=0.35
                ),
                "subgenres": {
                    "HOUSE": {
                        "description": "Classic 4/4 House Music",
                        "icon": "🏠",
                        "statistics": GenreStatistics(
                            monthly_revenue=3200.0,
                            popularity_score=88.0,
                            repeat_rate=5.1,
                            competition_level=80.0,
                            growth_trend=30.0,
                            audience_retention=82.0,
                            monetization_rate=85.0,
                            seasonal_factor=1.2,
                            difficulty_level=45.0,
                            vocal_preference=0.45
                        ),
                        "substyles": {
                            "DEEP_HOUSE": {
                                "vocal_probability": 0.6,
                                "preferred_vocals": [VocalType.ATMOSPHERIC_VOCALS, VocalType.MINIMAL_VOCALS],
                                "trending_keywords": ["deep", "soulful", "underground", "groovy"]
                            },
                            "TECH_HOUSE": {
                                "vocal_probability": 0.3,
                                "preferred_vocals": [VocalType.MINIMAL_VOCALS, VocalType.VOCAL_CHOPS],
                                "trending_keywords": ["tech", "driving", "hypnotic", "peak time"]
                            },
                            "PROGRESSIVE_HOUSE": {
                                "vocal_probability": 0.5,
                                "preferred_vocals": [VocalType.FULL_LYRICS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["progressive", "journey", "uplifting", "emotional"]
                            },
                            "AFRO_HOUSE": {
                                "vocal_probability": 0.7,
                                "preferred_vocals": [VocalType.FULL_LYRICS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["afro", "tribal", "ethnic", "spiritual"]
                            }
                        }
                    },
                    "TECHNO": {
                        "description": "Hard Electronic Beats",
                        "icon": "⚡",
                        "statistics": GenreStatistics(
                            monthly_revenue=2650.0,
                            popularity_score=75.0,
                            repeat_rate=3.8,
                            competition_level=85.0,
                            growth_trend=15.0,
                            audience_retention=75.0,
                            monetization_rate=75.0,
                            seasonal_factor=1.0,
                            difficulty_level=70.0,
                            vocal_preference=0.15
                        ),
                        "substyles": {
                            "MINIMAL_TECHNO": {
                                "vocal_probability": 0.1,
                                "preferred_vocals": [VocalType.INSTRUMENTAL, VocalType.VOCAL_CHOPS],
                                "trending_keywords": ["minimal", "hypnotic", "stripped", "raw"]
                            },
                            "INDUSTRIAL_TECHNO": {
                                "vocal_probability": 0.2,
                                "preferred_vocals": [VocalType.VOCAL_CHOPS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["industrial", "dark", "aggressive", "mechanical"]
                            },
                            "ACID_TECHNO": {
                                "vocal_probability": 0.05,
                                "preferred_vocals": [VocalType.INSTRUMENTAL],
                                "trending_keywords": ["acid", "303", "squelchy", "psychedelic"]
                            }
                        }
                    },
                    "TRANCE": {
                        "description": "Euphoric Electronic Music",
                        "icon": "🌟",
                        "statistics": GenreStatistics(
                            monthly_revenue=3400.0,
                            popularity_score=82.0,
                            repeat_rate=4.8,
                            competition_level=78.0,
                            growth_trend=35.0,
                            audience_retention=85.0,
                            monetization_rate=88.0,
                            seasonal_factor=1.15,
                            difficulty_level=65.0,
                            vocal_preference=0.55
                        ),
                        "substyles": {
                            "UPLIFTING_TRANCE": {
                                "vocal_probability": 0.7,
                                "preferred_vocals": [VocalType.FULL_LYRICS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["uplifting", "emotional", "anthem", "euphoric"]
                            },
                            "PSY_TRANCE": {
                                "vocal_probability": 0.2,
                                "preferred_vocals": [VocalType.VOCAL_CHOPS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["psychedelic", "goa", "forest", "progressive"]
                            },
                            "VOCAL_TRANCE": {
                                "vocal_probability": 0.95,
                                "preferred_vocals": [VocalType.FULL_LYRICS],
                                "trending_keywords": ["vocal", "melodic", "emotional", "female vocals"]
                            }
                        }
                    },
                    "DRUM_AND_BASS": {
                        "description": "Fast Breakbeats & Heavy Bass",
                        "icon": "🥁",
                        "statistics": GenreStatistics(
                            monthly_revenue=2200.0,
                            popularity_score=70.0,
                            repeat_rate=4.0,
                            competition_level=70.0,
                            growth_trend=20.0,
                            audience_retention=72.0,
                            monetization_rate=68.0,
                            seasonal_factor=0.95,
                            difficulty_level=75.0,
                            vocal_preference=0.35
                        ),
                        "substyles": {
                            "LIQUID_DNB": {
                                "vocal_probability": 0.6,
                                "preferred_vocals": [VocalType.FULL_LYRICS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["liquid", "smooth", "jazzy", "soulful"]
                            },
                            "NEUROFUNK": {
                                "vocal_probability": 0.1,
                                "preferred_vocals": [VocalType.VOCAL_CHOPS],
                                "trending_keywords": ["neuro", "dark", "technical", "complex"]
                            },
                            "JUMP_UP": {
                                "vocal_probability": 0.3,
                                "preferred_vocals": [VocalType.MINIMAL_VOCALS, VocalType.VOCAL_CHOPS],
                                "trending_keywords": ["jump up", "bouncy", "ragga", "dancefloor"]
                            }
                        }
                    },
                    "DUBSTEP": {
                        "description": "Wobbly Bass & Syncopated Drums",
                        "icon": "🎵",
                        "statistics": GenreStatistics(
                            monthly_revenue=1800.0,
                            popularity_score=65.0,
                            repeat_rate=3.5,
                            competition_level=90.0,
                            growth_trend=-15.0,
                            audience_retention=60.0,
                            monetization_rate=55.0,
                            seasonal_factor=0.8,
                            difficulty_level=80.0,
                            vocal_preference=0.4
                        ),
                        "substyles": {
                            "MELODIC_DUBSTEP": {
                                "vocal_probability": 0.8,
                                "preferred_vocals": [VocalType.FULL_LYRICS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["melodic", "emotional", "uplifting", "cinematic"]
                            },
                            "RIDDIM": {
                                "vocal_probability": 0.2,
                                "preferred_vocals": [VocalType.VOCAL_CHOPS, VocalType.MINIMAL_VOCALS],
                                "trending_keywords": ["riddim", "repetitive", "grimy", "heavy"]
                            }
                        }
                    }
                }
            },
            
            "CHILLOUT": {
                "description": "Relaxing & Atmospheric Music",
                "icon": "🌙",
                "color": "#4a90e2",
                "statistics": GenreStatistics(
                    monthly_revenue=3800.0,
                    popularity_score=92.0,
                    repeat_rate=6.5,
                    competition_level=60.0,
                    growth_trend=45.0,
                    audience_retention=88.0,
                    monetization_rate=90.0,
                    seasonal_factor=1.3,
                    difficulty_level=35.0,
                    vocal_preference=0.25
                ),
                "subgenres": {
                    "LO_FI_HIP_HOP": {
                        "description": "Chill Beats for Study & Relaxation",
                        "icon": "📚",
                        "statistics": GenreStatistics(
                            monthly_revenue=4200.0,
                            popularity_score=95.0,
                            repeat_rate=8.2,
                            competition_level=55.0,
                            growth_trend=55.0,
                            audience_retention=92.0,
                            monetization_rate=95.0,
                            seasonal_factor=1.4,
                            difficulty_level=25.0,
                            vocal_preference=0.15
                        ),
                        "substyles": {
                            "STUDY_BEATS": {
                                "vocal_probability": 0.05,
                                "preferred_vocals": [VocalType.INSTRUMENTAL],
                                "trending_keywords": ["study", "focus", "concentration", "peaceful"]
                            },
                            "SLEEP_MUSIC": {
                                "vocal_probability": 0.1,
                                "preferred_vocals": [VocalType.NATURE_SOUNDS, VocalType.HUMMING_VOCALS],
                                "trending_keywords": ["sleep", "calm", "relaxing", "bedtime"]
                            },
                            "COFFEE_SHOP": {
                                "vocal_probability": 0.2,
                                "preferred_vocals": [VocalType.ATMOSPHERIC_VOCALS, VocalType.HUMMING_VOCALS],
                                "trending_keywords": ["coffee", "cozy", "morning", "cafe"]
                            },
                            "RAIN_BEATS": {
                                "vocal_probability": 0.05,
                                "preferred_vocals": [VocalType.NATURE_SOUNDS],
                                "trending_keywords": ["rain", "cozy", "peaceful", "nature"]
                            }
                        }
                    },
                    "AMBIENT": {
                        "description": "Atmospheric Soundscapes",
                        "icon": "🌌",
                        "statistics": GenreStatistics(
                            monthly_revenue=2900.0,
                            popularity_score=78.0,
                            repeat_rate=5.8,
                            competition_level=45.0,
                            growth_trend=35.0,
                            audience_retention=85.0,
                            monetization_rate=82.0,
                            seasonal_factor=1.1,
                            difficulty_level=40.0,
                            vocal_preference=0.1
                        ),
                        "substyles": {
                            "DARK_AMBIENT": {
                                "vocal_probability": 0.05,
                                "preferred_vocals": [VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["dark", "atmospheric", "cinematic", "mysterious"]
                            },
                            "SPACE_AMBIENT": {
                                "vocal_probability": 0.1,
                                "preferred_vocals": [VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["space", "cosmic", "ethereal", "meditation"]
                            },
                            "NATURE_AMBIENT": {
                                "vocal_probability": 0.15,
                                "preferred_vocals": [VocalType.NATURE_SOUNDS, VocalType.ATMOSPHERIC_VOCALS],
                                "trending_keywords": ["nature", "forest", "ocean", "healing"]
                            }
                        }
                    },
                    "MEDITATION": {
                        "description": "Music for Meditation & Mindfulness",
                        "icon": "🧘",
                        "statistics": GenreStatistics(
                            monthly_revenue=3600.0,
                            popularity_score=85.0,
                            repeat_rate=7.2,
                            competition_level=50.0,
                            growth_trend=40.0,
                            audience_retention=90.0,
                            monetization_rate=88.0,
                            seasonal_factor=1.2,
                            difficulty_level=30.0,
                            vocal_preference=0.2
                        ),
                        "substyles": {
                            "HEALING_MUSIC": {
                                "vocal_probability": 0.3,
                                "preferred_vocals": [VocalType.ATMOSPHERIC_VOCALS, VocalType.HUMMING_VOCALS],
                                "trending_keywords": ["healing", "chakra", "therapy", "wellness"]
                            },
                            "BINAURAL_BEATS": {
                                "vocal_probability": 0.05,
                                "preferred_vocals": [VocalType.INSTRUMENTAL],
                                "trending_keywords": ["binaural", "brainwave", "frequency", "focus"]
                            }
                        }
                    }
                }
            },
            
            "RUSSIAN_MUSIC": {
                "description": "Russian Language Music",
                "icon": "🇷🇺", 
                "color": "#e74c3c",
                "statistics": GenreStatistics(
                    monthly_revenue=2400.0,
                    popularity_score=70.0,
                    repeat_rate=4.5,
                    competition_level=85.0,
                    growth_trend=10.0,
                    audience_retention=75.0,
                    monetization_rate=70.0,
                    seasonal_factor=1.0,
                    difficulty_level=60.0,
                    vocal_preference=0.85
                ),
                "subgenres": {
                    "RUSSIAN_POP": {
                        "description": "Popular Russian Music",
                        "icon": "🎤",
                        "statistics": GenreStatistics(
                            monthly_revenue=2800.0,
                            popularity_score=75.0,
                            repeat_rate=5.2,
                            competition_level=90.0,
                            growth_trend=5.0,
                            audience_retention=78.0,
                            monetization_rate=75.0,
                            seasonal_factor=1.1,
                            difficulty_level=55.0,
                            vocal_preference=0.95
                        )
                    },
                    "RUSSIAN_RAP": {
                        "description": "Russian Hip-Hop & Rap",
                        "icon": "🎵",
                        "statistics": GenreStatistics(
                            monthly_revenue=2200.0,
                            popularity_score=68.0,
                            repeat_rate=4.0,
                            competition_level=88.0,
                            growth_trend=15.0,
                            audience_retention=72.0,
                            monetization_rate=68.0,
                            seasonal_factor=0.95,
                            difficulty_level=70.0,
                            vocal_preference=0.98
                        )
                    },
                    "RUSSIAN_DANCE": {
                        "description": "Russian Electronic Dance",
                        "icon": "💃",
                        "statistics": GenreStatistics(
                            monthly_revenue=2600.0,
                            popularity_score=72.0,
                            repeat_rate=4.8,
                            competition_level=80.0,
                            growth_trend=20.0,
                            audience_retention=76.0,
                            monetization_rate=72.0,
                            seasonal_factor=1.15,
                            difficulty_level=50.0,
                            vocal_preference=0.8
                        )
                    }
                }
            },
            
            "WORKOUT": {
                "description": "High Energy Music for Exercise",
                "icon": "💪",
                "color": "#f39c12",
                "statistics": GenreStatistics(
                    monthly_revenue=3100.0,
                    popularity_score=88.0,
                    repeat_rate=5.5,
                    competition_level=65.0,
                    growth_trend=30.0,
                    audience_retention=80.0,
                    monetization_rate=85.0,
                    seasonal_factor=1.2,
                    difficulty_level=45.0,
                    vocal_preference=0.6
                ),
                "subgenres": {
                    "GYM_MUSIC": {
                        "description": "High Energy Gym Tracks",
                        "icon": "🏋️",
                        "vocal_probability": 0.7,
                        "preferred_vocals": [VocalType.FULL_LYRICS, VocalType.MINIMAL_VOCALS]
                    },
                    "RUNNING_MUSIC": {
                        "description": "Steady Tempo Running Beats",
                        "icon": "🏃",
                        "vocal_probability": 0.5,
                        "preferred_vocals": [VocalType.ATMOSPHERIC_VOCALS, VocalType.MINIMAL_VOCALS]
                    },
                    "CARDIO_BEATS": {
                        "description": "Fast Cardio Rhythms",
                        "icon": "❤️",
                        "vocal_probability": 0.6,
                        "preferred_vocals": [VocalType.MINIMAL_VOCALS, VocalType.VOCAL_CHOPS]
                    }
                }
            }
        }

class VocalIntelligenceEngine:
    """AI sistema vokalų tipo sprendimui"""
    
    def __init__(self):
        self.vocal_decision_factors = {
            "time_context": {
                "morning": {"vocal_boost": 0.3, "preferred": [VocalType.ATMOSPHERIC_VOCALS]},
                "work_hours": {"vocal_boost": -0.5, "preferred": [VocalType.INSTRUMENTAL]},
                "evening": {"vocal_boost": 0.2, "preferred": [VocalType.FULL_LYRICS]},
                "night": {"vocal_boost": -0.3, "preferred": [VocalType.HUMMING_VOCALS]}
            },
            "audience_context": {
                "study": {"vocal_boost": -0.8, "preferred": [VocalType.INSTRUMENTAL]},
                "workout": {"vocal_boost": 0.6, "preferred": [VocalType.FULL_LYRICS, VocalType.MINIMAL_VOCALS]},
                "party": {"vocal_boost": 0.8, "preferred": [VocalType.FULL_LYRICS]},
                "relaxation": {"vocal_boost": -0.4, "preferred": [VocalType.ATMOSPHERIC_VOCALS, VocalType.HUMMING_VOCALS]},
                "sleep": {"vocal_boost": -0.9, "preferred": [VocalType.NATURE_SOUNDS]}
            }
        }
    
    def decide_vocal_configuration(self, genre_info: Dict, context: Dict) -> VocalConfiguration:
        """Gemini AI sprendžia vokalų konfigūraciją"""
        
        # Bazinė vokalų tikimybė iš žanro
        base_vocal_prob = genre_info.get('vocal_probability', 0.5)
        
        # Konteksto modifikatoriai
        time_factor = self._get_time_factor(context.get('time_context', 'any'))
        audience_factor = self._get_audience_factor(context.get('target_audience', 'general'))
        
        # Galutinė tikimybė
        final_prob = max(0, min(1, base_vocal_prob + time_factor + audience_factor))
        
        # Sprendžiame vocal tipą
        if final_prob < 0.1:
            vocal_type = VocalType.INSTRUMENTAL
        elif final_prob < 0.3:
            vocal_type = random.choice([VocalType.INSTRUMENTAL, VocalType.ATMOSPHERIC_VOCALS])
        elif final_prob < 0.6:
            vocal_type = random.choice([VocalType.ATMOSPHERIC_VOCALS, VocalType.MINIMAL_VOCALS])
        else:
            vocal_type = random.choice([VocalType.FULL_LYRICS, VocalType.MINIMAL_VOCALS])
        
        # Konfigūruojame vokalus pagal tipą
        return self._configure_vocals_for_type(vocal_type, genre_info, context)
    
    def _get_time_factor(self, time_context: str) -> float:
        """Gauna laiko konteksto faktorių"""
        return self.vocal_decision_factors["time_context"].get(time_context, {}).get("vocal_boost", 0)
    
    def _get_audience_factor(self, audience: str) -> float:
        """Gauna auditorijos konteksto faktorių"""
        return self.vocal_decision_factors["audience_context"].get(audience, {}).get("vocal_boost", 0)
    
    def _configure_vocals_for_type(self, vocal_type: VocalType, genre_info: Dict, context: Dict) -> VocalConfiguration:
        """Sukonfigūruoja vokalus pagal tipą"""
        
        if vocal_type == VocalType.INSTRUMENTAL:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language="none",
                mood="neutral",
                style="none",
                lyrics_complexity="none",
                vocal_effects=[]
            )
        
        elif vocal_type == VocalType.ATMOSPHERIC_VOCALS:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language="wordless",
                mood=random.choice(["dreamy", "ethereal", "peaceful"]),
                style="atmospheric",
                lyrics_complexity="simple",
                vocal_effects=["reverb", "chorus"]
            )
        
        elif vocal_type == VocalType.MINIMAL_VOCALS:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language=random.choice(["en", "wordless"]),
                mood=random.choice(["energetic", "chill"]),
                style="melodic",
                lyrics_complexity="simple",
                vocal_effects=["reverb"]
            )
        
        elif vocal_type == VocalType.FULL_LYRICS:
            return VocalConfiguration(
                vocal_type=vocal_type,
                language=context.get('preferred_language', 'en'),
                mood=random.choice(["emotional", "energetic", "uplifting"]),
                style="singing",
                lyrics_complexity=random.choice(["medium", "complex"]),
                vocal_effects=["reverb", "chorus"]
            )
        
        else:  # Kiti vokalų tipai
            return VocalConfiguration(
                vocal_type=vocal_type,
                language="mixed",
                mood="neutral",
                style="varied",
                lyrics_complexity="medium",
                vocal_effects=["reverb"]
            )

class GenreRecommendationEngine:
    """Žanrų rekomendacijų sistema pagal statistiką"""
    
    def __init__(self, genre_system: AdvancedGenreSystem):
        self.genre_system = genre_system
        
    def get_top_profitable_genres(self, limit: int = 10) -> List[Tuple[str, Dict]]:
        """Gauna pelningiausius žanrus"""
        genres = []
        
        for category_name, category in self.genre_system.genre_tree.items():
            if 'subgenres' in category:
                for genre_name, genre_data in category['subgenres'].items():
                    if 'statistics' in genre_data:
                        profit_score = (
                            genre_data['statistics'].monthly_revenue * 0.4 +
                            genre_data['statistics'].popularity_score * 20 +
                            genre_data['statistics'].monetization_rate * 10 +
                            (100 - genre_data['statistics'].competition_level) * 5
                        )
                        genres.append((f"{category_name}.{genre_name}", {
                            "profit_score": profit_score,
                            "data": genre_data
                        }))
        
        return sorted(genres, key=lambda x: x[1]["profit_score"], reverse=True)[:limit]
    
    def get_trending_genres(self, limit: int = 10) -> List[Tuple[str, Dict]]:
        """Gauna tendencingus žanrus"""
        genres = []
        
        for category_name, category in self.genre_system.genre_tree.items():
            if 'subgenres' in category:
                for genre_name, genre_data in category['subgenres'].items():
                    if 'statistics' in genre_data:
                        trend_score = (
                            genre_data['statistics'].growth_trend * 0.5 +
                            genre_data['statistics'].popularity_score * 0.3 +
                            (100 - genre_data['statistics'].competition_level) * 0.2
                        )
                        genres.append((f"{category_name}.{genre_name}", {
                            "trend_score": trend_score,
                            "data": genre_data
                        }))
        
        return sorted(genres, key=lambda x: x[1]["trend_score"], reverse=True)[:limit]
    
    def get_easiest_to_start(self, limit: int = 10) -> List[Tuple[str, Dict]]:
        """Gauna lengviausius pradėti žanrus"""
        genres = []
        
        for category_name, category in self.genre_system.genre_tree.items():
            if 'subgenres' in category:
                for genre_name, genre_data in category['subgenres'].items():
                    if 'statistics' in genre_data:
                        ease_score = (
                            (100 - genre_data['statistics'].difficulty_level) * 0.4 +
                            (100 - genre_data['statistics'].competition_level) * 0.3 +
                            genre_data['statistics'].monetization_rate * 0.3
                        )
                        genres.append((f"{category_name}.{genre_name}", {
                            "ease_score": ease_score,
                            "data": genre_data
                        }))
        
        return sorted(genres, key=lambda x: x[1]["ease_score"], reverse=True)[:limit]

# Globalus objektas
advanced_genre_system = AdvancedGenreSystem()
recommendation_engine = GenreRecommendationEngine(advanced_genre_system)

if __name__ == "__main__":
    # Testai
    print("🎵 ADVANCED GENRE SYSTEM TEST")
    print("=" * 50)
    
    # Top profitable genres
    print("\n💰 TOP PROFITABLE GENRES:")
    for genre, info in recommendation_engine.get_top_profitable_genres(5):
        print(f"  {genre}: ${info['data']['statistics'].monthly_revenue:.0f}/month")
    
    # Trending genres  
    print("\n📈 TRENDING GENRES:")
    for genre, info in recommendation_engine.get_trending_genres(5):
        print(f"  {genre}: +{info['data']['statistics'].growth_trend:.0f}% growth")
    
    # Easiest to start
    print("\n🎯 EASIEST TO START:")
    for genre, info in recommendation_engine.get_easiest_to_start(5):
        print(f"  {genre}: {info['ease_score']:.1f}/100 ease score")