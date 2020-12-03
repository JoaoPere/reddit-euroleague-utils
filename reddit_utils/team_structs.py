from collections import namedtuple

team_info_by_fs = dict()
FlashScoreTeamParse = namedtuple(
    'TeamNameParsed', 'official reddit letter3_md full_md')

team_info_by_fs['CSKA Moscow'] = FlashScoreTeamParse('CSKA Moscow', 'CSKA Moscow', '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2020)',
                                                     '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2020)')
team_info_by_fs['Fenerbahce'] = FlashScoreTeamParse('Fenerbahce Beko Istanbul', 'Fenerbahce', '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2020)',
                                                    '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2020)')
team_info_by_fs['Anadolu Efes'] = FlashScoreTeamParse('Anadolu Efes Istanbul', 'Anadolu Efes', '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2020)',
                                                      '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2020)')
team_info_by_fs['Bayern'] = FlashScoreTeamParse('FC Bayern Munich', 'Bayern Munich', '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2020)',
                                                '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2020)')
team_info_by_fs['Barcelona'] = FlashScoreTeamParse('FC Barcelona', 'Barcelona', '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2020)',
                                                   '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2020)')
team_info_by_fs['Olympiacos'] = FlashScoreTeamParse('Olympiacos Piraeus', 'Olympiacos', '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2020)',
                                                    '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2020)')
team_info_by_fs['Khimki M.'] = FlashScoreTeamParse('Khimki Moscow Region', 'Khimki', '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2020)',
                                                   '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2020)')
team_info_by_fs['Maccabi Tel Aviv'] = FlashScoreTeamParse('Maccabi Playtika Tel Aviv', 'Maccabi Tel Aviv', '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2020)',
                                                          '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2020)')
team_info_by_fs['Zalgiris Kaunas'] = FlashScoreTeamParse('Zalgiris Kaunas', 'Zalgiris', '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2020)',
                                                         '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2020)')
team_info_by_fs['Baskonia'] = FlashScoreTeamParse('TD Systems Baskonia Vitoria-Gasteiz', 'Saski Baskonia', '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2020)',
                                                  '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2020)')
team_info_by_fs['Real Madrid'] = FlashScoreTeamParse('Real Madrid', 'Real Madrid', '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2020)',
                                                     '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2020)')
team_info_by_fs['Olimpia Milano'] = FlashScoreTeamParse('AX Armani Exchange Milan', 'Olimpia Milano', '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2020)',
                                                        '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2020)')
team_info_by_fs['Panathinaikos'] = FlashScoreTeamParse('Panathinaikos OPAP Athens', 'Panathinaikos', '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2020)',
                                                       '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2020)')
team_info_by_fs['Lyon-Villeurbanne'] = FlashScoreTeamParse('LDLC ASVEL Villeurbanne', 'ASVEL', '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2020)',
                                                           '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2020)')
team_info_by_fs['Alba Berlin'] = FlashScoreTeamParse('ALBA Berlin', 'Alba Berlin', '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2020)',
                                                     '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2020)')
team_info_by_fs['Valencia'] = FlashScoreTeamParse('Valencia Basket', 'Valencia', '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2020)',
                                                  '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2020)')
team_info_by_fs['Crvena zvezda mts'] = FlashScoreTeamParse('Crvena Zvezda mts Belgrade', 'Crvena Zvezda', '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2020)',
                                                           '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2020)')
team_info_by_fs['Zenit Petersburg'] = FlashScoreTeamParse('Zenit St Petersburg', 'Zenit', '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2020)',
                                                          '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2020)')

# Eurocup teams
team_info_by_fs['Buducnost'] = FlashScoreTeamParse('Buducnost VOLI Podgorica', 'Buducnost', '[BUD](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2020)',
                                                   '[Buducnost](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2020)')
team_info_by_fs['Promitheas'] = FlashScoreTeamParse('Promitheas Patras', 'Promitheas Patras', '[PRO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2020)',
                                                    '[Promitheas Patras](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2020)')
