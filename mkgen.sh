#!/bin/bash
cat fudz.1             | python -mpyaml
cat gen.prefix         | python -mpyaml
cat buck.sig buck.name | python -mpyaml
cat  lex.sig  lex.name | python -mpyaml
