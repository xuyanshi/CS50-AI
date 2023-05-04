from pagerank import *


def transition_model_test():
    """
    For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},
     the page was "1.html", and the damping_factor was 0.85,
      then the output of transition_model should be {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}.
    """
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    page = "1.html"
    damping_factor = 0.85

    print(transition_model(corpus, page, damping_factor))


# transition_model_test()

def sample_pagerank_test():
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    damping_factor = 0.85
    n = 10000

    print(sample_pagerank(corpus, damping_factor, n))


sample_pagerank_test()
