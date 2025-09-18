import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin, urlparse
from bangla_stopwords import remove_stopwords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk
from datetime import datetime
import os

class NewsScraperSummarizer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_prothomalo(self, url):
        """Scrape Prothom Alo news article"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_element = soup.find('h1') or soup.find('title')
            title = title_element.get_text().strip() if title_element else "Title not found"
            
            # Extract article content
            content_selectors = [
                '.story-element-text',
                '.story-content',
                '.article-content',
                'article p',
                '.content p',
                'p'
            ]
            
            content = ""
            for selector in content_selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    content = " ".join([p.get_text().strip() for p in paragraphs[:10]])
                    if len(content) > 100:
                        break
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'Prothom Alo'
            }
        except Exception as e:
            print(f"Error scraping Prothom Alo: {e}")
            return None
    
    def scrape_daily_star(self, url):
        """Scrape Daily Star news article"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_element = soup.find('h1') or soup.find('title')
            title = title_element.get_text().strip() if title_element else "Title not found"
            
            # Extract article content
            content_selectors = [
                '.article-content p',
                '.story-content p',
                '.content-body p',
                'article p',
                'p'
            ]
            
            content = ""
            for selector in content_selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    content = " ".join([p.get_text().strip() for p in paragraphs[:10]])
                    if len(content) > 100:
                        break
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'Daily Star'
            }
        except Exception as e:
            print(f"Error scraping Daily Star: {e}")
            return None
    
    def scrape_generic_news(self, url):
        """Generic scraper for any news website"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_selectors = ['h1', '.title', '.headline', 'title']
            title = "Title not found"
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element:
                    title = title_element.get_text().strip()
                    break
            
            # Extract article content
            content_selectors = [
                'article p',
                '.article-content p',
                '.story-content p',
                '.content p',
                '.post-content p',
                '.entry-content p',
                '.news-content p',
                'p'
            ]
            
            content = ""
            for selector in content_selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    text_paragraphs = []
                    for p in paragraphs[:15]:
                        text = p.get_text().strip()
                        # Skip navigation, ads, and read more elements
                        if (len(text) > 30 and 
                            'আরও পড়ুন' not in text and
                            'পড়ুন' not in text[-10:] and
                            'বিস্তারিত' not in text and
                            'সম্পূর্ণ খবর' not in text and
                            not re.search(r'\d{1,2}:\d{2}', text) and  # Skip timestamps
                            'হোম' not in text[:10] and
                            'প্রচ্ছদ' not in text[:10]):
                            text_paragraphs.append(text)
                    
                    content = " ".join(text_paragraphs)
                    if len(content) > 200:
                        break
            
            # Clean content
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Detect source from URL
            domain = urlparse(url).netloc
            source = domain.replace('www.', '').replace('.com', '').replace('.bd', '').title()
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'source': source
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def scrape_news_article(self, url):
        """Main scraping function that determines which scraper to use"""
        domain = urlparse(url).netloc.lower()
        
        if 'prothomalo' in domain:
            return self.scrape_prothomalo(url)
        elif 'thedailystar' in domain:
            return self.scrape_daily_star(url)
        else:
            return self.scrape_generic_news(url)
    
    def clean_bangla_text(self, text):
        """Clean Bangla text and remove unwanted elements"""
        if not text:
            return ""
        
        # Remove "আরও পড়ুন" and similar read more patterns
        text = re.sub(r'আরও পড়ুন.*?(?=\s|$)', '', text)
        text = re.sub(r'পড়ুন.*?(?=\s|$)', '', text) 
        text = re.sub(r'বিস্তারিত.*?(?=\s|$)', '', text)
        text = re.sub(r'সম্পূর্ণ খবর.*?(?=\s|$)', '', text)
        
        # Remove dates and timestamps
        text = re.sub(r'\d{1,2}\s+(?:জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর)\s+\d{4}', '', text)
        text = re.sub(r'\d{1,2}:\d{2}', '', text)
        
        # Remove navigation elements
        text = re.sub(r'হোম\s*বাংলাদেশ\s*', '', text)
        text = re.sub(r'প্রচ্ছদ\s*', '', text)
        text = re.sub(r'সর্বশেষ\s*', '', text)
        
        # Remove extra whitespace and normalize punctuation
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\.+', '।', text)  # Replace multiple dots with Bangla full stop
        
        # Ensure proper sentence ending
        if not text.endswith('।') and not text.endswith('.'):
            text += '।'
        
        return text.strip()
    
    def summarize_text(self, text, sentences=2):
        """Generate high-quality summary with proper formatting"""
        if not text or len(text) < 100:
            return "পর্যাপ্ত তথ্য পাওয়া যায়নি।"
        
        try:
            # Clean text first
            cleaned_text = self.clean_bangla_text(text)
            
            # Split into sentences using Bangla sentence separators
            sentences_list = re.split(r'[।\.!?]+', cleaned_text)
            sentences_list = [s.strip() for s in sentences_list if s.strip() and len(s.strip()) > 20]
            
            if len(sentences_list) < 2:
                return cleaned_text[:150] + "..."
            
            # Get important sentences (first few and longest ones)
            important_sentences = []
            
            # Always include first sentence (usually contains key info)
            if sentences_list[0]:
                important_sentences.append(sentences_list[0])
            
            # Add 1-2 more informative sentences
            remaining_sentences = sentences_list[1:6]  # Look at next 5 sentences
            remaining_sentences.sort(key=len, reverse=True)  # Sort by length (longer = more info)
            
            for sentence in remaining_sentences:
                if len(important_sentences) >= sentences:
                    break
                # Avoid repetitive sentences
                if not any(self.sentence_similarity(sentence, existing) for existing in important_sentences):
                    important_sentences.append(sentence)
            
            # Join sentences properly
            summary = ''
            for i, sentence in enumerate(important_sentences):
                sentence = sentence.strip()
                if sentence:
                    # Ensure proper capitalization (if mixed script)
                    if i > 0:
                        summary += ' '
                    summary += sentence
                    if not sentence.endswith('।') and not sentence.endswith('.'):
                        summary += '।'
            
            # Final cleanup
            summary = re.sub(r'\s+', ' ', summary)
            summary = re.sub(r'।+', '।', summary)
            
            # Limit length to ensure it's actually a summary
            max_length = min(len(text) // 3, 400)  # Summary should be max 1/3 of original
            if len(summary) > max_length:
                # Cut at sentence boundary
                sentences_in_summary = summary.split('।')
                truncated = ''
                for sentence in sentences_in_summary:
                    if len(truncated + sentence + '।') <= max_length:
                        truncated += sentence + '।'
                    else:
                        break
                summary = truncated
            
            return summary.strip() if summary.strip() else "সংক্ষিপ্ত বিবরণ তৈরি করা সম্ভব হয়নি।"
            
        except Exception as e:
            print(f"Error in summarization: {e}")
            # Fallback: return first 2 sentences
            sentences_list = text.split('।')
            if len(sentences_list) >= 2:
                fallback = sentences_list[0] + '।' + sentences_list[1] + '।'
                return self.clean_bangla_text(fallback)
            else:
                return text[:200] + "..."
    
    def sentence_similarity(self, sent1, sent2):
        """Check if two sentences are similar (simple word overlap check)"""
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())
        if not words1 or not words2:
            return False
        overlap = len(words1.intersection(words2))
        return overlap / min(len(words1), len(words2)) > 0.6
    
    def process_news_urls(self, urls):
        """Process multiple news URLs and generate summaries"""
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"Processing {i}/{len(urls)}: {url}")
            
            # Scrape article
            article_data = self.scrape_news_article(url)
            
            if article_data and article_data['content']:
                # Generate summary
                summary = self.summarize_text(article_data['content'])
                
                results.append({
                    'Title': article_data['title'],
                    'URL': article_data['url'],
                    'Source': article_data['source'],
                    'Summary': summary,
                    'Original_Length': len(article_data['content']),
                    'Summary_Length': len(summary),
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                print(f" Successfully processed: {article_data['title'][:50]}...")
            else:
                print(f" Failed to process: {url}")
        
        return results
    
    def save_to_csv(self, results, filename='summaries.csv'):
        """Save results to CSV file with error handling"""
        if not results:
            print("No results to save!")
            return
        
        # Try different filename if file is locked
        import os
        from datetime import datetime
        
        original_filename = filename
        counter = 1
        
        while True:
            try:
                df = pd.DataFrame(results)
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f" Results saved to {filename}")
                print(f" Total articles processed: {len(results)}")
                return df
            except PermissionError:
                if counter == 1:
                    print(f"  {original_filename} is open in another program. Trying alternative filename...")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"summaries_{timestamp}.csv"
                counter += 1
                if counter > 3:
                    print(f" Cannot save CSV file. Please close any open CSV files and try again.")
                    return None
            except Exception as e:
                print(f" Error saving CSV: {e}")
                return None

# Example usage and testing
if __name__ == "__main__":
    scraper = NewsScraperSummarizer()
    
    # Pre-defined Bangla news URLs (reduced to working ones)
    bangla_news_urls = [
        "https://www.prothomalo.com/bangladesh/nyv4t76ydg",
        #"https://www.thedailystar.net/news/bangladesh/news/dhaka-air-quality-ranks-4th-worst-world-3471856",
        "https://bangla.thedailystar.net/international/news-700181"
    ]
    
    print(" Starting News Scraper and Summarizer...")
    print(f" Processing {len(bangla_news_urls)} Bangla news articles...")
    
    # Process all URLs
    results = scraper.process_news_urls(bangla_news_urls)
    
    if results:
        print(f"\n Summary Report:")
        print(f" Successfully processed: {len(results)} articles")
        
        # Show first few results before saving
        print("\n Sample Results:")
        for i, result in enumerate(results[:2], 1):
            print(f"\n{i}. {result['Title'][:60]}...")
            print(f"   Source: {result['Source']}")
            print(f"   Original Length: {result['Original_Length']} characters")
            print(f"   Summary Length: {result['Summary_Length']} characters")
            print(f"   Compression: {100 - (result['Summary_Length']/result['Original_Length']*100):.1f}%")
            print(f"   Summary: {result['Summary'][:150]}...")
        
        # Save to CSV with error handling
        df = scraper.save_to_csv(results)
        
        if df is not None:
            print(f"\n File saved successfully!")
            print(f" Check your folder for the CSV file.")
    else:
        print(" No articles could be processed. Check your internet connection.")