team_info_by_fs['Monaco'] = FlashScoreTeamParse('AS Monaco', 'AS Monaco', '[MON](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2020)',
                                                '[AS Monaco](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2020)')
team_info_by_fs['MoraBanc Andorra'] = FlashScoreTeamParse('MoraBanc Andorra', 'BC Andorra', '[AND](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2020)',
                                                          '[BC Andorra](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2020)')
team_info_by_fs['Ulm'] = FlashScoreTeamParse('ratiopharm Ulm', 'ratiopharm Ulm', '[ULM](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2020)',
                                             '[ratiopharm Ulm](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2020)')
team_info_by_fs['Virtus Bologna'] = FlashScoreTeamParse('Virtus Segafredo Bologna', 'Virtus Bologna', '[VIR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2020)',
                                                        '[Virtus Bologna](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2020)')
team_info_by_fs['Partizan'] = FlashScoreTeamParse('Partizan NIS Belgrade', 'Partizan', '[PAR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2020)',
                                                  '[Partizan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2020)')
team_info_by_fs['Lokomotiv Kuban'] = FlashScoreTeamParse('Lokomotiv Kuban Krasnodar', 'Lokomotiv Kuban', '[LOK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2020)',
                                                         '[Lokomotiv Kuban](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2020)')
team_info_by_fs['Venezia'] = FlashScoreTeamParse('Umana Reyer Venice', 'Reyer Venezia', '[URV](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2020)',
                                                 '[Reyer Venezia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2020)')
team_info_by_fs['Nanterre'] = FlashScoreTeamParse('Nanterre 92', 'Nanterre 92', '[NTR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2020)',
                                                  '[Nanterre 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2020)')
team_info_by_fs['Joventut Badalona'] = FlashScoreTeamParse('Joventut Badalona', 'Joventut Badalona', '[CJB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2020)',
                                                           '[Joventut Badalona](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2020)')
team_info_by_fs['Brescia'] = FlashScoreTeamParse('Germani Brescia', 'Brescia Leonessa', '[BRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2020)',
                                                 '[Brescia Leonessa](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2020)')
team_info_by_fs['Unics Kazan'] = FlashScoreTeamParse('UNICS Kazan', 'UNICS Kazan', '[UNK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2020)',
                                                     '[UNICS Kazan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2020)')
team_info_by_fs['Cedevita Olimpija'] = FlashScoreTeamParse('Cedevita Olimpija Ljubljana', 'Cedevita Olimpija Ljubljana', '[COL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2020)',
                                                           '[Cedevita Olimpija Ljubljana](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2020)')
team_info_by_fs['Unicaja'] = FlashScoreTeamParse('Unicaja Malaga', 'Unicaja Malaga', '[UNI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2020)',
                                                 '[Unicaja Malaga](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2020)')
team_info_by_fs['Trento'] = FlashScoreTeamParse('Dolomiti Energia Trento', 'Aquila Basket Trento', '[TRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2020)',
                                                '[Aquila Basket Trento](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2020)')
team_info_by_fs['Bahcesehir Kol.'] = FlashScoreTeamParse('Bahcesehir Koleji Istanbul', 'Bahcesehir', '[BAH](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BAH&seasoncode=U2020)',
                                                         '[Bahcesehir](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BAH&seasoncode=U2020)')
team_info_by_fs['Levallois'] = FlashScoreTeamParse('Boulogne Metropolitans 92', 'Metropolitans 92', '[MET](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAI&seasoncode=U2020)',
                                                   '[Metropolitans 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAI&seasoncode=U2020)')
team_info_by_fs['Bursaspor'] = FlashScoreTeamParse('Frutti Extra Bursaspor', 'Bursaspor', '[BUR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BBU&seasoncode=U2020)',
                                                   '[Bursaspor](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BBU&seasoncode=U2020)')
team_info_by_fs['Gran Canaria'] = FlashScoreTeamParse('Herbalife Gran Canaria', 'Gran Canaria', '[GCA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=CAN&seasoncode=U2020)',
                                                      '[Gran Canaria](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=CAN&seasoncode=U2020)')
