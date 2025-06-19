#!/usr/bin/env python3

import copy
import glob
import jinja2
import jinja2.ext
import os
import shutil
import subprocess
import yaml
import json
import sys

def file_get_contents(filename, encoding=None):
    with open(filename, mode='r', encoding=encoding) as fh:
        return fh.read()

def file_put_contents(filename, s, encoding=None):
    with open(filename, mode='w', encoding=encoding) as fh:
        fh.write(s)

def get_kem_nistlevel(alg, docsdir):
    # KpqC 알고리즘들은 보안 레벨을 직접 지정
    if alg['family'] == 'NTRU+':
        name = alg['name_group']
        if name == 'ntru_plus_kem576':
            return 1
        elif name == 'ntru_plus_kem768':
            return 3
        elif name == 'ntru_plus_kem864':
            return 3
        elif name == 'ntru_plus_kem1152':
            return 5
        return None
    elif alg['family'] == 'SMAUG-T':
        name = alg['name_group']
        if name == 'smaug-t1':
            return 1
        elif name == 'smaug-t3':
            return 3
        elif name == 'smaug-t5':
            return 5
        return None

    # translate family names in generate.yml to directory names for liboqs algorithm datasheets
    if alg['family'] == 'CRYSTALS-Kyber': datasheetname = 'kyber'
    elif alg['family'] == 'SIDH': datasheetname = 'sike'
    elif alg['family'] == 'NTRU-Prime': datasheetname = 'ntruprime'
    else: datasheetname = alg['family'].lower().replace('-', '_')
    # load datasheet
    try:
        algymlfilename = os.path.join(docsdir, 'algorithms', 'kem', '{:s}.yml'.format(datasheetname))
        algyml = yaml.safe_load(file_get_contents(algymlfilename, encoding='utf-8'))
    except: # check alternate location in "oldalgs" folder
        algymlfilename = os.path.join("oqs-template", 'oldalgdocs', 'kem', '{:s}.yml'.format(datasheetname))
        algyml = yaml.safe_load(file_get_contents(algymlfilename, encoding='utf-8'))

    # hacks to match names
    def matches(name, alg):
        def simplify(s):
            return s.lower().replace('_', '').replace('-', '')
        if 'FrodoKEM' in name: name = name.replace('FrodoKEM', 'Frodo')
        if 'Saber-KEM' in name: name = name.replace('-KEM', '')
        if '-90s' in name: name = name.replace('-90s', '').replace('Kyber', 'Kyber90s')
        if simplify(name) == simplify(alg['name_group']): return True
        return False
    # find the variant that matches
    for variant in algyml['parameter-sets']:
        if matches(variant['name'], alg) or ('alias' in variant and matches(variant['alias'], alg)):
            return variant['claimed-nist-level']
    # Information file for algorithms no longer supported by liboqs:
    oldalgs = yaml.safe_load(file_get_contents(os.path.join("oqs-template", "oldalgs.yml"), encoding='utf-8'))
    name = alg['name_group']
    if name in oldalgs:
        return oldalgs[name]['claimed-nist-level']
    return None

def get_sig_nistlevel(family, alg, docsdir):
    # KpqC 서명 알고리즘들은 보안 레벨을 직접 지정
    if family['family'] == 'HAETAE':
        name = alg['name']
        if name == 'haetae2':
            return 1
        elif name == 'haetae3':
            return 3
        elif name == 'haetae5':
            return 5
        return None
    elif family['family'] == 'AIMer':
        name = alg['name']
        if name in ['aimer128s', 'aimer128f']:
            return 1
        elif name in ['aimer192s', 'aimer192f']:
            return 3
        elif name in ['aimer256s', 'aimer256f']:
            return 5
        return None

    # translate family names in generate.yml to directory names for liboqs algorithm datasheets
    if family['family'] == 'CRYSTALS-Dilithium': datasheetname = 'dilithium'
    elif family['family'] == 'SPHINCS-Haraka': datasheetname = 'sphincs'
    elif family['family'] == 'SPHINCS-SHA256': datasheetname = 'sphincs'
    elif family['family'] == 'SPHINCS-SHAKE256': datasheetname = 'sphincs'
    elif family['family'] == 'SPHINCS-SHA2': datasheetname = 'sphincs'
    elif family['family'] == 'SPHINCS-SHAKE': datasheetname = 'sphincs'
    else: datasheetname = family['family'].lower().replace('-', '_')
    # load datasheet
    algymlfilename = os.path.join(docsdir, 'algorithms', 'sig', '{:s}.yml'.format(datasheetname))
    algyml = yaml.safe_load(file_get_contents(algymlfilename, encoding='utf-8'))
    # hacks to match names
    def matches(name, alg):
        def simplify(s):
            return s.lower().replace('_', '').replace('-', '').replace('+', '')
        if simplify(name) == simplify(alg['name']): return True
        return False
    # find the variant that matches
    for variant in algyml['parameter-sets']:
        if matches(variant['name'], alg) or ('alias' in variant and matches(variant['alias'], alg)):
            return variant['claimed-nist-level']
    # Information file for algorithms no longer supported by liboqs:
    oldalgs = yaml.safe_load(file_get_contents(os.path.join("oqs-template", "oldalgs.yml"), encoding='utf-8'))
    name = alg['name']
    if name in oldalgs:
        return oldalgs[name]['claimed-nist-level']
    return None

def nist_to_bits(nistlevel):
   if nistlevel==1 or nistlevel==2:
      return 128
   elif nistlevel==3 or nistlevel==4:
      return 192
   elif nistlevel==5:
      return 256
   else: 
      return None

def complete_config(config, oqsdocsdir = None):
   if oqsdocsdir == None:
      if 'LIBOQS_DOCS_DIR' not in os.environ:
        print("Must include LIBOQS_DOCS_DIR in environment")
        exit(1)
      oqsdocsdir = os.environ["LIBOQS_DOCS_DIR"]
   for kem in config['kems']:
      if not "bit_security" in kem.keys():
         bits_level = nist_to_bits(get_kem_nistlevel(kem, oqsdocsdir))
         if bits_level == None: 
             print("Cannot find security level for {:s} {:s}".format(kem['family'], kem['name_group']))
             exit(1)
         kem['bit_security'] = bits_level
   for famsig in config['sigs']:
      for sig in famsig['variants']:
         if not "security" in sig.keys():
            bits_level = nist_to_bits(get_sig_nistlevel(famsig, sig, oqsdocsdir))
            if bits_level == None: 
                if sig['name'].startswith("rainbowI"):
                    bits_level=128
                else:
                    print("Cannot find security level for {:s} {:s}".format(famsig['family'], sig['name']))
                    exit(1)
            sig['security'] = bits_level
   return config

