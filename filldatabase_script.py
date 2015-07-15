from stats import *
from riotApi import *
from filler import Filler
from database import *
import time
import logging
import logging.handlers


api = RiotApi('70f53e5d-eea1-46f0-9e8a-19889489902f')
logger = logging.getLogger('leaguestats')
logger.setLevel(logging.INFO)
timed_log = logging.handlers.TimedRotatingFileHandler('fill.log', when='W0', interval=4)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
timed_log.setFormatter(formatter)
logger.addHandler(timed_log)
# Grabs challenger 5v5 teams
dataC = api.getchallenger()

# Outer loop running through all challenger teams (dataM)
def fill_it_up():
    filler = Filler()
    start = time.time()
    x = 0
    for g in dataC['entries']:
        y = 0
        dataT = api.getteam(g['playerOrTeamName'])
        # Grabs all games form a team (dataT)
        for j in dataT['matchHistory']:
            match = filler.session.query(MatchDetail).\
                filter(MatchDetail.matchId == j['gameId']).first()
            if match is not None:
                continue
            try:
                dataM = api.getmatch(g['playerOrTeamName'], str(j['gameId']))
            except:
                logger.exception('Exception while calling getmatch')
                continue
            statgetter = GetStats(dataM)
            realdata = statgetter.returnMatchDetail()
            filler.add_match(realdata)
            print(time.time() - start)
            logger.info('Successfully added team \"%s\"s match %s', g['playerOrTeamName'], str(j['gameId']))
            x += 1
        logger.info('Finished adding all matches for team %s', g['playerOrTeamName'])

fill_it_up()
# json_obj = get_single_json()

# for x in json_objs:
#     filler.add_match(x)
#     print(time.time() - start)
