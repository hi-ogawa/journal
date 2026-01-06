# OBS Knowledge Base - Initial Estimation

**Date**: 2026-01-06
**Source**: https://obsproject.com/kb

## Site Structure

### Categories (10 total)

| ID | Category Name           | Articles (Page 1) | Pagination |
|----|-------------------------|-------------------|------------|
| 0  | F.A.Q.s                 | 10                | Yes        |
| 1  | Getting Started         | 8                 | Yes        |
| 2  | Troubleshooting Guides  | 9                 | Yes        |
| 3  | OBS Studio              | 12                | Yes        |
| 4  | Streaming               | ?                 | ?          |
| 5  | Recording               | ?                 | ?          |
| 6  | Sources & Filters       | 13                | Yes        |
| 7  | Audio                   | ?                 | ?          |
| 8  | Scripting & Development | 3                 | Yes        |
| 9  | Post-Production         | ?                 | ?          |

**Checked categories (6/10)**: 55 articles on first pages
**Unchecked categories (4/10)**: Estimated ~10 articles each = ~40 articles

## URL Patterns

### Category Pages
- Pattern: `https://obsproject.com/kb/category/{ID}`
- Pagination: `https://obsproject.com/kb/category/{ID}?page={N}`
- Articles per page: ~8-13

### Article Pages
- Pattern: `https://obsproject.com/kb/{article-slug}`
- Example: `https://obsproject.com/kb/quick-start-guide`

## HTML Structure

### Category Pages
```html
<li>
  <a href="https://obsproject.com/kb/{article-slug}">{Article Title}</a>
  <p>{Article description}</p>
</li>
```

### Article Pages
- Title: `<h1>` or similar
- Content: Semantic HTML (h2, h3, p, img, etc.)
- Metadata: Date shown (e.g., "2021-08-25")
- Table of contents for longer articles
- Images with lightbox functionality

## Sample Article Analysis

**Article**: Quick Start Guide
- **URL**: https://obsproject.com/kb/quick-start-guide
- **Word count**: ~450-500 words
- **Images**: 5 screenshots
- **Structure**: Clear headings, step-by-step tutorial
- **Special elements**: TOC, linked cards, image gallery

## Rough Estimation

### Conservative Estimate
- **Total categories**: 10
- **Avg articles per category**: 10-15
- **Estimated total articles**: 100-150 articles

### Size Projection
- **Avg words per article**: 400-600 words
- **Total words estimate**: 40,000-90,000 words
- **Compared to Ableton**: 228,954 words
- **Expected size**: 0.3-0.6 MB (smaller than Ableton)

## Next Steps

1. Create comprehensive scraper to:
   - Iterate all 10 categories
   - Follow pagination to get all articles
   - Count exact total
2. Download all article HTML
3. Convert to single markdown file
4. Compare actual vs. estimated size

## Notes

- Many categories have pagination (multiple pages)
- Need to handle rate limiting (respectful scraping)
- Articles include rich media (images, code blocks)
- Consider stripping images or converting to alt text for LLM context
