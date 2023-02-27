# AI x Bookathon
# MindsLab, Inc.

import random
import os, re
from pathlib import Path


'''
Feeding a model with sampled data during train is a way of data augmentation. 
 Because when you try inference later, you may feed the model a prompt text 
 ('infer_text') starting from any position of paragraph or sentence, not always 
 from the beginnig.

It's up to your strategy of feeding & inferring.
'''
class NsgDataFeeder(object):
    def __init__(self, data_dir, tokenizer):
        self.data_dir_path = Path(data_dir)
        self.tokenizer = tokenizer

        # exclude empty files
        self.text_files = [text_file for text_file in self.data_dir_path.rglob('*.txt') 
                                         if text_file.read_text().strip() != '']

    def feed(self, length=None):
        text_file = random.choice(self.text_files)
        text = text_file.read_text(encoding='utf-8')    # if encoding error occurs, fix here.

        # return self._no_sample(text, length)
        # return self._token_sample(text, length)
        # return self._sent_sample(text, length)
        # return self._sent_sample_repeat(text, length)
        # return self._sent_sample_append(text, length)
        return self._token_sample_append(text, length)

    def _no_sample(self, text, length):
        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        if len(token_ids) < length:
            token_ids += [0] * (length - len(token_ids))

        return token_ids[:length]

    def _token_sample(self, text, length):
        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        begin_index = random.randint(0, len(token_ids) - length)
        sampled = token_ids[begin_index:begin_index+length]
        sampled += [0] * (length - len(sampled))

        return sampled[:length]

    def _token_sample_repeat(self, text, length):
        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        # duplicate itself if the number of tokens is shorter than sampling length
        if len(token_ids) < length:
            token_ids = (length // len(token_ids) + 1) * token_ids

        begin_index = random.randint(0, len(token_ids) - length)
        sampled = token_ids[begin_index:begin_index+length]

        return sampled[:length]

    def _token_sample_append(self, text, length):
        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        # append another text if the number of tokens is shorter than sampling length
        while len(token_ids) < length:
            appending_text = random.choice(self.text_files).read_text(encoding='utf-8')
            token_ids += self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(appending_text))

        begin_index = random.randint(0, len(token_ids) - length)
        sampled = token_ids[begin_index:begin_index+length]

        return sampled[:length]

    def _sent_sample_repeat(self, text, length):
        sentences = split_text_into_sentences(text)
        sentences_tokenized = [self.tokenizer.tokenize(sent) for sent in sentences if sent is not '']

        begin_index = random.randrange(0, len(sentences_tokenized)-2) if len(sentences_tokenized) > 2 else 0
        selected_sents = sentences_tokenized[begin_index:]

        token_ids = self.tokenizer.convert_tokens_to_ids([token for sent in selected_sents for token in sent])
        whole_token_ids = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(text)) 

        if len(token_ids) < length:
            token_ids += (length // len(whole_token_ids) + 1) * whole_token_ids

        return token_ids[:length]

    def _sent_sample_append(self, text, length):
        sentences = split_text_into_sentences(text)
        sentences_tokenized = [self.tokenizer.tokenize(sent) for sent in sentences if sent is not '']

        begin_index = random.randrange(0, len(sentences_tokenized)-2) if len(sentences_tokenized) > 2 else 0
        selected_sents = sentences_tokenized[begin_index:]

        token_ids = self.tokenizer.convert_tokens_to_ids([token for sent in selected_sents for token in sent])
        while len(token_ids) < length:
            appending_text = random.choice(self.text_files).read_text(encoding='utf-8')
            token_ids += self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(appending_text))

        return token_ids[:length]


# Utility function to split a text into sentences
ending_chars = '[다요죠오네나라자아"][\.]+'     # it's perhaps a incomplete list for your data. adjust it.
ending_marks = '[!?][\.]*'
ending_exceptions = '["\']'
whitespaces = '[ \n\t\*]'
sep_token = '<<SEP>>'

def split_text_into_sentences(text):
    converted = re.sub('(?P<ending>{})(?!{})[ ]*'.format(ending_chars, ending_exceptions), '\g<ending>{}'.format(sep_token),
        re.sub('(?P<ending>{})(?!{})[ ]*'.format(ending_marks, ending_exceptions), '\g<ending>{}'.format(sep_token),
        re.sub('[ ]+', ' ', 
        re.sub('{}+'.format(whitespaces), ' ', text))))

    sents = converted.strip().split(sep_token)
    return sents[:-1] if len(sents) > 1 and sents[-1] == '' else sents
