#!/bin/bash

cat gen.prefix         | python -mpyaml
cat buck.sig buck.name | python -mpyaml
cat  lex.sig  lex.name | python -mpyaml

