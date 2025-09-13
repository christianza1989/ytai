#!/usr/bin/env python3
"""
YouTube Profit Tracking & Analytics System
Advanced profit monitoring, trend analysis, and revenue optimization
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import statistics
import random

class ProfitTracker:
    """YouTube pelno sekimas ir analitika"""
    
    def __init__(self, db_path: str = "youtube_profits.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for profit tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Channels table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                style TEXT NOT NULL,
                created_date DATE,
                subscribers INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0.0,
                average_rpm REAL DEFAULT 0.0,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                channel_id TEXT,
                title TEXT,
                upload_date DATE,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0.0,
                rpm REAL DEFAULT 0.0,
                watch_time_hours REAL DEFAULT 0.0,
                ctr REAL DEFAULT 0.0,
                seo_score INTEGER DEFAULT 0,
                FOREIGN KEY (channel_id) REFERENCES channels (id)
            )
        ''')
        
        # Daily analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_analytics (
                date DATE,
                channel_id TEXT,
                views INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0.0,
                watch_time_hours REAL DEFAULT 0.0,
                new_subscribers INTEGER DEFAULT 0,
                PRIMARY KEY (date, channel_id),
                FOREIGN KEY (channel_id) REFERENCES channels (id)
            )
        ''')
        
        # Revenue goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT,
                month TEXT,
                target_revenue REAL,
                actual_revenue REAL DEFAULT 0.0,
                target_views INTEGER,
                actual_views INTEGER DEFAULT 0,
                FOREIGN KEY (channel_id) REFERENCES channels (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Populate with sample data if empty
        self.populate_sample_data()
    
    def populate_sample_data(self):
        """Populate database with sample data for demo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM channels")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample channels
        channels_data = [
            ('lofi_study_vibes', 'Lo-Fi Study Vibes', 'lofi', '2024-01-15', 12500, 850000, 2150.00, 2.53),
            ('trap_beast_beats', 'Trap Beast Beats', 'trap', '2024-02-01', 8900, 520000, 980.00, 1.88),
            ('healing_frequencies', 'Healing Frequencies 432Hz', 'meditation', '2024-01-20', 15200, 420000, 1680.00, 4.00),
            ('epic_gaming_sounds', 'Epic Gaming Sounds', 'gaming', '2024-02-10', 22100, 1200000, 2760.00, 2.30),
        ]
        
        cursor.executemany('''
            INSERT INTO channels (id, name, style, created_date, subscribers, total_views, total_revenue, average_rpm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', channels_data)
        
        # Generate sample video data
        video_id_counter = 1
        for channel_id, channel_name, style, _, _, _, _, _ in channels_data:
            # Generate 20-30 videos per channel
            for i in range(random.randint(20, 30)):
                upload_date = datetime.now() - timedelta(days=random.randint(1, 90))
                
                # Style-specific data
                if style == 'lofi':
                    views = random.randint(3000, 45000)
                    rpm = random.uniform(2.0, 4.5)
                elif style == 'trap':
                    views = random.randint(2000, 25000)
                    rpm = random.uniform(1.2, 3.0)
                elif style == 'meditation':
                    views = random.randint(1500, 20000)
                    rpm = random.uniform(3.0, 5.5)
                else:  # gaming
                    views = random.randint(8000, 80000)
                    rpm = random.uniform(1.8, 3.5)
                
                revenue = (views / 1000) * rpm
                likes = views * random.uniform(0.02, 0.08)  # 2-8% like rate
                comments = views * random.uniform(0.005, 0.02)  # 0.5-2% comment rate
                watch_time = views * random.uniform(0.5, 2.5)  # Average watch time per view
                ctr = random.uniform(2.0, 12.0)  # Click-through rate
                seo_score = random.randint(45, 95)
                
                video_data = (
                    f"video_{video_id_counter:04d}",
                    channel_id,
                    f"Generated {style.title()} Video #{i+1}",
                    upload_date.date(),
                    int(views),
                    int(likes),
                    int(comments),
                    round(revenue, 2),
                    round(rpm, 2),
                    round(watch_time, 1),
                    round(ctr, 1),
                    seo_score
                )
                
                cursor.execute('''
                    INSERT INTO videos 
                    (id, channel_id, title, upload_date, views, likes, comments, revenue, rpm, watch_time_hours, ctr, seo_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', video_data)
                
                video_id_counter += 1
        
        # Generate daily analytics for last 30 days
        for channel_id, _, _, _, _, _, _, _ in channels_data:
            for i in range(30):
                date = (datetime.now() - timedelta(days=i)).date()
                daily_views = random.randint(100, 2000)
                daily_revenue = daily_views * random.uniform(0.002, 0.008)
                daily_watch_time = daily_views * random.uniform(0.3, 1.8)
                new_subs = random.randint(0, 50)
                
                cursor.execute('''
                    INSERT INTO daily_analytics (date, channel_id, views, revenue, watch_time_hours, new_subscribers)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (date, channel_id, daily_views, round(daily_revenue, 2), round(daily_watch_time, 1), new_subs))
        
        # Set revenue goals
        current_month = datetime.now().strftime('%Y-%m')
        for channel_id, _, style, _, _, _, _, _ in channels_data:
            if style == 'lofi':
                target_revenue = 800.0
                target_views = 300000
            elif style == 'trap':
                target_revenue = 450.0
                target_views = 250000
            elif style == 'meditation':
                target_revenue = 650.0
                target_views = 180000
            else:  # gaming
                target_revenue = 950.0
                target_views = 400000
            
            # Current month actuals (partial)
            actual_revenue = target_revenue * random.uniform(0.3, 0.8)
            actual_views = target_views * random.uniform(0.3, 0.8)
            
            cursor.execute('''
                INSERT INTO revenue_goals (channel_id, month, target_revenue, actual_revenue, target_views, actual_views)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (channel_id, current_month, target_revenue, actual_revenue, target_views, int(actual_views)))
        
        conn.commit()
        conn.close()
    
    def get_empire_overview(self) -> Dict:
        """Get comprehensive empire performance overview"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total channels and basic stats
        cursor.execute('''
            SELECT 
                COUNT(*) as total_channels,
                SUM(subscribers) as total_subscribers,
                SUM(total_views) as total_views,
                SUM(total_revenue) as total_revenue,
                AVG(average_rpm) as avg_rpm
            FROM channels WHERE status = 'active'
        ''')
        basic_stats = cursor.fetchone()
        
        # Monthly performance (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).date()
        cursor.execute('''
            SELECT 
                SUM(views) as monthly_views,
                SUM(revenue) as monthly_revenue,
                SUM(watch_time_hours) as monthly_watch_time,
                SUM(new_subscribers) as monthly_new_subs
            FROM daily_analytics 
            WHERE date >= ?
        ''', (thirty_days_ago,))
        monthly_stats = cursor.fetchone()
        
        # Video count (last 30 days)
        cursor.execute('''
            SELECT COUNT(*) 
            FROM videos 
            WHERE upload_date >= ?
        ''', (thirty_days_ago,))
        monthly_videos = cursor.fetchone()[0]
        
        # Growth rate (compare to previous 30 days)
        sixty_days_ago = (datetime.now() - timedelta(days=60)).date()
        cursor.execute('''
            SELECT 
                SUM(views) as prev_views,
                SUM(revenue) as prev_revenue
            FROM daily_analytics 
            WHERE date >= ? AND date < ?
        ''', (sixty_days_ago, thirty_days_ago))
        prev_stats = cursor.fetchone()
        
        # Calculate growth rates
        views_growth = 0
        revenue_growth = 0
        if prev_stats[0] and prev_stats[0] > 0:
            views_growth = ((monthly_stats[0] - prev_stats[0]) / prev_stats[0]) * 100
        if prev_stats[1] and prev_stats[1] > 0:
            revenue_growth = ((monthly_stats[1] - prev_stats[1]) / prev_stats[1]) * 100
        
        conn.close()
        
        return {
            'total_channels': basic_stats[0],
            'total_subscribers': basic_stats[1] or 0,
            'total_views': basic_stats[2] or 0,
            'total_revenue': round(basic_stats[3] or 0, 2),
            'average_rpm': round(basic_stats[4] or 0, 2),
            'monthly_performance': {
                'views': monthly_stats[0] or 0,
                'revenue': round(monthly_stats[1] or 0, 2),
                'watch_time_hours': round(monthly_stats[2] or 0, 1),
                'new_subscribers': monthly_stats[3] or 0,
                'videos_uploaded': monthly_videos,
                'views_growth_percent': round(views_growth, 1),
                'revenue_growth_percent': round(revenue_growth, 1)
            }
        }
    
    def get_channel_performance(self, days: int = 30) -> List[Dict]:
        """Get detailed performance by channel"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).date()
        
        cursor.execute('''
            SELECT 
                c.id,
                c.name,
                c.style,
                c.subscribers,
                c.total_revenue,
                c.average_rpm,
                COALESCE(SUM(da.views), 0) as period_views,
                COALESCE(SUM(da.revenue), 0) as period_revenue,
                COALESCE(SUM(da.watch_time_hours), 0) as period_watch_time,
                COALESCE(SUM(da.new_subscribers), 0) as period_new_subs,
                COUNT(v.id) as period_videos
            FROM channels c
            LEFT JOIN daily_analytics da ON c.id = da.channel_id AND da.date >= ?
            LEFT JOIN videos v ON c.id = v.channel_id AND v.upload_date >= ?
            WHERE c.status = 'active'
            GROUP BY c.id, c.name, c.style, c.subscribers, c.total_revenue, c.average_rpm
            ORDER BY period_revenue DESC
        ''', (start_date, start_date))
        
        results = []
        for row in cursor.fetchall():
            channel_data = {
                'id': row[0],
                'name': row[1],
                'style': row[2],
                'subscribers': row[3],
                'total_revenue': round(row[4], 2),
                'average_rpm': round(row[5], 2),
                'period_performance': {
                    'views': row[6],
                    'revenue': round(row[7], 2),
                    'watch_time_hours': round(row[8], 1),
                    'new_subscribers': row[9],
                    'videos_uploaded': row[10]
                }
            }
            
            # Calculate performance metrics
            if row[6] > 0:  # If there are views
                channel_data['period_performance']['rpm'] = round((row[7] / row[6]) * 1000, 2)
                channel_data['period_performance']['avg_watch_time_per_view'] = round(row[8] / row[6], 2)
            else:
                channel_data['period_performance']['rpm'] = 0
                channel_data['period_performance']['avg_watch_time_per_view'] = 0
            
            results.append(channel_data)
        
        conn.close()
        return results
    
    def get_revenue_projections(self) -> Dict:
        """Calculate revenue projections based on current trends"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last 7 days average
        week_ago = (datetime.now() - timedelta(days=7)).date()
        cursor.execute('''
            SELECT 
                AVG(daily_revenue) as avg_daily_revenue,
                AVG(daily_views) as avg_daily_views
            FROM (
                SELECT 
                    date,
                    SUM(revenue) as daily_revenue,
                    SUM(views) as daily_views
                FROM daily_analytics 
                WHERE date >= ?
                GROUP BY date
            )
        ''', (week_ago,))
        
        weekly_avg = cursor.fetchone()
        daily_revenue = weekly_avg[0] or 0
        daily_views = weekly_avg[1] or 0
        
        # Calculate projections
        projections = {
            'daily': round(daily_revenue, 2),
            'weekly': round(daily_revenue * 7, 2),
            'monthly': round(daily_revenue * 30, 2),
            'quarterly': round(daily_revenue * 90, 2),
            'yearly': round(daily_revenue * 365, 2),
            'views_per_day': int(daily_views),
            'views_per_month': int(daily_views * 30)
        }
        
        # Get revenue goals progress
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute('''
            SELECT 
                SUM(target_revenue) as total_target,
                SUM(actual_revenue) as total_actual,
                SUM(target_views) as views_target,
                SUM(actual_views) as views_actual
            FROM revenue_goals 
            WHERE month = ?
        ''', (current_month,))
        
        goals_data = cursor.fetchone()
        if goals_data[0]:
            projections['monthly_goal'] = {
                'target_revenue': round(goals_data[0], 2),
                'actual_revenue': round(goals_data[1] or 0, 2),
                'revenue_progress_percent': round(((goals_data[1] or 0) / goals_data[0]) * 100, 1),
                'target_views': goals_data[2],
                'actual_views': goals_data[3] or 0,
                'views_progress_percent': round(((goals_data[3] or 0) / goals_data[2]) * 100, 1)
            }
        
        conn.close()
        return projections
    
    def get_top_performing_videos(self, limit: int = 10, metric: str = 'revenue') -> List[Dict]:
        """Get top performing videos by specified metric"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        order_by = {
            'revenue': 'revenue DESC',
            'views': 'views DESC',
            'rpm': 'rpm DESC',
            'ctr': 'ctr DESC',
            'seo_score': 'seo_score DESC'
        }.get(metric, 'revenue DESC')
        
        cursor.execute(f'''
            SELECT 
                v.id,
                v.title,
                v.upload_date,
                v.views,
                v.revenue,
                v.rpm,
                v.ctr,
                v.seo_score,
                c.name as channel_name,
                c.style as channel_style
            FROM videos v
            JOIN channels c ON v.channel_id = c.id
            ORDER BY {order_by}
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'title': row[1],
                'upload_date': row[2],
                'views': row[3],
                'revenue': round(row[4], 2),
                'rpm': round(row[5], 2),
                'ctr': round(row[6], 1),
                'seo_score': row[7],
                'channel_name': row[8],
                'channel_style': row[9]
            })
        
        conn.close()
        return results
    
    def get_optimization_opportunities(self) -> Dict:
        """Identify optimization opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        opportunities = {}
        
        # Low-performing videos that could be optimized
        cursor.execute('''
            SELECT 
                v.id,
                v.title,
                v.views,
                v.revenue,
                v.rpm,
                v.seo_score,
                c.name as channel_name
            FROM videos v
            JOIN channels c ON v.channel_id = c.id
            WHERE v.seo_score < 60 OR v.rpm < 2.0
            ORDER BY v.upload_date DESC
            LIMIT 10
        ''')
        
        opportunities['low_seo_videos'] = []
        for row in cursor.fetchall():
            opportunities['low_seo_videos'].append({
                'id': row[0],
                'title': row[1],
                'views': row[2],
                'revenue': round(row[3], 2),
                'rpm': round(row[4], 2),
                'seo_score': row[5],
                'channel_name': row[6],
                'optimization_potential': self.calculate_optimization_potential(row[2], row[4], row[5])
            })
        
        # Channels with declining performance
        cursor.execute('''
            SELECT 
                c.id,
                c.name,
                c.style,
                AVG(da1.revenue) as recent_revenue,
                AVG(da2.revenue) as older_revenue
            FROM channels c
            JOIN daily_analytics da1 ON c.id = da1.channel_id 
            JOIN daily_analytics da2 ON c.id = da2.channel_id
            WHERE da1.date >= date('now', '-7 days') 
            AND da2.date >= date('now', '-21 days') 
            AND da2.date < date('now', '-14 days')
            GROUP BY c.id, c.name, c.style
            HAVING recent_revenue < older_revenue * 0.8
        ''')
        
        opportunities['declining_channels'] = []
        for row in cursor.fetchall():
            decline_percent = ((row[4] - row[3]) / row[4]) * 100
            opportunities['declining_channels'].append({
                'id': row[0],
                'name': row[1],
                'style': row[2],
                'recent_avg_revenue': round(row[3], 2),
                'older_avg_revenue': round(row[4], 2),
                'decline_percent': round(decline_percent, 1)
            })
        
        # Underutilized profitable styles
        cursor.execute('''
            SELECT 
                c.style,
                COUNT(*) as channel_count,
                AVG(c.average_rpm) as avg_rpm,
                SUM(da.revenue) as total_recent_revenue
            FROM channels c
            JOIN daily_analytics da ON c.id = da.channel_id
            WHERE da.date >= date('now', '-30 days')
            GROUP BY c.style
            ORDER BY avg_rpm DESC
        ''')
        
        opportunities['style_analysis'] = []
        for row in cursor.fetchall():
            opportunities['style_analysis'].append({
                'style': row[0],
                'channel_count': row[1],
                'average_rpm': round(row[2], 2),
                'total_recent_revenue': round(row[3], 2),
                'expansion_recommended': row[1] < 3 and row[2] > 2.5  # Less than 3 channels but high RPM
            })
        
        conn.close()
        return opportunities
    
    def calculate_optimization_potential(self, views: int, rpm: float, seo_score: int) -> Dict:
        """Calculate potential improvements from optimization"""
        
        # Estimate improvement potential
        seo_improvement_factor = 1.0
        if seo_score < 40:
            seo_improvement_factor = 1.5  # 50% improvement possible
        elif seo_score < 60:
            seo_improvement_factor = 1.3  # 30% improvement possible
        elif seo_score < 80:
            seo_improvement_factor = 1.15  # 15% improvement possible
        
        rpm_improvement_factor = 1.0
        if rpm < 1.5:
            rpm_improvement_factor = 1.4  # 40% RPM improvement possible
        elif rpm < 2.5:
            rpm_improvement_factor = 1.2  # 20% RPM improvement possible
        
        potential_views = int(views * seo_improvement_factor)
        potential_rpm = rpm * rpm_improvement_factor
        potential_revenue = (potential_views / 1000) * potential_rpm
        current_revenue = (views / 1000) * rpm
        
        return {
            'current_revenue': round(current_revenue, 2),
            'potential_revenue': round(potential_revenue, 2),
            'revenue_increase': round(potential_revenue - current_revenue, 2),
            'improvement_percent': round(((potential_revenue - current_revenue) / current_revenue) * 100, 1) if current_revenue > 0 else 0,
            'potential_views': potential_views,
            'potential_rpm': round(potential_rpm, 2)
        }
    
    def generate_profit_report(self) -> Dict:
        """Generate comprehensive profit analysis report"""
        
        empire_overview = self.get_empire_overview()
        channel_performance = self.get_channel_performance()
        revenue_projections = self.get_revenue_projections()
        top_videos = self.get_top_performing_videos()
        optimization_opportunities = self.get_optimization_opportunities()
        
        # Calculate additional insights
        total_optimization_potential = sum(
            opp.get('optimization_potential', {}).get('revenue_increase', 0) 
            for opp in optimization_opportunities.get('low_seo_videos', [])
        )
        
        report = {
            'empire_overview': empire_overview,
            'channel_performance': channel_performance,
            'revenue_projections': revenue_projections,
            'top_performing_videos': top_videos,
            'optimization_opportunities': optimization_opportunities,
            'key_insights': {
                'total_optimization_potential': round(total_optimization_potential, 2),
                'best_performing_style': max(channel_performance, key=lambda x: x['period_performance']['rpm'])['style'] if channel_performance else 'N/A',
                'fastest_growing_channel': max(channel_performance, key=lambda x: x['period_performance']['new_subscribers'])['name'] if channel_performance else 'N/A',
                'most_profitable_video': top_videos[0] if top_videos else None
            },
            'generated_at': datetime.now().isoformat()
        }
        
        return report


# Example usage
if __name__ == "__main__":
    print("💰 YouTube Profit Tracker - Demo")
    
    tracker = ProfitTracker()
    
    # Generate comprehensive report
    report = tracker.generate_profit_report()
    
    print("\n📊 EMPIRE OVERVIEW:")
    overview = report['empire_overview']
    print(f"Total Channels: {overview['total_channels']}")
    print(f"Total Revenue: ${overview['total_revenue']}")
    print(f"Monthly Revenue: ${overview['monthly_performance']['revenue']}")
    print(f"Monthly Growth: {overview['monthly_performance']['revenue_growth_percent']}%")
    
    print(f"\n📈 REVENUE PROJECTIONS:")
    projections = report['revenue_projections']
    print(f"Daily: ${projections['daily']}")
    print(f"Monthly: ${projections['monthly']}")
    print(f"Yearly: ${projections['yearly']}")
    
    if projections.get('monthly_goal'):
        goal = projections['monthly_goal']
        print(f"\nMonthly Goal Progress: {goal['revenue_progress_percent']}%")
        print(f"Target: ${goal['target_revenue']} | Actual: ${goal['actual_revenue']}")
    
    print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
    print(f"Total Optimization Potential: +${report['key_insights']['total_optimization_potential']}")
    print(f"Best Performing Style: {report['key_insights']['best_performing_style']}")
    print(f"Videos Needing SEO: {len(report['optimization_opportunities']['low_seo_videos'])}")
    
    # Save detailed report
    with open('profit_analysis_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Detailed report saved to: profit_analysis_report.json")