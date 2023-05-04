import os
import random
import re
import sys
from collections import defaultdict

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = {}

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = {link for link in pages[filename] if link in pages}

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    next_pages = {}
    link_pages = len(corpus[page])
    all_pages_cnt = len(corpus.keys())
    for p in corpus.keys():
        if p in corpus[page]:
            next_pages[p] = damping_factor / link_pages + (1 - damping_factor) / all_pages_cnt
        else:
            next_pages[p] = (1 - damping_factor) / all_pages_cnt
    return next_pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = {}
    all_pages = list(corpus.keys())
    all_pages_cnt = len(corpus.keys())
    transitions = []
    for p in all_pages:
        pagerank_dict[p] = 1 / all_pages_cnt
        transitions.append(transition_model(corpus, p, damping_factor))

    for _ in range(n - 1):
        new_pagerank_dict = defaultdict(int)
        for i in range(all_pages_cnt):
            p = all_pages[i]
            this_page_probability = pagerank_dict[p]
            for link in transitions[i].keys():
                new_pagerank_dict[link] += this_page_probability * transitions[i][link]

        pagerank_dict = dict(new_pagerank_dict)
    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = {}
    all_pages = list(corpus.keys())
    all_pages_cnt = len(corpus.keys())
    for p in all_pages:
        pagerank_dict[p] = 1 / all_pages_cnt

    changes = True
    while changes:
        changes = False
        new_pagerank_dict = defaultdict(int)
        for idx in range(all_pages_cnt):
            p = all_pages[idx]
            new_pagerank_dict[p] = (1 - damping_factor) * all_pages_cnt
            
        for idx in range(all_pages_cnt):
            p = all_pages[idx]
            if abs(pagerank_dict[p] - new_pagerank_dict[p]) > 0.001:
                changes = True
                break

        pagerank_dict = dict(new_pagerank_dict)

    return pagerank_dict


if __name__ == "__main__":
    main()
