from collections import namedtuple

team_info_by_fs = dict()
FlashScoreTeamParse = namedtuple(
    'TeamNameParsed', 'official reddit letter3_md full_md')

team_info_by_fs['CSKA Moscow'] = FlashScoreTeamParse('CSKA Moscow', 'CSKA Moscow', '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)',
                                                     '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)')
team_info_by_fs['Fenerbahce'] = FlashScoreTeamParse('Fenerbahce Beko Istanbul', 'Fenerbahce', '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)',
                                                    '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)')
team_info_by_fs['Anadolu Efes'] = FlashScoreTeamParse('Anadolu Efes Istanbul', 'Anadolu Efes', '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)',
                                                      '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)')
team_info_by_fs['Bayern'] = FlashScoreTeamParse('FC Bayern Munich', 'Bayern Munich', '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)',
                                                '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)')
team_info_by_fs['Barcelona'] = FlashScoreTeamParse('FC Barcelona', 'Barcelona', '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)',
                                                   '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)')
team_info_by_fs['Olympiacos'] = FlashScoreTeamParse('Olympiacos Piraeus', 'Olympiacos', '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)',
                                                    '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)')
team_info_by_fs['Khimki M.'] = FlashScoreTeamParse('Khimki Moscow Region', 'Khimki', '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)',
                                                   '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)')
team_info_by_fs['Maccabi Tel Aviv'] = FlashScoreTeamParse('Maccabi FOX Tel Aviv', 'Maccabi Tel Aviv', '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)',
                                                          '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)')
team_info_by_fs['Zalgiris Kaunas'] = FlashScoreTeamParse('Zalgiris Kaunas', 'Zalgiris Kaunas', '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)',
                                                         '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)')
team_info_by_fs['Baskonia'] = FlashScoreTeamParse('KIROLBET Baskonia Vitoria-Gasteiz', 'Saski Baskonia', '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)',
                                                  '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)')
team_info_by_fs['Real Madrid'] = FlashScoreTeamParse('Real Madrid', 'Real Madrid', '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)',
                                                     '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)')
team_info_by_fs['Olimpia Milano'] = FlashScoreTeamParse('AX Armani Exchange Milan', 'Olimpia Milano', '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)',
                                                        '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)')
team_info_by_fs['Panathinaikos'] = FlashScoreTeamParse('Panathinaikos OPAP Athens', 'Panathinaikos', '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)',
                                                       '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)')
team_info_by_fs['Lyon-Villeurbanne'] = FlashScoreTeamParse('LDLC ASVEL Villeurbanne', 'ASVEL', '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)',
                                                           '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)')
team_info_by_fs['Alba Berlin'] = FlashScoreTeamParse('ALBA Berlin', 'Alba Berlin', '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)',
                                                     '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)')
team_info_by_fs['Valencia'] = FlashScoreTeamParse('Valencia Basket', 'Valencia', '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)',
                                                  '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)')
team_info_by_fs['Crvena zvezda mts'] = FlashScoreTeamParse('Crvena Zvezda mts Belgrade', 'Crvena Zvezda', '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)',
                                                           '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)')
team_info_by_fs['Zenit Petersburg'] = FlashScoreTeamParse('Zenit St Petersburg', 'Zenit', '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)',
                                                          '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)')

# Eurocup teams
team_info_by_fs['Tofas'] = FlashScoreTeamParse('Tofas Bursa', 'Tofas', '[TOF](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)',
                                               '[Tofas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)')
team_info_by_fs['Darussafaka'] = FlashScoreTeamParse('Darussafaka Tekfen Istanbul', 'Darussafaka', '[DTI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)',
                                                     '[Darussafaka](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)')
team_info_by_fs['Buducnost'] = FlashScoreTeamParse('Buducnost VOLI Podgorica', 'Buducnost', '[BUD](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)',
                                                   '[Buducnost](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)')
team_info_by_fs['Promitheas'] = FlashScoreTeamParse('Promitheas Patras', 'Promitheas Patras', '[PRO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)',
                                                    '[Promitheas Patras](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)')
team_info_by_fs['Monaco'] = FlashScoreTeamParse('AS Monaco', 'AS Monaco', '[MON](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)',
                                                '[AS Monaco](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)')
team_info_by_fs['MoraBanc Andorra'] = FlashScoreTeamParse('MoraBanc Andorra', 'BC Andorra', '[MBA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)',
                                                          '[BC Andorra](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)')
team_info_by_fs['Ulm'] = FlashScoreTeamParse('ratiopharm Ulm', 'ratiopharm Ulm', '[ULM](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)',
                                             '[ratiopharm Ulm](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)')
team_info_by_fs['Virtus Bologna'] = FlashScoreTeamParse('Segafredo Virtus Bologna', 'Virtus Bologna', '[VIR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)',
                                                        '[Virtus Bologna](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)')
team_info_by_fs['Maccabi Rishon'] = FlashScoreTeamParse('Maccabi Rishon LeZion', 'Maccabi Rishon LeZion', '[RLZ](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)',
                                                        '[Maccabi Rishon LeZion](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)')