team_info_by_fs['JL Bourg'] = FlashScoreTeamParse('JL Bourg en Bresse', 'JL Bourg', '[BOU](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BOU&seasoncode=U2020)',
                                                  '[JL Bourg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BOU&seasoncode=U2020)')
team_info_by_fs['Lietkabelis'] = FlashScoreTeamParse('Lietkabelis Panevezys', 'Lietkabelis', '[LKB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LKB&seasoncode=U2020',
                                                     '[Lietkabelis](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LKB&seasoncode=U2020)')
team_info_by_fs['Mornar Bar'] = FlashScoreTeamParse('Mornar Bar', 'Mornar Bar', '[MBA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MBA&seasoncode=U2020)',
                                                    '[Mornar Bar](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MBA&seasoncode=U2020)')
team_info_by_fs['Antwerp Giants'] = FlashScoreTeamParse('Telenet Giants Antwerp', 'Antwerp Giants', '[ANT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANT&seasoncode=U2020)',
                                                        '[Antwerp Giants](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANT&seasoncode=U2020)')

team_info_by_official = dict()
OfficialTeamParse = namedtuple(
    'OfficialTeamParse', 'reddit letter3_md full_md')

team_info_by_official['CSKA Moscow'] = OfficialTeamParse('CSKA Moscow', '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2020)',
                                                         '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2020)')
team_info_by_official['Fenerbahce Beko Istanbul'] = OfficialTeamParse(
    'Fenerbahce', '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2020)', '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2020)')
team_info_by_official['Anadolu Efes Istanbul'] = OfficialTeamParse(
    'Anadolu Efes', '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2020)', '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2020)')
team_info_by_official['FC Bayern Munich'] = OfficialTeamParse('Bayern Munich', '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2020)',
                                                              '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2020)')
team_info_by_official['FC Barcelona'] = OfficialTeamParse('Barcelona', '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2020)',
                                                          '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2020)')
team_info_by_official['Olympiacos Piraeus'] = OfficialTeamParse('Olympiacos', '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2020)',
                                                                '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2020)')
team_info_by_official['Khimki Moscow Region'] = OfficialTeamParse(
    'Khimki', '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2020)', '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2020)')
team_info_by_official['Maccabi Playtika Tel Aviv'] = OfficialTeamParse('Maccabi Tel Aviv', '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2020)',
                                                                       '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2020)')
team_info_by_official['Zalgiris Kaunas'] = OfficialTeamParse('Zalgiris Kaunas', '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2020)',
                                                             '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2020)')
team_info_by_official['TD Systems Baskonia Vitoria-Gasteiz'] = OfficialTeamParse('Saski Baskonia', '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2020)',
                                                                                 '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2020)')
team_info_by_official['Real Madrid'] = OfficialTeamParse('Real Madrid', '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2020)',
                                                         '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2020)')
team_info_by_official['AX Armani Exchange Milan'] = OfficialTeamParse(
    'Olimpia Milano', '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2020)', '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2020)')
team_info_by_official['Panathinaikos OPAP Athens'] = OfficialTeamParse(
    'Panathinaikos', '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2020)', '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2020)')
team_info_by_official['LDLC ASVEL Villeurbanne'] = OfficialTeamParse(
    'ASVEL', '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2020)', '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2020)')
team_info_by_official['ALBA Berlin'] = OfficialTeamParse('Alba Berlin', '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2020)',
                                                         '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2020)')
team_info_by_official['Valencia Basket'] = OfficialTeamParse('Valencia', '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2020)',
                                                             '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2020)')
team_info_by_official['Crvena Zvezda mts Belgrade'] = OfficialTeamParse(
    'Crvena Zvezda', '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2020)', '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2020)')
team_info_by_official['Zenit St Petersburg'] = OfficialTeamParse(
    'Zenit', '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2020)', '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2020)')

