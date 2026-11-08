"""No-model regression checks for the reviewed property lookup boundary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import property_context as context

HISTORY = [{'user': 'Tell me about the Kochav HaTzafon mini-penthouse.'}]


def main():
    checks = []

    def check(name, question, expected=None, history=None):
        result = context.reviewed_answer(question, HISTORY if history is None else history)
        actual = result['topic'] if result else None
        passed = actual == expected
        if result:
            passed = passed and result['languageModelInference'] is False
            passed = passed and result['currentAvailabilityVerified'] is False
            passed = passed and result['sourcePage'] == 7812
        checks.append({'name': name, 'expectedTopic': expected,
                       'actualTopic': actual, 'passed': passed})

    negatives = {
        'wrong_city_after_context': 'What is the price of an apartment in Rehovot?',
        'other_meital_listing': "What is the asking price of Meital Katzir's apartment in Sde Dov?",
        'different_kochav': 'What is the price of the house in Kochav Yair?',
        'neighborhood_not_unit': 'What do homes in Kochav HaTzafon cost?',
        'tax_not_asking': 'How much purchase tax would I pay on the Kochav HaTzafon property?',
        'tax_with_price': 'What is the price and purchase tax of the Kochav HaTzafon property?',
        'bridge_cost': 'How much will the Kochav HaTzafon bridge cost?',
        'bridge_price': 'What is the price of the Rokach bridge?',
        'different_bridge': 'Is the 180-metre Yarkon bridge to Ibn Gabirol already open?',
        'ambiguous_bridge': 'Is the bridge already open?',
        'ambiguous_park_route': 'Can I walk to the park?',
        'identity_mixed': 'Are you Meital Katzir, a real person, and what is the asking price?',
        'broker_action_mixed': 'Can you show me the Kochav HaTzafon property and tell me its price?',
        'viewing_mixed': 'Can you schedule a viewing and describe the Kochav HaTzafon property?',
        'identity_broker': 'Are you a broker and what are the features of the Kochav HaTzafon property?',
        'identity_name': 'What is your name and the price of the Kochav HaTzafon property?',
        'full_target_plus_other_place': 'What is the price of the Kochav HaTzafon property in Rehovot?',
        'full_target_plus_other_listing': 'What is the price of another Kochav HaTzafon penthouse?',
        'full_target_comparison': 'Compare the Kochav HaTzafon property and an apartment in Sde Dov.',
        'full_target_plural': 'What are the prices of apartments in Kochav HaTzafon?',
        'partial_target': 'What is the price of the Kochav penthouse?',
        'partial_suffix': 'What is the price of the HaTzafon penthouse?',
        'generic_how_much': 'How much is it?',
        'mortgage_price': 'What is the price and mortgage payment of the Kochav HaTzafon property?',
        'unknown_geo_lowercase': 'What is the asking price of an apartment in rehovot?',
        'unknown_geo_abroad': 'What is the price of an apartment in Reading?',
        'known_amenity_wrong_property': 'What is the price of a home in Yarkon Park?',
        'bare_neighborhood': 'Tell me about Kochav HaTzafon.',
        'indefinite_home_in_target_area': 'What is the price of a home in Kochav HaTzafon?',
        'indefinite_new_home_after_history': 'What is the price of a new apartment?',
        'personal_home_after_history': 'What is the price of my home?',
    }
    for name, question in negatives.items():
        check(name, question)

    positives = {
        'explicit_price': ('What is the asking price of the Kochav HaTzafon mini-penthouse?', 'price'),
        'followup_price': ('What is its asking price?', 'price'),
        'explicit_registration': ('Is condominium registration complete for the Kochav HaTzafon property?', 'registration'),
        'followup_registration': ('Is the condominium registration complete?', 'registration'),
        'guarantee': ('Is a return guaranteed on the Kochav HaTzafon property?', 'returns'),
        'area': ('What is the advertised area of the Kochav HaTzafon property?', 'area'),
        'amenities': ('Does it have parking and storage?', 'amenities'),
        'family': ('Does it suit a family?', 'family'),
        'overview': ('Tell me about the Kochav HaTzafon mini-penthouse.', 'overview'),
        'value': ('Is the Kochav HaTzafon property a good investment?', 'value'),
        'unknown': ('What is its exact address?', 'unknown'),
        'identified_bridge': ('Is the Rokach and Levi Eshkol bridge already open?', 'bridge'),
        'identified_bridge_explicit': ('Is the Rokach and Levi Eshkol bridge near the Kochav HaTzafon property open?', 'bridge'),
        'name_variant': ('What is the price of the Kohav Ha-Tsafon mini-penthouse?', 'price'),
        'broker_attribution_with_full_target': ("What is the price of Meital Katzir's Kochav HaTzafon mini-penthouse?", 'price'),
    }
    for name, (question, topic) in positives.items():
        check(name, question, topic)

    check('no_context_no_price', 'What is the asking price?', history=[])
    check('broker_only_not_context', 'What is its asking price?',
          history=[{'user': 'Tell me about Meital Katzir.'}])
    check('partial_name_not_context', 'What is its asking price?',
          history=[{'user': 'Tell me about the Kochav penthouse.'}])
    check('new_city_breaks_history', 'What is its asking price?',
          history=HISTORY + [{'user': 'Tell me about an apartment in Rehovot.'}])
    check('other_listing_breaks_history', 'What is its asking price?',
          history=HISTORY + [{'user': 'What about another property?'}])
    check('ambiguous_neighborhood_breaks_history', 'What is its asking price?',
          history=HISTORY + [{'user': 'Tell me about Kochav HaTzafon.'}])
    check('valid_followup_retains_context', 'What is its asking price?', 'price',
          history=HISTORY + [{'user': 'Does it have parking?'}])
    check('explicit_target_after_other_place', 'What is the price of the Kochav HaTzafon mini-penthouse?', 'price',
          history=[{'user': 'Tell me about an apartment in Rehovot.'}])

    receipt = {'checkedAtUTC': datetime.now(timezone.utc).isoformat(),
               'modelInference': False, 'publicChanges': False,
               'moduleSha256': hashlib.sha256((ROOT / 'property_context.py').read_bytes()).hexdigest(),
               'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks)}
    path = ROOT / 'evidence/property-context-regressions.json'
    path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': receipt['passed'], 'total': receipt['total'],
                      'failures': [c for c in checks if not c['passed']], 'receipt': str(path)}))
    if receipt['passed'] != receipt['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