team_info_by_fs['Partizan'] = FlashScoreTeamParse('Partizan NIS Belgrade', 'Partizan', '[PAR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)',
                                                  '[Partizan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)')
team_info_by_fs['Lokomotiv Kuban'] = FlashScoreTeamParse('Lokomotiv Kuban Krasnodar', 'Lokomotiv Kuban', '[LOK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)',
                                                         '[Lokomotiv Kuban](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)')
team_info_by_fs['Venezia'] = FlashScoreTeamParse('Umana Reyer Venice', 'Reyer Venezia', '[URV](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)',
                                                 '[Reyer Venezia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)')
team_info_by_fs['Limoges'] = FlashScoreTeamParse('Limoges CSP', 'Limoges CSP', '[CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)',
                                                 '[Limoges CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)')
team_info_by_fs['Rytas'] = FlashScoreTeamParse('Rytas Vilnius', 'Rytas', '[RYT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)',
                                               '[Rytas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)')
team_info_by_fs['Nanterre'] = FlashScoreTeamParse('Nanterre 92', 'Nanterre 92', '[NTR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)',
                                                  '[Nanterre 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)')
team_info_by_fs['Joventut Badalona'] = FlashScoreTeamParse('Joventut Badalona', 'Joventut Badalona', '[CJB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)',
                                                           '[Joventut Badalona](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)')
team_info_by_fs['Brescia'] = FlashScoreTeamParse('Germani Brescia Leonessa', 'Brescia Leonessa', '[BRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)',
                                                 '[Brescia Leonessa](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)')
team_info_by_fs['Unics Kazan'] = FlashScoreTeamParse('UNICS Kazan', 'UNICS Kazan', '[UNK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)',
                                                     '[UNICS Kazan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)')
team_info_by_fs['Cedevita Olimpija'] = FlashScoreTeamParse('Cedevita Olimpija Ljubljana', 'Cedevita Olimpija Ljubljana', '[COL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)',
                                                           '[Cedevita Olimpija Ljubljana](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)')
team_info_by_fs['Galatasaray'] = FlashScoreTeamParse('Galatasaray Doga Sigorta Istanbul', 'Galatasaray', '[GAL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)',
                                                     '[Galatasaray](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)')
team_info_by_fs['Oldenburg'] = FlashScoreTeamParse('EWE Baskets Oldenburg', 'EWE Baskets Oldenburg', '[EBO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)',
                                                   '[EWE Baskets Oldenburg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)')
team_info_by_fs['Gdynia'] = FlashScoreTeamParse('Asseco Arka Gdynia', 'Arka Gdynia', '[ARK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)',
                                                '[Arka Gdynia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)')
team_info_by_fs['Unicaja'] = FlashScoreTeamParse('Unicaja Malaga', 'Unicaja Malaga', '[UNI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)',
                                                 '[Unicaja Malaga](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)')
team_info_by_fs['Trento'] = FlashScoreTeamParse('Dolomiti Energia Trento', 'Aquila Basket Trento', '[TRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)',
                                                '[Aquila Basket Trento](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)')

team_info_by_official = dict()
OfficialTeamParse = namedtuple(
    'OfficialTeamParse', 'reddit letter3_md full_md')

team_info_by_official['CSKA Moscow'] = OfficialTeamParse('CSKA Moscow', '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)',
                                                         '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)')
team_info_by_official['Fenerbahce Beko Istanbul'] = OfficialTeamParse(
    'Fenerbahce', '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)', '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)')
team_info_by_official['Anadolu Efes Istanbul'] = OfficialTeamParse(
    'Anadolu Efes', '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)', '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)')
team_info_by_official['FC Bayern Munich'] = OfficialTeamParse('Bayern Munich', '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)',
                                                              '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)')
team_info_by_official['FC Barcelona'] = OfficialTeamParse('Barcelona', '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)',
                                                          '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)')
team_info_by_official['Olympiacos Piraeus'] = OfficialTeamParse('Olympiacos', '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)',
                                                                '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)')
team_info_by_official['Khimki Moscow Region'] = OfficialTeamParse(
    'Khimki', '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)', '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)')
team_info_by_official['Maccabi FOX Tel Aviv'] = OfficialTeamParse('Maccabi Tel Aviv', '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)',
                                                                  '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)')
team_info_by_official['Zalgiris Kaunas'] = OfficialTeamParse('Zalgiris Kaunas', '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)',
                                                             '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)')
team_info_by_official['KIROLBET Baskonia Vitoria-Gasteiz'] = OfficialTeamParse('Saski Baskonia', '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)',
                                                                               '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)')
team_info_by_official['Real Madrid'] = OfficialTeamParse('Real Madrid', '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)',
                                                         '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)')
team_info_by_official['AX Armani Exchange Milan'] = OfficialTeamParse(
    'Olimpia Milano', '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)', '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)')
