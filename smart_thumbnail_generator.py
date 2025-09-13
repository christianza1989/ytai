#!/usr/bin/env python3
"""
Smart Thumbnail Generator - AI-Powered YouTube Thumbnail Creation
Automatic thumbnail generation with CTR optimization and A/B testing
"""

import os
import json
import random
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class SmartThumbnailGenerator:
    """AI-powered thumbnail generator su CTR optimizavimu"""
    
    def __init__(self):
        self.style_templates = self.load_thumbnail_templates()
        self.ctr_data = {}
        self.ab_test_results = {}
        
    def load_thumbnail_templates(self):
        """Įkelia thumbnail template'us kiekvienam stiliui"""
        return {
            'lofi': {
                'color_schemes': [
                    {'primary': '#FFB6C1', 'secondary': '#DDA0DD', 'accent': '#98FB98'},  # Pastel
                    {'primary': '#FFA07A', 'secondary': '#20B2AA', 'accent': '#F0E68C'},  # Warm
                    {'primary': '#D8BFD8', 'secondary': '#FFE4E1', 'accent': '#F5DEB3'},  # Soft
                    {'primary': '#B0E0E6', 'secondary': '#F0F8FF', 'accent': '#FFEFD5'}   # Cool
                ],
                'visual_elements': [
                    'cozy room with plants',
                    'coffee cup and books',
                    'vinyl record player',
                    'rain on window',
                    'neon city night',
                    'anime girl studying',
                    'minimalist desk setup',
                    'sunset landscape'
                ],
                'text_styles': [
                    {'font': 'bold', 'size': 'large', 'position': 'center'},
                    {'font': 'clean', 'size': 'medium', 'position': 'bottom'},
                    {'font': 'modern', 'size': 'large', 'position': 'top'}
                ],
                'trending_elements': [
                    '🎵 music notes',
                    '📚 study elements', 
                    '☕ coffee vibes',
                    '🌧️ rain aesthetic',
                    '🌙 night mood',
                    '✨ sparkle effects'
                ]
            },
            'trap': {
                'color_schemes': [
                    {'primary': '#FF0000', 'secondary': '#000000', 'accent': '#FFD700'},  # Red/Black/Gold
                    {'primary': '#800080', 'secondary': '#000000', 'accent': '#00FF00'},  # Purple/Black/Green  
                    {'primary': '#FF1493', 'secondary': '#000000', 'accent': '#00FFFF'},  # Pink/Black/Cyan
                    {'primary': '#FFA500', 'secondary': '#000000', 'accent': '#FF69B4'}   # Orange/Black/Pink
                ],
                'visual_elements': [
                    'dark urban street',
                    'money stacks',
                    'luxury cars',
                    'studio equipment',
                    'neon lights', 
                    'graffiti walls',
                    'diamond jewelry',
                    'smoke effects'
                ],
                'text_styles': [
                    {'font': 'bold', 'size': 'extra_large', 'position': 'center'},
                    {'font': 'street', 'size': 'large', 'position': 'diagonal'},
                    {'font': 'impact', 'size': 'large', 'position': 'bottom'}
                ],
                'trending_elements': [
                    '🔥 fire effects',
                    '💰 money symbols',
                    '👑 crown icons',
                    '💎 diamond graphics',
                    '🎤 microphone',
                    '⚡ lightning bolts'
                ]
            },
            'meditation': {
                'color_schemes': [
                    {'primary': '#E6E6FA', 'secondary': '#F0F8FF', 'accent': '#FFE4B5'},  # Lavender
                    {'primary': '#98FB98', 'secondary': '#F0FFF0', 'accent': '#FFFACD'},  # Nature
                    {'primary': '#DDA0DD', 'secondary': '#FFF8DC', 'accent': '#E0FFFF'},  # Spiritual  
                    {'primary': '#F5DEB3', 'secondary': '#FFF5EE', 'accent': '#F0E68C'}   # Golden
                ],
                'visual_elements': [
                    'lotus flower',
                    'mandala patterns', 
                    'peaceful nature',
                    'golden light rays',
                    'chakra symbols',
                    'zen garden',
                    'mountain landscape',
                    'crystal formations'
                ],
                'text_styles': [
                    {'font': 'elegant', 'size': 'medium', 'position': 'center'},
                    {'font': 'serif', 'size': 'large', 'position': 'top'},
                    {'font': 'zen', 'size': 'medium', 'position': 'bottom'}
                ],
                'trending_elements': [
                    '🧘‍♀️ meditation pose',
                    '🕯️ candle light',
                    '🌸 cherry blossoms', 
                    '☯️ yin yang symbol',
                    '🔮 crystal ball',
                    '✨ sparkle aura'
                ]
            },
            'gaming': {
                'color_schemes': [
                    {'primary': '#00FF00', 'secondary': '#000000', 'accent': '#FF0000'},  # Matrix
                    {'primary': '#FF6600', 'secondary': '#000000', 'accent': '#FFFF00'},  # Fire
                    {'primary': '#0080FF', 'secondary': '#000000', 'accent': '#FF00FF'},  # Cyber
                    {'primary': '#FF0080', 'secondary': '#000000', 'accent': '#00FFFF'}   # Neon
                ],
                'visual_elements': [
                    'epic warrior character',
                    'futuristic cityscape',
                    'battle arena',
                    'gaming setup',
                    'digital landscape',
                    'spaceship combat',
                    'fantasy castle',
                    'cyberpunk streets'
                ],
                'text_styles': [
                    {'font': 'futuristic', 'size': 'extra_large', 'position': 'center'},
                    {'font': 'game', 'size': 'large', 'position': 'diagonal'},
                    {'font': 'cyber', 'size': 'large', 'position': 'corner'}
                ],
                'trending_elements': [
                    '🎮 game controller',
                    '⚔️ sword weapons',
                    '🏆 trophy victory',
                    '🔥 epic effects',
                    '⚡ power symbols',
                    '👾 pixel art'
                ]
            }
        }
    
    def generate_thumbnail_prompt(self, style: str, title: str, mood: str = None) -> str:
        """Generuoja AI prompt thumbnail generavimui"""
        
        template = self.style_templates.get(style, self.style_templates['lofi'])
        
        # Select random elements
        color_scheme = random.choice(template['color_schemes'])
        visual_element = random.choice(template['visual_elements'])
        text_style = random.choice(template['text_styles'])
        trending_element = random.choice(template['trending_elements'])
        
        # Build prompt based on style
        if style == 'lofi':
            prompt = f"""Create a cozy, aesthetic lo-fi thumbnail featuring {visual_element}. 
            Color palette: {color_scheme['primary']} and {color_scheme['secondary']} with {color_scheme['accent']} accents.
            Include {trending_element} in a minimalist, calming design.
            Style: soft lighting, dreamy atmosphere, study/chill vibes.
            Text placement: {text_style['position']} with {text_style['font']} font.
            Make it perfect for YouTube lo-fi music video."""
            
        elif style == 'trap':
            prompt = f"""Create a bold, street-style thumbnail featuring {visual_element}.
            Color palette: dominant {color_scheme['primary']} with {color_scheme['secondary']} and {color_scheme['accent']} accents.
            Include {trending_element} with dramatic lighting and urban aesthetic.
            Style: high contrast, gritty, powerful, money/success themes.
            Text placement: {text_style['position']} with {text_style['font']} font style.
            Make it eye-catching for YouTube trap music video."""
            
        elif style == 'meditation':
            prompt = f"""Create a peaceful, spiritual thumbnail featuring {visual_element}.
            Color palette: soft {color_scheme['primary']} and {color_scheme['secondary']} with gentle {color_scheme['accent']} highlights.
            Include {trending_element} in a serene, healing composition.
            Style: soft lighting, ethereal glow, spiritual energy, calming atmosphere.
            Text placement: {text_style['position']} with elegant {text_style['font']} typography.
            Make it perfect for YouTube meditation/healing frequency video."""
            
        elif style == 'gaming':
            prompt = f"""Create an epic, high-energy thumbnail featuring {visual_element}.
            Color palette: vibrant {color_scheme['primary']} with {color_scheme['secondary']} and {color_scheme['accent']} accents.
            Include {trending_element} with dynamic action and futuristic elements.
            Style: intense lighting, digital effects, epic atmosphere, victory themes.
            Text placement: {text_style['position']} with {text_style['font']} gaming font.
            Make it exciting for YouTube gaming music video."""
        
        # Add title integration
        prompt += f"\n\nTitle to integrate: '{title}'"
        prompt += f"\nMood: {mood or 'engaging'}"
        prompt += "\nResolution: 1280x720, YouTube thumbnail optimized"
        prompt += "\nMake it click-worthy and algorithm-friendly!"
        
        return prompt
    
    def generate_thumbnail_variants(self, style: str, title: str, mood: str = None, variant_count: int = 3) -> List[Dict]:
        """Generuoja kelis thumbnail variantus A/B testingui"""
        
        variants = []
        
        for i in range(variant_count):
            # Generate unique prompt for each variant
            prompt = self.generate_thumbnail_prompt(style, title, mood)
            
            # Create variant with different emphasis
            variant_modifications = [
                "with more text emphasis",
                "with stronger visual impact", 
                "with better color contrast",
                "with trending elements highlighted",
                "with emotional appeal enhanced"
            ]
            
            modified_prompt = prompt + f". {random.choice(variant_modifications)}"
            
            variant_data = {
                'variant_id': f"{style}_thumb_v{i+1}_{int(datetime.now().timestamp())}",
                'prompt': modified_prompt,
                'style': style,
                'title': title,
                'mood': mood,
                'created_at': datetime.now().isoformat(),
                'ctr_data': {
                    'impressions': 0,
                    'clicks': 0,
                    'ctr': 0.0
                },
                'ab_test_group': f'group_{chr(65+i)}'  # A, B, C, etc.
            }
            
            # Simulate thumbnail generation (in production would call DALL-E API)
            variant_data['thumbnail_path'] = self.create_mock_thumbnail(variant_data)
            
            variants.append(variant_data)
        
        return variants
    
    def create_mock_thumbnail(self, variant_data: Dict) -> str:
        """Sukuria mock thumbnail failą (production'e naudoti DALL-E API)"""
        
        # Create simple colored rectangle as placeholder
        style = variant_data['style']
        template = self.style_templates[style]
        color_scheme = random.choice(template['color_schemes'])
        
        # Create thumbnail directory
        thumb_dir = Path('output/thumbnails')
        thumb_dir.mkdir(parents=True, exist_ok=True)
        
        # Create simple thumbnail with PIL
        img = Image.new('RGB', (1280, 720), color=color_scheme['primary'])
        draw = ImageDraw.Draw(img)
        
        # Add style-specific visual elements
        if style == 'lofi':
            # Soft gradient effect
            for i in range(720):
                alpha = i / 720
                color = tuple(int(c * (1 - alpha * 0.3)) for c in Image.new('RGB', (1, 1), color_scheme['secondary']).getpixel((0, 0)))
                draw.line([(0, i), (1280, i)], fill=color)
        
        elif style == 'trap':
            # Bold geometric shapes  
            draw.rectangle([100, 100, 1180, 620], outline=color_scheme['accent'], width=10)
            draw.rectangle([200, 200, 1080, 520], fill=color_scheme['secondary'])
        
        elif style == 'meditation':
            # Circular mandala-like pattern
            center_x, center_y = 640, 360
            for radius in range(50, 300, 50):
                draw.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius], 
                           outline=color_scheme['accent'], width=3)
        
        elif style == 'gaming':
            # Tech grid pattern
            for x in range(0, 1280, 100):
                draw.line([(x, 0), (x, 720)], fill=color_scheme['accent'], width=2)
            for y in range(0, 720, 50):
                draw.line([(0, y), (1280, y)], fill=color_scheme['accent'], width=1)
        
        # Add title text (simplified)
        title = variant_data['title'][:30] + '...' if len(variant_data['title']) > 30 else variant_data['title']
        
        try:
            # Try to use a font (might not be available in sandbox)
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Add text with outline for readability
        text_x, text_y = 640, 360
        
        # Text outline
        for adj in range(-3, 4):
            for adj2 in range(-3, 4):
                draw.text((text_x + adj, text_y + adj2), title, font=font, fill='black', anchor="mm")
        
        # Main text
        draw.text((text_x, text_y), title, font=font, fill='white', anchor="mm")
        
        # Save thumbnail
        thumb_path = thumb_dir / f"{variant_data['variant_id']}.jpg"
        img.save(thumb_path, 'JPEG', quality=85)
        
        return str(thumb_path)
    
    def analyze_thumbnail_performance(self, variant_id: str, impressions: int, clicks: int):
        """Analizuoja thumbnail performance A/B testingui"""
        
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        
        performance_data = {
            'variant_id': variant_id,
            'impressions': impressions,
            'clicks': clicks,
            'ctr': round(ctr, 2),
            'performance_tier': self.get_performance_tier(ctr),
            'optimization_suggestions': self.get_optimization_suggestions(ctr),
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Store in CTR database
        self.ctr_data[variant_id] = performance_data
        
        return performance_data
    
    def get_performance_tier(self, ctr: float) -> str:
        """Nustato performance tier pagal CTR"""
        if ctr >= 12.0:
            return 'EXCELLENT'
        elif ctr >= 8.0:
            return 'GOOD'
        elif ctr >= 5.0:
            return 'AVERAGE'
        elif ctr >= 2.0:
            return 'POOR'
        else:
            return 'VERY_POOR'
    
    def get_optimization_suggestions(self, ctr: float) -> List[str]:
        """Grąžina optimizacijos patarimus"""
        suggestions = []
        
        if ctr < 2.0:
            suggestions.extend([
                "Try brighter, more contrasting colors",
                "Increase text size and make it more readable",
                "Add more emotional/trending elements",
                "Simplify the design - less clutter"
            ])
        elif ctr < 5.0:
            suggestions.extend([
                "Experiment with different text positioning",
                "Add more visual hierarchy", 
                "Try different color combinations",
                "Include trending visual elements"
            ])
        elif ctr < 8.0:
            suggestions.extend([
                "Fine-tune color balance",
                "Test different font styles",
                "Optimize for mobile viewing"
            ])
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def run_ab_test_analysis(self, variants: List[Dict]) -> Dict:
        """Paleidžia A/B test analizę su mock duomenimis"""
        
        results = {
            'test_id': f"test_{int(datetime.now().timestamp())}",
            'started_at': datetime.now().isoformat(),
            'variants_tested': len(variants),
            'variant_results': [],
            'winner': None,
            'performance_insights': {}
        }
        
        # Simulate performance data for each variant
        for i, variant in enumerate(variants):
            # Simulate realistic CTR data based on style
            style = variant['style']
            
            # Base CTR by style (realistic YouTube averages)
            base_ctrs = {
                'lofi': 6.5,      # Lo-fi has good engagement
                'trap': 4.2,      # Trap is competitive  
                'meditation': 8.1, # Meditation has dedicated audience
                'gaming': 5.8     # Gaming has massive audience
            }
            
            base_ctr = base_ctrs.get(style, 5.0)
            
            # Add random variation (some thumbnails perform better)
            variation = random.uniform(-2.0, 4.0)
            final_ctr = max(0.1, base_ctr + variation)
            
            # Generate mock impressions and clicks
            impressions = random.randint(1000, 10000)
            clicks = int(impressions * (final_ctr / 100))
            
            # Analyze performance
            performance = self.analyze_thumbnail_performance(
                variant['variant_id'], 
                impressions, 
                clicks
            )
            
            results['variant_results'].append({
                'variant': variant,
                'performance': performance
            })
        
        # Find winner (highest CTR)
        if results['variant_results']:
            winner = max(results['variant_results'], key=lambda x: x['performance']['ctr'])
            results['winner'] = winner
            
            # Calculate performance insights
            ctrs = [v['performance']['ctr'] for v in results['variant_results']]
            results['performance_insights'] = {
                'best_ctr': max(ctrs),
                'worst_ctr': min(ctrs),
                'average_ctr': sum(ctrs) / len(ctrs),
                'improvement_potential': max(ctrs) - min(ctrs),
                'statistical_significance': len(ctrs) >= 3 and (max(ctrs) - min(ctrs)) > 1.0
            }
        
        return results
    
    def generate_comprehensive_thumbnail_package(self, style: str, title: str, mood: str = None) -> Dict:
        """Generuoja pilną thumbnail paketą su A/B testavimu"""
        
        # Generate multiple variants
        variants = self.generate_thumbnail_variants(style, title, mood, variant_count=3)
        
        # Run A/B test simulation
        ab_test_results = self.run_ab_test_analysis(variants)
        
        # Calculate ROI potential
        roi_analysis = self.calculate_thumbnail_roi(ab_test_results)
        
        package = {
            'package_id': f"thumb_pkg_{int(datetime.now().timestamp())}",
            'style': style,
            'title': title,
            'mood': mood,
            'variants_generated': variants,
            'ab_test_results': ab_test_results,
            'roi_analysis': roi_analysis,
            'recommendations': self.get_package_recommendations(ab_test_results),
            'generated_at': datetime.now().isoformat()
        }
        
        return package
    
    def calculate_thumbnail_roi(self, ab_test_results: Dict) -> Dict:
        """Apskaičiuoja thumbnail ROI potencialą"""
        
        if not ab_test_results.get('winner'):
            return {'roi_potential': 0, 'additional_revenue': 0}
        
        winner_ctr = ab_test_results['winner']['performance']['ctr']
        baseline_ctr = 3.5  # Average YouTube thumbnail CTR
        
        # Calculate improvement
        ctr_improvement = winner_ctr - baseline_ctr
        improvement_percent = (ctr_improvement / baseline_ctr) * 100 if baseline_ctr > 0 else 0
        
        # Estimate revenue impact (simplified)
        avg_monthly_views = 50000  # Conservative estimate per video
        avg_rpm = 2.50  # Average RPM
        
        baseline_revenue = (avg_monthly_views / 1000) * avg_rpm
        improved_revenue = ((avg_monthly_views * (winner_ctr / baseline_ctr)) / 1000) * avg_rpm
        additional_revenue = improved_revenue - baseline_revenue
        
        return {
            'ctr_improvement_percent': round(improvement_percent, 1),
            'baseline_ctr': baseline_ctr,
            'optimized_ctr': round(winner_ctr, 2),
            'baseline_monthly_revenue': round(baseline_revenue, 2),
            'improved_monthly_revenue': round(improved_revenue, 2),
            'additional_monthly_revenue': round(additional_revenue, 2),
            'annual_revenue_boost': round(additional_revenue * 12, 2),
            'roi_multiplier': round(improved_revenue / baseline_revenue, 2) if baseline_revenue > 0 else 1.0
        }
    
    def get_package_recommendations(self, ab_test_results: Dict) -> List[str]:
        """Grąžina rekomendacijas thumbnail optimizacijai"""
        
        recommendations = []
        
        if ab_test_results.get('winner'):
            winner_ctr = ab_test_results['winner']['performance']['ctr']
            
            if winner_ctr > 8.0:
                recommendations.append("🎉 Excellent performance! Use this thumbnail style for future videos")
                recommendations.append("💡 Analyze winning elements and apply to other thumbnails")
            elif winner_ctr > 5.0:
                recommendations.append("👍 Good performance! Consider A/B testing refinements")
                recommendations.append("🔧 Test minor variations to optimize further")
            else:
                recommendations.append("⚠️ Below average performance - try different approach")
                recommendations.append("🎨 Experiment with bolder colors and larger text")
        
        insights = ab_test_results.get('performance_insights', {})
        if insights.get('improvement_potential', 0) > 2.0:
            recommendations.append("📊 High variation between variants - more testing recommended")
        
        return recommendations


# Example usage and API integration
if __name__ == "__main__":
    print("🎨 Smart Thumbnail Generator - Demo")
    
    generator = SmartThumbnailGenerator()
    
    # Test different styles
    test_cases = [
        {'style': 'lofi', 'title': 'Chill Study Beats - Perfect for Focus [2 Hours]', 'mood': 'relaxed'},
        {'style': 'trap', 'title': 'FREE Hard Trap Beat - "Money Moves" | Type Beat 2024', 'mood': 'aggressive'},
        {'style': 'meditation', 'title': '432Hz Healing Frequency - Deep Meditation Music', 'mood': 'peaceful'},
        {'style': 'gaming', 'title': 'EPIC Boss Battle Music - Ultimate Gaming Soundtrack', 'mood': 'intense'}
    ]
    
    total_roi_potential = 0
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"🎯 Testing: {test_case['style'].upper()} Style")
        print(f"📝 Title: {test_case['title'][:50]}...")
        
        # Generate comprehensive package
        package = generator.generate_comprehensive_thumbnail_package(
            style=test_case['style'],
            title=test_case['title'],
            mood=test_case['mood']
        )
        
        # Display results
        winner = package['ab_test_results']['winner']
        roi = package['roi_analysis']
        
        print(f"🏆 Winner CTR: {winner['performance']['ctr']}%")
        print(f"📈 CTR Improvement: +{roi['ctr_improvement_percent']}%")
        print(f"💰 Additional Monthly Revenue: ${roi['additional_monthly_revenue']}")
        print(f"🎯 Performance Tier: {winner['performance']['performance_tier']}")
        
        total_roi_potential += roi['additional_monthly_revenue']
        
        print("💡 Recommendations:")
        for rec in package['recommendations'][:2]:
            print(f"   • {rec}")
    
    print(f"\n🚀 TOTAL THUMBNAIL OPTIMIZATION POTENTIAL:")
    print(f"💰 Additional Monthly Revenue: ${total_roi_potential:.2f}")
    print(f"📈 Annual Revenue Boost: ${total_roi_potential * 12:.2f}")
    print(f"🎉 ROI Timeline: Immediate (1-2 days after deployment)")
    
    # Save sample package for inspection
    sample_package = generator.generate_comprehensive_thumbnail_package(
        'lofi', 'Demo Lo-Fi Beats for Testing', 'chill'
    )
    
    with open('thumbnail_package_sample.json', 'w') as f:
        json.dump(sample_package, f, indent=2, default=str)
    
    print(f"\n📄 Sample package saved to: thumbnail_package_sample.json")
    print(f"🎨 Thumbnail files created in: output/thumbnails/")
    print(f"✅ Smart Thumbnail Generator ready for integration!")