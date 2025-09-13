import time
from typing import Dict, Any, Optional
import platform
import sys
from pathlib import Path

class PerformanceTracker:
    """Tracks performance metrics for various operations"""

    def __init__(self):
        self.timers: Dict[str, float] = {}
        self.metrics: Dict[str, Any] = {}
        self.warnings: list = []

    def start_timer(self, operation: str) -> None:
        """Start timing an operation"""
        self.timers[operation] = time.time()
        print(f"⏱️  Pradėta: {operation}")

    def stop_timer(self, operation: str) -> float:
        """Stop timing an operation and return elapsed time"""
        if operation not in self.timers:
            print(f"⚠️  Laikmatis '{operation}' nebuvo pradėtas")
            return 0.0

        elapsed = time.time() - self.timers[operation]
        self.metrics[f"{operation}_time"] = elapsed
        print(".1f")
        return elapsed

    def add_metric(self, key: str, value: Any) -> None:
        """Add a custom metric"""
        self.metrics[key] = value

    def add_warning(self, warning: str) -> None:
        """Add a warning message"""
        self.warnings.append(warning)
        print(f"⚠️  ĮSPĖJIMAS: {warning}")

    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get detailed file information"""
        try:
            path = Path(file_path)
            if not path.exists():
                return None

            stat = path.stat()
            file_info = {
                'path': str(path),
                'size_bytes': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'modified': stat.st_mtime
            }

            # Try to get image dimensions if it's an image
            if path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                try:
                    from PIL import Image
                    with Image.open(path) as img:
                        file_info['width'] = img.width
                        file_info['height'] = img.height
                        file_info['resolution'] = f"{img.width}x{img.height}"
                except ImportError:
                    self.add_warning("PIL biblioteka neprieinama paveikslėlių analizei")
                except Exception as e:
                    self.add_warning(f"Nepavyko gauti paveikslėlio dimensijų: {e}")

            return file_info

        except Exception as e:
            self.add_warning(f"Nepavyko gauti failo informacijos {file_path}: {e}")
            return None

    def generate_report(self) -> str:
        """Generate comprehensive performance report"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("📊 TECHNINĖ ATASKAITA - PHASE 1C")
        report_lines.append("=" * 60)

        # System Information
        report_lines.append("\n🖥️  SISTEMOS INFORMACIJA:")
        report_lines.append(f"   Python versija: {sys.version.split()[0]}")
        report_lines.append(f"   OS: {platform.system()} {platform.release()}")
        report_lines.append(f"   Architektūra: {platform.machine()}")

        # Performance Metrics
        report_lines.append("\n⏱️  VYKDYMO LAIKAI:")
        time_metrics = {k: v for k, v in self.metrics.items() if k.endswith('_time')}
        for metric, value in sorted(time_metrics.items()):
            operation = metric.replace('_time', '').replace('_', ' ').title()
            report_lines.append("6.1f")

        # File Information
        report_lines.append("\n📁 FAILŲ INFORMACIJA:")
        file_metrics = {k: v for k, v in self.metrics.items() if not k.endswith('_time') and isinstance(v, dict)}
        for metric_name, file_info in file_metrics.items():
            if file_info:
                report_lines.append(f"   {metric_name.upper()}:")
                report_lines.append(f"     Kelias: {file_info.get('path', 'N/A')}")
                report_lines.append(".1f")
                if 'resolution' in file_info:
                    report_lines.append(f"     Rezoliucija: {file_info['resolution']}")

        # Warnings
        if self.warnings:
            report_lines.append("\n⚠️  ĮSPĖJIMAI:")
            for warning in self.warnings:
                report_lines.append(f"   • {warning}")

        # Summary
        total_time = sum(v for k, v in time_metrics.items())
        report_lines.append("\n📈 SANTRAUKA:")
        report_lines.append(".1f")
        report_lines.append(f"   Iš viso failų: {len(file_metrics)}")
        report_lines.append(f"   Įspėjimų: {len(self.warnings)}")

        report_lines.append("=" * 60)

        return "\n".join(report_lines)

    def save_report(self, output_dir: str, filename: str = "performance_report.txt") -> None:
        """Save performance report to file"""
        try:
            report_path = Path(output_dir) / filename
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(self.generate_report())
            print(f"💾 Ataskaita išsaugota: {report_path}")
        except Exception as e:
            print(f"❌ Nepavyko išsaugoti ataskaitos: {e}")
