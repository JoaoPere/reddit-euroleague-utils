#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:29:24 2020

@author: pi
"""

from postgame import createEmptyThread, updateThread
import time

home_team = 'Unicaja'
away_team = 'Tofas'

sub, link = createEmptyThread(home_team, away_team, 'EC')
time.sleep(15)
updateThread(home_team, away_team, sub, link)