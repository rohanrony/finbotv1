import re
from typing import List, Dict

class SectionParser:
    """Parses raw text into structured sections based on SEC 'ITEM' markers."""
    
    # Common SEC Item patterns (e.g., ITEM 1. BUSINESS)
    ITEM_PATTERN = re.compile(r'(?i)^ITEM\s+([0-9A-Z]+)[\.:]?\s*(.*)$', re.MULTILINE)

    def parse(self, text: str) -> List[Dict]:
        """
        Parse text into sections using regex for Item headers.
        Returns a list of dicts with 'heading', 'subheading', and 'text'.
        """
        sections = []
        matches = list(self.ITEM_PATTERN.finditer(text))
        
        if not matches:
            # Fallback if no items found: treat whole doc as one section
            return [{"heading": "Full Document", "subheading": None, "text": text.strip()}]
            
        for i, match in enumerate(matches):
            item_num = match.group(1)
            item_title = match.group(2).strip()
            
            start_idx = match.end()
            end_idx = matches[i+1].start() if i + 1 < len(matches) else len(text)
            
            section_text = text[start_idx:end_idx].strip()
            
            sections.append({
                "heading": f"Item {item_num}",
                "subheading": item_title or None,
                "text": section_text
            })
            
        return sections
