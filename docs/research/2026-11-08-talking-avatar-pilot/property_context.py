"""Reviewed facts for Ben's confirmed property example. No live-market claims.

These explicit answers are source-grounded editorial responses, not LLM inference.
The general buyer conversation remains a separate model path.
"""
from __future__ import annotations

import re

SOURCE_URL = 'https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/'
SOURCE_DATE = '2026-11-08'
SOURCE_PAGE = 7812


_NEIGHBORHOOD = re.compile(
    r'\b(?:kochav|kohav|kokhav|cochav)[\s-]*ha[\s-]?(?:tzafon|tsafon)\b', re.I)
_LISTING = re.compile(r'\b(?:mini[\s-]*penthouse|penthouse|listing|property|apartment|home)\b', re.I)
_ROLE_OR_ACTION = re.compile(
    r'\b(?:ignore|pretend|instructions?|human|person|robot|ai|fictional|'
    r'broker|agent|who are you|are you|your name|book\w*|arrang\w*|'
    r'negotiat\w*|submit\w*|represent\w*|show\w*|viewing\w*|tour\w*|'
    r'schedul\w*|contact\w*|call|meet|reserve|offer\w*)\b', re.I)
_OTHER_SUBJECT = re.compile(
    r'\b(?:another|other|different|elsewhere|instead|compare\w*|versus|vs|'
    r'neighbou?rhood|market|homes|houses|apartments|properties|listings|penthouses)\b', re.I)

# This editorial lookup intentionally accepts a small question vocabulary.
# Unknown place/name words cannot inherit an earlier listing's price or facts.
# A general language model can handle everything that falls outside this scope.
_QUESTION_WORDS = frozenset('''
    a an the this that it its s is are was be been does do did has have having
    what which how why when where can could would will should may might i me my
    we our you your for of on to with and or but about please tell describe
    in at from into near by already now still current currently exact advertised
    saved listed listing property apartment home mini penthouse new sale
    price asking area size square metres meters sqm terrace terraces balcony
    balconies indoor indoors outdoor built space generous large
    parking storage safe room rooms gym lift elevator amenity amenities facilities
    children family layout bedroom bedrooms master suite separate wing privacy
    registration registered condominium land registry title legal complete
    completed incomplete documents rights plans attachments check checks
    address street developer management fee fees completion year available availability
    investment bargain worth value good deal worthwhile guarantee guaranteed
    profit return returns yield appreciation appreciate appreciated future
    features special advantages benefits suitable suit need needs useful
    bridge planned proposed rokach levi eshkol yarkon park access walk walking
    pedestrian cycle cycling open opened opening construction under
'''.split())


def mentions_property(text):
    """The full neighbourhood name, never a broker or a partial place name."""
    return bool(_NEIGHBORHOOD.search(text))


def _scope_safe(question):
    if _ROLE_OR_ACTION.search(question) or _OTHER_SUBJECT.search(question):
        return False
    if re.search(r'\b(?:a|an|any|my|our|your)\s+(?:new\s+)?'
                 r'(?:mini[\s-]*)?(?:penthouse|listing|property|apartment|home)\b', question, re.I):
        # An indefinite or personally owned home is not this confirmed listing.
        return False
    remaining = _NEIGHBORHOOD.sub(' ', question)
    # Broker attribution is not an identifier, but may accompany the full name.
    if mentions_property(question):
        remaining = re.sub(r'\b(?:meital|meytal)\s+katzir\b', ' ', remaining, flags=re.I)
    words = re.findall(r"[\w]+", remaining.lower(), flags=re.UNICODE)
    if not words or any(word not in _QUESTION_WORDS for word in words):
        return False
    # Known amenity names are permitted only for their own route, never as the
    # supposed location of a different home whose price is being requested.
    if re.search(r'\b(?:rokach|levi|eshkol|yarkon|park)\b', remaining, re.I):
        if not re.search(r'\bbridge\b', remaining, re.I):
            return False
    return True


def _explicit_listing(question):
    return mentions_property(question) and bool(_LISTING.search(question))


def in_context(question, history):
    if not _scope_safe(question):
        return False
    if mentions_property(question):
        # A neighbourhood by itself does not identify this one listing.
        return _explicit_listing(question)
    # An intervening new/ambiguous subject breaks inheritance. Do not skip it
    # to resurrect an earlier listing merely because it remains in history.
    for turn in reversed(history[-2:]):
        previous = turn.get('user', '')
        if not _scope_safe(previous):
            return False
        if mentions_property(previous):
            return _explicit_listing(previous)
    return False


