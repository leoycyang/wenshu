import re
from rapidfuzz import fuzz
from heapq import nlargest

def extract(full_text, anchor_regexp, context_before, context_after, extract_regexps):
    """
    Process full_text to extract relevant information based on anchors.
    Anchors are substrings defined by a parenthesized group named 'anchor' in anchor_regexp;
    the entire full_text will be processed to find all anchors.
    The context around each anchor is defined as the substring matching context_before before the anchor,
    followed by the anchor, and then the substring matching context_after after the anchor.
    The regular expression context_before should end with '$',
    and context_after should begin with '^'.
    Finally, extract_regexps are applied to the context:
    for each regexp, all named parenthesized groups will be extracted,
    and a dictionary with the group name, extracted string, and span will be generated;
    in the end, a list of all dictionaries generated over all regexps will be reported for the anchor.
    """
    anchor_pat = re.compile(anchor_regexp, flags=re.DOTALL)
    context_before_pat = re.compile(context_before, flags=re.DOTALL)
    context_after_pat = re.compile(context_after, flags=re.DOTALL)
    extract_pats = [re.compile(extract_regexp, flags=re.DOTALL) for extract_regexp in extract_regexps]
    # iterate through all anchor matches:
    results = []
    start_pos = 0
    while (anchor_match := anchor_pat.search(full_text, start_pos)) is not None:
        # identify anchor substring and its positions:
        anchor_span = anchor_match.span('anchor')
        anchor_substring = full_text[anchor_span[0]:anchor_span[1]]
        # find the match for context_before ending at anchor's start:
        before_match = context_before_pat.search(full_text[:anchor_span[0]])
        context_before_str = before_match.group(0) if before_match else ''
        # find the match for context_after starting at anchor's end:
        after_match = context_after_pat.search(full_text[anchor_span[1]:])
        context_after_str = after_match.group(0) if after_match else ''
        # build context string:
        context = context_before_str + anchor_substring + context_after_str
        # evaluate extract_regexp over context, extract all groups:
        extracts = []
        for extract_pat in extract_pats:
            for extract_match in extract_pat.finditer(context):
                for group, text in extract_match.groupdict().items():
                    begin, end = extract_match.span(group)
                    begin += anchor_span[0] - len(context_before_str)
                    end += anchor_span[0] - len(context_after_str)
                    extracts.append({
                        'label': group,
                        'text': text,
                        'span': (begin, end),
                    })
        # order by span and deduplicate:
        final_extracts = []
        for extract in sorted(extracts, key=lambda entry: entry['span']):
            if not any(e for e in final_extracts if e['label'] == extract['label'] and e['span'] == extract['span']):
                final_extracts.append(extract)
        results.append({
            'anchor': anchor_substring,
            'anchor_span': anchor_span,
            'context': context,
            'context_span': (anchor_span[0] - len(context_before_str), anchor_span[1] + len(context_after_str)),
            'extracts': final_extracts,
        })
        # set starting search position for the next anchor:
        start_pos = anchor_span[1]
    return results

def simrank(target: str, candidates: list[str], topk: int = 3) -> list[tuple[int, float]]:
    """
    Given a target string and a list of candidate strings, return a list of topk fuzzy matches.
    Each returned entry consists of the match's index in the candidate list, as well as the similarity score.
    The entries are sorted from greatest similarity score to least similarity score, using rapidfuzz.fuzz.ratio().
    """
    scores = [(i, fuzz.ratio(target, cand)) for i, cand in enumerate(candidates)]
    return nlargest(topk, scores, key=lambda x: x[1])

def combine_scores(matches: list[tuple[int, str, float]], factor_weights: dict[str, float]) -> list[tuple[int, float]]:
    """Given a list of matches characterized by (case#, factor, score), where score is in [0,1],
    compute the combined scores for all case#, sorted by score descending.
    If there are multiple matches for the same case and same factor, only the highest score is considered.
    Each factor score is further weighed by the given weights dictionary.
    The final score is normalized to be within [0,1].
    """
    factor_max: dict[tuple[int, str], float] = {}
    for case, factor, score in matches:
        if score > factor_max.get((case, factor), 0.0):
            factor_max[(case, factor)] = score
    scores = {}
    for (case, factor), max_score in factor_max.items():
        if case not in scores:
            scores[case] = 0.0
        scores[case] += max_score * factor_weights[factor]
    for case in scores:
        scores[case] /= sum(factor_weights.values())
    return sorted(scores.items(), key = lambda x: - x[1])