team_info_by_official['Panathinaikos OPAP Athens'] = OfficialTeamParse(
    'Panathinaikos', '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)', '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)')
team_info_by_official['LDLC ASVEL Villeurbanne'] = OfficialTeamParse(
    'ASVEL', '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)', '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)')
team_info_by_official['ALBA Berlin'] = OfficialTeamParse('Alba Berlin', '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)',
                                                         '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)')
team_info_by_official['Valencia Basket'] = OfficialTeamParse('Valencia', '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)',
                                                             '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)')
team_info_by_official['Crvena Zvezda mts Belgrade'] = OfficialTeamParse(
    'Crvena Zvezda', '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)', '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)')
team_info_by_official['Zenit St Petersburg'] = OfficialTeamParse(
    'Zenit', '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)', '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)')

# Eurocup teams
team_info_by_official['Tofas Bursa'] = OfficialTeamParse('Tofas', '[TOF](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)',
                                                         '[Tofas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)')
team_info_by_official['Darussafaka Tekfen Istanbul'] = OfficialTeamParse('Darussafaka', '[DTI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)',
                                                                         '[Darussafaka](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)')
team_info_by_official['Buducnost VOLI Podgorica'] = OfficialTeamParse('Buducnost', '[BUD](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)',
                                                                      '[Buducnost](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)')
team_info_by_official['Promitheas Patras'] = OfficialTeamParse('Promitheas Patras', '[PRO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)',
                                                               '[Promitheas Patras](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)')
team_info_by_official['AS Monaco'] = OfficialTeamParse('AS Monaco', '[MON](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)',
                                                       '[AS Monaco](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)')
team_info_by_official['MoraBanc Andorra'] = OfficialTeamParse('BC Andorra', '[MBA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)',
                                                              '[BC Andorra](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)')
team_info_by_official['ratiopharm Ulm'] = OfficialTeamParse('ratiopharm Ulm', '[ULM](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)',
                                                            '[ratiopharm Ulm](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)')
team_info_by_official['Segafredo Virtus Bologna'] = OfficialTeamParse('Virtus Bologna', '[VIR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)',
                                                                      '[Virtus Bologna](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)')
team_info_by_official['Maccabi Rishon LeZion'] = OfficialTeamParse('Maccabi Rishon LeZion', '[RLZ](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)',
                                                                   '[Maccabi Rishon LeZion](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)')
team_info_by_official['Partizan NIS Belgrade'] = OfficialTeamParse('Partizan', '[PAR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)',
                                                                   '[Partizan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)')
team_info_by_official['Lokomotiv Kuban Krasnodar'] = OfficialTeamParse('Lokomotiv Kuban', '[LOK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)',
                                                                       '[Lokomotiv Kuban](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)')
team_info_by_official['Umana Reyer Venice'] = OfficialTeamParse('Reyer Venezia', '[URV](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)',
                                                                '[Reyer Venezia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)')
team_info_by_official['Limoges CSP'] = OfficialTeamParse('Limoges CSP', '[CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)',
                                                         '[Limoges CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)')
team_info_by_official['Rytas Vilnius'] = OfficialTeamParse('Rytas', '[RYT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)',
                                                           '[Rytas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)')
team_info_by_official['Nanterre 92'] = OfficialTeamParse('Nanterre 92', '[NTR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)',
                                                         '[Nanterre 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)')
team_info_by_official['Joventut Badalona'] = OfficialTeamParse('Joventut Badalona', '[CJB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)',
                                                               '[Joventut Badalona](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)')
team_info_by_official['Germani Brescia Leonessa'] = OfficialTeamParse('Brescia Leonessa', '[BRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)',
                                                                      '[Brescia Leonessa](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)')
team_info_by_official['UNICS Kazan'] = OfficialTeamParse('UNICS Kazan', '[UNK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)',
                                                         '[UNICS Kazan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)')
team_info_by_official['Cedevita Olimpija Ljubljana'] = OfficialTeamParse('Cedevita Olimpija Ljubljana', '[COL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)',
                                                                         '[Cedevita Olimpija Ljubljana](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)')
team_info_by_official['Galatasaray Doga Sigorta Istanbul'] = OfficialTeamParse(
    'Galatasaray', '[GAL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)', '[Galatasaray](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)')
team_info_by_official['EWE Baskets Oldenburg'] = OfficialTeamParse('EWE Baskets Oldenburg', '[EBO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)',
                                                                   '[EWE Baskets Oldenburg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)')
team_info_by_official['Asseco Arka Gdyni'] = OfficialTeamParse('Arka Gdynia', '[ARK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)',
                                                               '[Arka Gdynia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)')
team_info_by_official['Unicaja Malaga'] = OfficialTeamParse('Unicaja Malaga', '[UNI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)',
                                                            '[Unicaja Malaga](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)')
team_info_by_official['Dolomiti Energia Trento'] = OfficialTeamParse('Aquila Basket Trento', '[TRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)',
                                                                     '[Aquila Basket Trento](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)')