FACTS = [
    {'heading': 'Confirmed example: Meital Katzir mini-penthouse in Kochav HaTzafon',
     'text': 'The saved NadLan listing advertises an asking price of eighteen million shekels, five rooms, floor eleven of twelve, approximately 197 square metres of advertised built area and 76 square metres of terraces. These are advertised approximate figures, not current availability or registered measurements. Confirm current price and availability with the named broker.'},
    {'heading': 'Advertised features and buyer fit',
     'text': "The listing describes a master suite, a separate children's wing with a sea-view balcony, a large living room, terraces, two parking spaces, storage, a safe room, a lift, a residents' gym and a residents' room. Outdoor space and separated living areas may suit a family that values them. Near Yarkon Park. No evidence here establishes a bargain, guaranteed appreciation, yield or investment suitability."},
    {'heading': 'Material unresolved checks',
     'text': 'The listing says condominium registration is incomplete. Check the plans, registered area, parking and storage attachments, management fees, exact address, occupancy documents and future development affecting views. The planned Rokach and Levi Eshkol bridge into Yarkon Park is not an established open amenity. Older area figures differ; verify the architect plan and registration. Exact address, developer, fees, completion year and current availability are not established by this context.'},
]


def reviewed_answer(question, history):
    """Return a sourced exact reply only for a recognised fact question.

    Leave identity, broker-action requests, injected instructions and unrelated
    questions to the unchanged general role handling. Never claim live inference.
    """
    q = question.lower()
    # Mixed identity/action questions must reach the general role handler too.
    if _ROLE_OR_ACTION.search(q):
        return None
    # No numerical financial answer is inferred from an asking-price keyword.
    if re.search(r'\b(?:tax\w*|mortgage\w*|loan\w*|rent\w*|currency|dollars?|'
                 r'euros?|cost\w*|pay|payment\w*|commission\w*)\b', q):
        return None
    if not in_context(question, history):
        return None
    topic = None
    if re.search(r'\b(?:bridge|park access|walk to the park)\b', q):
        # The source describes two different bridges. Only the explicitly
        # identified Rokach/Levi Eshkol project has a reviewed reply here.
        if (re.search(r'\b(?:price|asking|how much)\b', q)
                or not re.search(r'\b(?:rokach|levi eshkol)\b', q)):
            return None
        topic = 'bridge'
    elif re.search(r'\b(?:guarantee\w*|profit|returns?|yield|appreciat\w*)\b', q):
        topic = 'returns'
    elif re.search(r'\b(?:investment|bargain|worth|value|good deal|worthwhile)\b', q):
        topic = 'value'
    elif re.search(r'\b(?:registration|registered|land registry|title|legal)\b', q):
        topic = 'registration'
    elif re.search(r'\b(?:address|street|developer|management|fees?|completion|available|availability)\b', q):
        topic = 'unknown'
    elif re.search(r'\b(?:price|asking price)\b', q):
        topic = 'price'
    elif re.search(r'\b(?:area|size|square|metres|meters|sqm|terraces?|balcon\w*)\b', q):
        topic = 'area'
    elif re.search(r'\b(?:parking|storage|safe room|gym|lift|elevator|amenit\w*)\b', q):
        topic = 'amenities'
    elif re.search(r'\b(?:children|family|layout|bedroom|rooms)\b', q):
        topic = 'family'
    elif re.search(r'\b(?:tell|describe|recommend|about|features|special|advantages|benefits)\b', q):
        topic = 'overview'
    answers = {
        'price': "The listing advertises eighteen million shekels, but the current asking price and availability need confirmation with Meital Katzir. Would this be a permanent home or a home for occasional visits?",
        'area': "The listing advertises about one hundred ninety-seven square metres of built area and seventy-six square metres of terraces, subject to checking the plans and incomplete condominium registration. Is generous outdoor space a priority for your household?",
        'amenities': "The listing includes two parking spaces, storage, a safe room, a lift, a residents' gym and a residents' room; their documents and ongoing costs need checking. Which facilities matter most to you?",
        'family': "The separate children's wing, master suite and terraces may suit a family wanting privacy alongside shared living space, according to the listing. How many people would use the home regularly?",
        'overview': "The listing highlights terraces, a separate children's wing and sea-facing views; condominium registration is incomplete and needs independent legal review. Would you like to examine the layout, outdoor space or purchase checks?",
        'value': "Its terraces, separated living areas and location near Yarkon Park may suit your needs. Incomplete registration, comparable sales and ownership costs need review. Which of those features matters most to you?",
        'returns': "I cannot guarantee profit or future appreciation; the listing's features do not establish an investment return, and an independent valuation needs comparable sales and ownership costs. Is your priority personal use or investment?",
        'registration': "The listing says condominium registration is incomplete, so a qualified lawyer should verify the rights, plans and attachments before a decision. Have you already appointed independent legal counsel?",
        'unknown': "The saved listing does not establish the current availability, exact address, developer or management fees; those details need confirmation with Meital Katzir and the relevant documents. Which detail would you like to clarify first?",
        'bridge': "The Rokach and Levi Eshkol bridge into Yarkon Park is described as planned, so I cannot present that route as already open. How important is current walking access to your daily routine?",
    }
    if topic is None:
        return None
    answer = answers[topic]
    return {'text': answer, 'mode': 'reviewed_property_facts', 'topic': topic,
            'sourceUrl': SOURCE_URL, 'sourcePage': SOURCE_PAGE, 'sourceDate': SOURCE_DATE,
            'currentAvailabilityVerified': False, 'languageModelInference': False}
