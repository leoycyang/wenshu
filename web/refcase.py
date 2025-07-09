import re

def find_highlight_spans(fulltext, anchor_regex, extraction_regex):
    anchor_pattern = re.compile(anchor_regex)
    extract_pattern = re.compile(extraction_regex)

    highlight_spans = []

    for anchor_match in anchor_pattern.finditer(fulltext):
        anchor_start = anchor_match.start(1)
        anchor_end = anchor_match.end(1)

        context_start = max(0, anchor_start - 100)
        context_end = min(len(fulltext), anchor_end + 100)
        context_text = fulltext[context_start:context_end]
        print(context_text)

        extracted_spans = []
        for m in extract_pattern.finditer(context_text):
            span_start, span_end = m.span()
            extracted_spans.append((context_start + span_start, context_start + span_end))

        # add context highlight (with nested extracted inside)
        highlight_spans.append({
            "context": [context_start, context_end],
            "extracted": extracted_spans
        })

    return highlight_spans
