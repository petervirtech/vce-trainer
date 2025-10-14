"""
Improved VCE decoder that actually attempts to parse real VCE file content.
"""

import struct
import zlib
import re
from typing import List, Tuple, Optional
from pathlib import Path


def decode_vce_file_properly(file_path: str) -> Tuple[str, List[str], bool]:
    """
    Attempt to properly decode a VCE file and extract real questions.
    Returns: (title, questions_text_list, success)
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        print(f"Analyzing VCE file: {Path(file_path).name}")
        print(f"File size: {len(data)} bytes")
        
        # Try multiple decoding approaches
        decoded_text = None
        method_used = None
        
        # Method 1: Look for readable strings directly
        strings = extract_readable_strings(data)
        if strings:
            decoded_text = '\n'.join(strings)
            method_used = "String extraction"
        
        # Method 2: Try common VCE decryption methods
        if not decoded_text or len(decoded_text) < 1000:
            for method, result in try_vce_decryption_methods(data):
                if result and len(result) > len(decoded_text or ""):
                    decoded_text = result
                    method_used = method
        
        # Method 3: Try to find XML or structured content
        if not decoded_text or len(decoded_text) < 1000:
            xml_content = extract_xml_content(data)
            if xml_content:
                decoded_text = xml_content
                method_used = "XML extraction"
        
        if decoded_text and len(decoded_text) > 500:
            print(f"✅ Successfully decoded using: {method_used}")
            print(f"Decoded content length: {len(decoded_text)} characters")
            
            # Extract title from filename or content
            title = extract_title_from_content(decoded_text, file_path)
            
            # Extract questions
            questions = extract_questions_from_decoded_text(decoded_text)
            
            if questions:
                print(f"✅ Extracted {len(questions)} questions from VCE file")
                return title, questions, True
            else:
                print("❌ No questions found in decoded content")
        else:
            print("❌ Failed to decode VCE file content")
        
        return "", [], False
        
    except Exception as e:
        print(f"❌ Error decoding VCE file: {e}")
        return "", [], False


def extract_readable_strings(data: bytes, min_length: int = 20) -> List[str]:
    """Extract readable ASCII strings from binary data."""
    strings = []
    current_string = ""
    
    for byte_val in data:
        if 32 <= byte_val <= 126:  # Printable ASCII
            current_string += chr(byte_val)
        else:
            if len(current_string) >= min_length:
                # Clean up the string
                cleaned = current_string.strip()
                if cleaned and is_likely_question_content(cleaned):
                    strings.append(cleaned)
            current_string = ""
    
    # Don't forget the last string
    if len(current_string) >= min_length:
        cleaned = current_string.strip()
        if cleaned and is_likely_question_content(cleaned):
            strings.append(cleaned)
    
    return strings


def is_likely_question_content(text: str) -> bool:
    """Check if text looks like it could be question content."""
    text_lower = text.lower()
    
    # Skip if it's mostly non-alphabetic
    alpha_chars = sum(1 for c in text if c.isalpha())
    if alpha_chars < len(text) * 0.3:
        return False
    
    # Look for question indicators
    question_indicators = [
        'what', 'which', 'how', 'why', 'when', 'where', 'who',
        'should', 'would', 'could', 'can', 'may', 'must',
        'azure', 'microsoft', 'windows', 'server', 'network',
        'configure', 'implement', 'deploy', 'manage', 'create'
    ]
    
    # Look for answer indicators
    answer_indicators = ['a.', 'b.', 'c.', 'd.', 'correct', 'answer']
    
    has_question_words = any(word in text_lower for word in question_indicators)
    has_answer_words = any(word in text_lower for word in answer_indicators)
    
    return has_question_words or has_answer_words or len(text) > 50


def try_vce_decryption_methods(data: bytes) -> List[Tuple[str, str]]:
    """Try various decryption methods commonly used in VCE files."""
    methods = []
    
    # Method 1: XOR with common keys
    common_xor_keys = [0x85, 0xA8, 0x06, 0x02, 0xFF, 0x00, 0x5A, 0xA5, 0xAA, 0x55]
    for key in common_xor_keys:
        try:
            decrypted = bytes(b ^ key for b in data)
            text = decrypted.decode('utf-8', errors='ignore')
            if len(text) > 1000 and calculate_readability_score(text) > 0.3:
                methods.append((f"XOR key 0x{key:02X}", text))
        except:
            continue
    
    # Method 2: Try zlib decompression
    try:
        decompressed = zlib.decompress(data)
        text = decompressed.decode('utf-8', errors='ignore')
        if len(text) > 1000 and calculate_readability_score(text) > 0.3:
            methods.append(("Zlib decompression", text))
    except:
        pass
    
    # Method 3: Combined XOR + zlib
    for key in common_xor_keys[:5]:  # Try top keys
        try:
            xor_data = bytes(b ^ key for b in data)
            decompressed = zlib.decompress(xor_data)
            text = decompressed.decode('utf-8', errors='ignore')
            if len(text) > 1000 and calculate_readability_score(text) > 0.3:
                methods.append((f"XOR 0x{key:02X} + Zlib", text))
        except:
            continue
    
    # Method 4: Try different encodings
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            text = data.decode(encoding, errors='ignore')
            if len(text) > 1000 and calculate_readability_score(text) > 0.3:
                methods.append((f"Direct {encoding}", text))
        except:
            continue
    
    return methods


def extract_xml_content(data: bytes) -> Optional[str]:
    """Try to extract XML content from VCE file."""
    try:
        # Look for XML patterns
        text = data.decode('utf-8', errors='ignore')
        
        # Find XML-like structures
        xml_patterns = [
            r'<\?xml.*?\?>.*?</.*?>',
            r'<question.*?</question>',
            r'<exam.*?</exam>',
            r'<vce.*?</vce>'
        ]
        
        for pattern in xml_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                return '\n'.join(matches)
        
        return None
    except:
        return None


def calculate_readability_score(text: str) -> float:
    """Calculate how readable the text appears to be."""
    if not text or len(text) < 50:
        return 0.0
    
    # Count character types
    total_chars = len(text)
    printable = sum(1 for c in text if c.isprintable())
    alpha = sum(1 for c in text if c.isalpha())
    
    # Basic readability score
    printable_ratio = printable / total_chars
    alpha_ratio = alpha / total_chars
    
    # Look for exam-related keywords
    exam_keywords = [
        'question', 'answer', 'correct', 'azure', 'microsoft', 'which', 'what',
        'configure', 'implement', 'deploy', 'manage', 'create', 'should', 'would'
    ]
    
    text_lower = text.lower()
    keyword_count = sum(1 for keyword in exam_keywords if keyword in text_lower)
    keyword_bonus = min(keyword_count * 0.1, 0.5)
    
    return min(printable_ratio * 0.5 + alpha_ratio * 0.3 + keyword_bonus, 1.0)


def extract_title_from_content(content: str, file_path: str) -> str:
    """Extract exam title from content or filename."""
    # Try to find title in content
    title_patterns = [
        r'title[:\s]+([^\n\r]+)',
        r'exam[:\s]+([^\n\r]+)',
        r'<title>([^<]+)</title>'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            if len(title) > 10 and len(title) < 200:
                return title
    
    # Fall back to filename
    filename = Path(file_path).stem
    # Clean up filename
    title = filename.replace('.', ' ').replace('-', ' ').replace('_', ' ')
    return title


def extract_questions_from_decoded_text(text: str) -> List[str]:
    """Extract individual questions from decoded text."""
    questions = []
    
    # Method 1: Look for numbered questions
    question_patterns = [
        r'(?:Question\s+\d+[:\.]?\s*)(.*?)(?=Question\s+\d+|$)',
        r'(?:^\d+[\.\)]\s*)(.*?)(?=^\d+[\.\)]|$)',
        r'(?:Q\d+[:\.]?\s*)(.*?)(?=Q\d+|$)'
    ]
    
    for pattern in question_patterns:
        matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if matches and len(matches) > 5:  # Found a good pattern
            questions.extend([match.strip() for match in matches if len(match.strip()) > 50])
            break
    
    # Method 2: Split by common delimiters if no numbered questions found
    if not questions:
        # Try splitting by double newlines or other patterns
        potential_questions = re.split(r'\n\s*\n|\r\n\s*\r\n', text)
        for q in potential_questions:
            q = q.strip()
            if len(q) > 100 and is_likely_question_content(q):
                questions.append(q)
    
    # Clean up questions
    cleaned_questions = []
    for q in questions[:100]:  # Limit to reasonable number
        q = q.strip()
        if len(q) > 50 and len(q) < 5000:  # Reasonable question length
            cleaned_questions.append(q)
    
    return cleaned_questions


if __name__ == "__main__":
    # Test the decoder
    import sys
    if len(sys.argv) > 1:
        vce_file = sys.argv[1]
        title, questions, success = decode_vce_file_properly(vce_file)
        
        if success:
            print(f"\n✅ Successfully decoded: {title}")
            print(f"Found {len(questions)} questions")
            
            # Show first few questions
            for i, q in enumerate(questions[:3]):
                print(f"\nQuestion {i+1}:")
                print(q[:200] + "..." if len(q) > 200 else q)
        else:
            print("\n❌ Failed to decode VCE file")
    else:
        print("Usage: python vce_decoder_fix.py <vce_file_path>")