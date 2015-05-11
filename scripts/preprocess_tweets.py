#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

######################################################################################################

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

# The components of the tokenizer:
regex_strings = (
    emoticon_string
    ,
    # Twitter username:
    r"""(?:@[\w_]+)"""
    ,
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,    
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
)

word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
emoticon_re = re.compile(regex_strings[0], re.VERBOSE | re.I | re.UNICODE)
lengthening_re_before = re.compile(r"(.)\1{2,}", re.VERBOSE | re.I | re.UNICODE)

def tokenize(s):
    words = word_re.findall(s)
    words = map((lambda x : x if emoticon_re.search(x) else x.lower()), words)
    words = [lengthening_re_before.sub(r"\1\1\1", word) for word in words]

    return words

######################################################################################################

def preprocess(text, to_unicode=False):
  # transform to unicode
  if to_unicode:
    text = text.encode("utf8")

  # tokenize
  tokens = tokenize(text)

  return tokens

######################################################################################################