# Eurocup teams
team_info_by_official['Buducnost VOLI Podgorica'] = OfficialTeamParse('Buducnost', '[BUD](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2020)',
                                                                      '[Buducnost](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2020)')
team_info_by_official['Promitheas Patras'] = OfficialTeamParse('Promitheas Patras', '[PRO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2020)',
                                                               '[Promitheas Patras](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2020)')
team_info_by_official['AS Monaco'] = OfficialTeamParse('AS Monaco', '[MON](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2020)',
                                                       '[AS Monaco](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2020)')
team_info_by_official['MoraBanc Andorra'] = OfficialTeamParse('BC Andorra', '[AND](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2020)',
                                                              '[BC Andorra](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2020)')
team_info_by_official['ratiopharm Ulm'] = OfficialTeamParse('ratiopharm Ulm', '[ULM](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2020)',
                                                            '[ratiopharm Ulm](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2020)')
team_info_by_official['Virtus Segafredo Bologna'] = OfficialTeamParse('Virtus Bologna', '[VIR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2020)',
                                                                      '[Virtus Bologna](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2020)')
team_info_by_official['Partizan NIS Belgrade'] = OfficialTeamParse('Partizan', '[PAR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2020)',
                                                                   '[Partizan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2020)')
team_info_by_official['Lokomotiv Kuban Krasnodar'] = OfficialTeamParse('Lokomotiv Kuban', '[LOK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2020)',
                                                                       '[Lokomotiv Kuban](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2020)')
team_info_by_official['Umana Reyer Venice'] = OfficialTeamParse('Reyer Venezia', '[URV](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2020)',
                                                                '[Reyer Venezia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2020)')
team_info_by_official['Nanterre 92'] = OfficialTeamParse('Nanterre 92', '[NTR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2020)',
                                                         '[Nanterre 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2020)')
team_info_by_official['Joventut Badalona'] = OfficialTeamParse('Joventut Badalona', '[CJB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2020)',
                                                               '[Joventut Badalona](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2020)')
team_info_by_official['Germani Brescia'] = OfficialTeamParse('Brescia Leonessa', '[BRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2020)',
                                                             '[Brescia Leonessa](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2020)')
team_info_by_official['UNICS Kazan'] = OfficialTeamParse('UNICS Kazan', '[UNK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2020)',
                                                         '[UNICS Kazan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2020)')
team_info_by_official['Cedevita Olimpija Ljubljana'] = OfficialTeamParse('Cedevita Olimpija Ljubljana', '[COL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2020)',
                                                                         '[Cedevita Olimpija Ljubljana](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2020)')
team_info_by_official['Unicaja Malaga'] = OfficialTeamParse('Unicaja Malaga', '[UNI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2020)',
                                                            '[Unicaja Malaga](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2020)')
team_info_by_official['Dolomiti Energia Trento'] = OfficialTeamParse('Aquila Basket Trento', '[TRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2020)',
                                                                     '[Aquila Basket Trento](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2020)')
team_info_by_official['Bahcesehir Koleji Istanbul'] = OfficialTeamParse('Bahcesehir', '[BAH](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BAH&seasoncode=U2020)',
                                                                        '[Bahcesehir](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BAH&seasoncode=U2020)')
team_info_by_official['Boulogne Metropolitans 92'] = OfficialTeamParse('Metropolitans 92', '[MET](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAI&seasoncode=U2020)',
                                                                       '[Metropolitans 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAI&seasoncode=U2020)')
team_info_by_official['Frutti Extra Bursaspor'] = OfficialTeamParse('Bursaspor', '[BUR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BBU&seasoncode=U2020)',
                                                                    '[Bursaspor](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BBU&seasoncode=U2020)')
team_info_by_official['Herbalife Gran Canaria'] = OfficialTeamParse('Gran Canaria', '[GCA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=CAN&seasoncode=U2020)',
                                                                    '[Gran Canaria](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=CAN&seasoncode=U2020)')
team_info_by_official['JL Bourg en Bresse'] = OfficialTeamParse('JL Bourg', '[BOU](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BOU&seasoncode=U2020)',
                                                                '[JL Bourg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BOU&seasoncode=U2020)')
