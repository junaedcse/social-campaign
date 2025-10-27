#!/usr/bin/env python3
"""
Project Structure Analyzer
Generates a visual tree of the project structure with statistics and analysis.
"""

import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import json


class ProjectAnalyzer:
    """Analyzes and displays project structure."""
    
    IGNORE_DIRS = {
        '__pycache__', '.git', 'venv', 'venvsma', '.venv', 
        'node_modules', '.pytest_cache', '.mypy_cache', 'htmlcov',
        '.DS_Store', '.idea', '.vscode'
    }
    
    IGNORE_FILES = {
        '.DS_Store', '.pyc', '.pyo', '.pyd', '.so', '.dll',
        '.dylib', '.coverage', 'desktop.ini', 'Thumbs.db'
    }
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.stats = defaultdict(int)
        self.file_types = defaultdict(list)
        self.large_files = []
        self.issues = []
        
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        if path.name in self.IGNORE_DIRS or path.name in self.IGNORE_FILES:
            return True
        if path.suffix in self.IGNORE_FILES:
            return True
        return False
    
    def count_lines(self, file_path: Path) -> int:
        """Count lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file."""
        stats = {
            'name': file_path.name,
            'path': str(file_path.relative_to(self.root_path)),
            'size': file_path.stat().st_size,
            'extension': file_path.suffix,
        }
        
        # Count lines for text files
        if file_path.suffix in ['.py', '.md', '.txt', '.json', '.yaml', '.yml']:
            stats['lines'] = self.count_lines(file_path)
            
            # Track large Python files
            if file_path.suffix == '.py' and stats['lines'] > 300:
                self.large_files.append((file_path, stats['lines']))
        
        return stats
    
    def scan_directory(self, path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """Recursively scan directory and build tree."""
        lines = []
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return lines
        
        for i, item in enumerate(items):
            if self.should_ignore(item):
                continue
            
            is_last_item = i == len(items) - 1
            connector = "└── " if is_last_item else "├── "
            
            if item.is_dir():
                self.stats['directories'] += 1
                lines.append(f"{prefix}{connector}📁 {item.name}/")
                
                # Recursively scan subdirectory
                extension = "    " if is_last_item else "│   "
                sublines = self.scan_directory(item, prefix + extension, is_last_item)
                lines.extend(sublines)
            else:
                if self.should_ignore(item):
                    continue
                    
                self.stats['files'] += 1
                file_info = self.analyze_file(item)
                self.file_types[item.suffix].append(file_info)
                
                # Format file display
                icon = self._get_file_icon(item.suffix)
                extra_info = ""
                
                if 'lines' in file_info:
                    extra_info = f" [{file_info['lines']:,} lines]"
                    self.stats['total_lines'] += file_info['lines']
                    
                    # Flag large files
                    if file_info['lines'] > 300:
                        extra_info += " ⚠️"
                
                lines.append(f"{prefix}{connector}{icon} {item.name}{extra_info}")
        
        return lines
    
    def _get_file_icon(self, extension: str) -> str:
        """Get emoji icon for file type."""
        icon_map = {
            '.py': '🐍',
            '.md': '📝',
            '.txt': '📄',
            '.json': '⚙️',
            '.yaml': '⚙️',
            '.yml': '⚙️',
            '.sh': '🔧',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.log': '📋',
        }
        return icon_map.get(extension, '📄')
    
    def detect_issues(self):
        """Detect common project structure issues."""
        root_files = list(self.root_path.glob('*'))
        
        # Check for too many root files
        root_file_count = sum(1 for f in root_files if f.is_file())
        if root_file_count > 15:
            self.issues.append(
                f"🔴 Too many files in root directory: {root_file_count} files (should be < 15)"
            )
        
        # Check for test files in wrong location
        test_files_in_root = [f for f in root_files if f.name.startswith('test_') and f.suffix == '.py']
        if test_files_in_root:
            self.issues.append(
                f"🔴 {len(test_files_in_root)} test files in root (should be in tests/)"
            )
        
        # Check for debug/demo files
        debug_files = [f for f in root_files if any(
            f.name.startswith(prefix) for prefix in ['debug_', 'demo_', 'fix_']
        )]
        if debug_files:
            self.issues.append(
                f"🟡 {len(debug_files)} debug/demo files in root (consider moving to scripts/)"
            )
        
        # Check for large Python files
        if self.large_files:
            self.issues.append(
                f"🟡 {len(self.large_files)} large Python files (>300 lines)"
            )
        
        # Check for multiple pipeline files
        pipeline_files = list(self.root_path.glob('src/services/pipeline*.py'))
        if len(pipeline_files) > 1:
            self.issues.append(
                f"🔴 Multiple pipeline files found: {len(pipeline_files)} (should consolidate to 1)"
            )
        
        # Check for documentation organization
        md_files_in_root = [f for f in root_files if f.suffix == '.md' and f.name != 'README.md']
        if len(md_files_in_root) > 5:
            self.issues.append(
                f"🟡 {len(md_files_in_root)} documentation files in root (consider docs/ directory)"
            )
    
    def print_structure(self):
        """Print the complete project structure."""
        print("=" * 80)
        print(f"PROJECT STRUCTURE: {self.root_path.name}")
        print("=" * 80)
        print()
        print(f"📁 {self.root_path.name}/")
        
        tree_lines = self.scan_directory(self.root_path)
        for line in tree_lines:
            print(line)
        
        print()
        self.print_statistics()
        self.detect_issues()
        self.print_issues()
        self.print_file_analysis()
    
    def print_statistics(self):
        """Print project statistics."""
        print("=" * 80)
        print("STATISTICS")
        print("=" * 80)
        print()
        print(f"📊 Total Directories:  {self.stats['directories']:,}")
        print(f"📊 Total Files:        {self.stats['files']:,}")
        print(f"📊 Total Lines:        {self.stats['total_lines']:,}")
        print()
        
        # File type breakdown
        print("File Types:")
        sorted_types = sorted(
            self.file_types.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )
        for ext, files in sorted_types[:10]:  # Top 10
            count = len(files)
            total_lines = sum(f.get('lines', 0) for f in files)
            if total_lines > 0:
                print(f"  {ext or 'no extension':10s} {count:3d} files  {total_lines:6,} lines")
            else:
                print(f"  {ext or 'no extension':10s} {count:3d} files")
        print()
    
    def print_issues(self):
        """Print detected issues."""
        if not self.issues:
            print("✅ No major issues detected!")
            print()
            return
        
        print("=" * 80)
        print("DETECTED ISSUES")
        print("=" * 80)
        print()
        for issue in self.issues:
            print(f"  {issue}")
        print()
    
    def print_file_analysis(self):
        """Print analysis of specific file types."""
        # Python files analysis
        py_files = self.file_types.get('.py', [])
        if py_files:
            print("=" * 80)
            print("PYTHON FILES ANALYSIS")
            print("=" * 80)
            print()
            
            total_py_lines = sum(f['lines'] for f in py_files if 'lines' in f)
            avg_lines = total_py_lines / len(py_files) if py_files else 0
            
            print(f"📊 Total Python files: {len(py_files)}")
            print(f"📊 Total lines of code: {total_py_lines:,}")
            print(f"📊 Average file size: {avg_lines:.0f} lines")
            print()
            
            # Top 10 largest files
            if self.large_files:
                print("Largest Python files:")
                for file_path, lines in sorted(self.large_files, key=lambda x: x[1], reverse=True)[:10]:
                    rel_path = file_path.relative_to(self.root_path)
                    warning = " ⚠️ TOO LARGE" if lines > 500 else ""
                    print(f"  {str(rel_path):50s} {lines:5,} lines{warning}")
                print()
        
        # Documentation analysis
        md_files = self.file_types.get('.md', [])
        if md_files:
            print("=" * 80)
            print("DOCUMENTATION ANALYSIS")
            print("=" * 80)
            print()
            print(f"📚 Total documentation files: {len(md_files)}")
            
            # Check where they are located
            root_md = sum(1 for f in md_files if '/' not in f['path'])
            if root_md > 5:
                print(f"⚠️  {root_md} documentation files in root directory")
                print("   Consider organizing in docs/ subdirectory")
            print()
    
    def export_json(self, output_file: str = "project_structure.json"):
        """Export structure to JSON file."""
        data = {
            'root': str(self.root_path),
            'statistics': dict(self.stats),
            'file_types': {k: len(v) for k, v in self.file_types.items()},
            'large_files': [
                {'path': str(f.relative_to(self.root_path)), 'lines': lines}
                for f, lines in self.large_files
            ],
            'issues': self.issues
        }
        
        output_path = self.root_path / output_file
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📄 Structure exported to: {output_file}")
        print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze and display project structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python print_structure.py                    # Analyze current directory
  python print_structure.py /path/to/project   # Analyze specific directory
  python print_structure.py --export           # Export to JSON
        """
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to project directory (default: current directory)'
    )
    parser.add_argument(
        '--export',
        action='store_true',
        help='Export structure to JSON file'
    )
    parser.add_argument(
        '--json-output',
        default='project_structure.json',
        help='JSON output filename (default: project_structure.json)'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = ProjectAnalyzer(args.path)
    
    # Print structure
    analyzer.print_structure()
    
    # Export if requested
    if args.export:
        analyzer.export_json(args.json_output)
    
    # Print recommendations
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("To improve project structure:")
    print("  1. Run ./cleanup_phase1.sh to reorganize files")
    print("  2. Read CODE_REVIEW_REPORT.md for detailed analysis")
    print("  3. Consolidate pipeline files (see report Section 3)")
    print("  4. Split large files into smaller modules")
    print()


if __name__ == "__main__":
    main()