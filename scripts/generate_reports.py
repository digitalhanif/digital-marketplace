#!/usr/bin/env python3
"""Render a concise Markdown research report from a validated record."""
def report(item):
    return f"""# {item.get('name','Opportunity')}
Research date: {item.get('date','Not recorded')}
Market: {item.get('market','USA')}
Score: {item.get('score','Not scored')}
Evidence confidence: {item.get('confidence','LOW')}
Decision: {item.get('decision','WATCH')}
## Evidence
{item.get('evidence','No verified evidence supplied')}
## Next step
{item.get('next_step','Collect more evidence')}
"""
