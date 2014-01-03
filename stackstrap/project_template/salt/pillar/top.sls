#
# StackStrap auto-generated pillar data top.sls file
#
# Generated using the following template:
# {{ name }} - {{ template_url }}
#

base:
  '*':
    - stackstrap
    - packages
    - services
    - {{ name }}

# vim: set ft=yaml et sw=2 ts=2 sts=2 :