team_info_by_official['Lietkabelis Panevezys'] = OfficialTeamParse('Lietkabelis', '[LKB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LKB&seasoncode=U2020',
                                                                   '[Lietkabelis](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LKB&seasoncode=U2020)')
team_info_by_official['Mornar Bar'] = OfficialTeamParse('Mornar Bar', '[MBA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MBA&seasoncode=U2020)',
                                                        '[Mornar Bar](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MBA&seasoncode=U2020)')
team_info_by_official['Telenet Giants Antwerp'] = OfficialTeamParse('Antwerp Giants', '[ANT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANT&seasoncode=U2020)',
                                                                    '[Antwerp Giants](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANT&seasoncode=U2020)')

'''
# OUT OF THE COMPETITION THIS YEAR
team_info_by_official['Asseco Arka Gdyni'] = OfficialTeamParse('Arka Gdynia', '[ARK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2020)',
                                                               '[Arka Gdynia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2020)')
team_info_by_official['Limoges CSP'] = OfficialTeamParse('Limoges CSP', '[CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2020)',
                                                         '[Limoges CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2020)')
team_info_by_official['Rytas Vilnius'] = OfficialTeamParse('Rytas', '[RYT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2020)',
                                                           '[Rytas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2020)')
team_info_by_official['Tofas Bursa'] = OfficialTeamParse('Tofas', '[TOF](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2020)',
                                                         '[Tofas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2020)')
team_info_by_official['Darussafaka Tekfen Istanbul'] = OfficialTeamParse('Darussafaka', '[DTI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2020)',
                                                                         '[Darussafaka](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2020)')
team_info_by_official['Galatasaray Doga Sigorta Istanbul'] = OfficialTeamParse(
    'Galatasaray', '[GAL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2020)', '[Galatasaray](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2020)')
team_info_by_official['EWE Baskets Oldenburg'] = OfficialTeamParse('EWE Baskets Oldenburg', '[EBO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2020)',
                                                                   '[EWE Baskets Oldenburg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2020)')
team_info_by_official['Maccabi Rishon LeZion'] = OfficialTeamParse('Maccabi Rishon LeZion', '[RLZ](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2020)',
                                                                   '[Maccabi Rishon LeZion](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2020)')


team_info_by_fs['Tofas'] = FlashScoreTeamParse('Tofas Bursa', 'Tofas', '[TOF](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2020)',
                                               '[Tofas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2020)')
team_info_by_fs['Darussafaka'] = FlashScoreTeamParse('Darussafaka Tekfen Istanbul', 'Darussafaka', '[DTI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2020)',
                                                     '[Darussafaka](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2020)')
team_info_by_fs['Maccabi Rishon'] = FlashScoreTeamParse('Maccabi Rishon LeZion', 'Maccabi Rishon LeZion', '[RLZ](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2020)',
                                                        '[Maccabi Rishon LeZion](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2020)')
team_info_by_fs['Oldenburg'] = FlashScoreTeamParse('EWE Baskets Oldenburg', 'EWE Baskets Oldenburg', '[EBO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2020)',
                                                   '[EWE Baskets Oldenburg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2020)')
team_info_by_fs['Gdynia'] = FlashScoreTeamParse('Asseco Arka Gdynia', 'Arka Gdynia', '[ARK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2020)',
                                                '[Arka Gdynia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2020)')
team_info_by_fs['Rytas'] = FlashScoreTeamParse('Rytas Vilnius', 'Rytas', '[RYT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2020)',
                                               '[Rytas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2020)')
team_info_by_fs['Limoges'] = FlashScoreTeamParse('Limoges CSP', 'Limoges CSP', '[CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2020)',
                                                 '[Limoges CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2020)')
team_info_by_fs['Galatasaray'] = FlashScoreTeamParse('Galatasaray Doga Sigorta Istanbul', 'Galatasaray', '[GAL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2020)',
                                                     '[Galatasaray](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2020)')
'''
