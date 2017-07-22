'''
The Blue ALliance API
Version = 3.0
'''

import json
import requests
import re
import datetime


PREFIX = 'https://www.thebluealliance.com/api/v3/%s'
auth_key = ''

def _fetch(url):
	return json.loads(requests.get(PREFIX % url, headers={'X-TBA-Auth-Key': auth_key}).text)

class API_Status:
	'''
	:rtype: API_Status object.
	'''
	def __init__(self):

		d = _fetch('status')
		self.current_season = d['current_season']
		self.max_season = d['max_season']
		self.is_datafeed_down = d['is_datafeed_down']
		self.down_events = d['down_events']
		self.ios = API_Status_App_Version(d['ios'])
		self.android = API_Status_App_Version(d['android'])

class API_Status_App_Version:
	'''
	:param d: The value from the API_Status object.
	:type d: dictionary
	:rtype: API_Status_App_Version object.
	'''
	
	def __init__(self, d=None):
		if d:
			self.min_app_version = d['min_app_version']
			self.latest_app_version = d['latest_app_version']
		else:
			raise NoParametersException()

class Team_Simple:
	'''
	:param team_key: Team key with the format `frcXXXX` with `XXXX` representing the team number.
	:type team_key: string
	:rtype: Team_Simple object.
	'''
	def __init__(self, team_key):
		team_key = validate_team_key(team_key)
		d = _fetch('team/%s/simple' % team_key)
		self.key = d['key']
		self.team_number = d['team_number']
		self.nickname = d['nickname']
		self.name = d['name']
		self.city = d['city']
		self.state_prov = d['state_prov']
		self.country = d['country']

class Team:
	'''
	:param team_key: Team key with the format `frcXXXX` with `XXXX` representing the team number.
	:type team_key: string
	:param d: Dictionary value used from other function calls
	:type d: dict
	:rtype: Team object.
	'''
	def __init__(self, team_key=None, d=None):
		
		if team_key:
			team_key = validate_team_key(team_key)
			d = _fetch('team/%s' % team_key)
		self.key = d['key']
		self.team_number = d['team_number']
		self.nickname = d['nickname']
		self.name = d['name']
		self.city = d['city']
		self.state_prov = d['state_prov']
		self.country = d['country']
		self.address = d['address']
		self.postal_code = d['postal_code']
		self.gmaps_place_id = d['gmaps_place_id']
		self.gmaps_url = d['gmaps_url']
		self.lat = d['lat']
		self.lng = d['lng']
		self.location_name = d['location_name']
		self.website = d['website']
		self.rookie_year = d['rookie_year']
		self.motto = d['motto']
		self.home_championship = d['home_championship']

	@property
	def years_participated(self):
		d = _fetch('team/%s/years_participated' % self.key)
		return d

	@property
	def districts(self):
		d = _fetch('team/%s/districts' % self.key)
		return d

	@property
	def robots(self):
		d = _fetch('team/%s/robots' % self.key)
		return [Team_Robot(d=robot) for robot in d]

	@property
	def events(self):
		d = _fetch('team/%s/events' % self.key)
		return [Event(d=event) for event in d]

	@property
	def events_simple(self):
		d = _fetch('team/%s/events/simple' % self.key)
		return [Event_Simple(d=event) for event in d]

	@property
	def events_keys(self):
		d = _fetch('team/%s/events/keys' % self.key)
		return d

	def events_year(self, year):
		d = _fetch('team/%s/events/%s' % (self.key, str(year)))
		return [Event(d=event) for event in d]

	def events_year_simple(self, year):
		d = _fetch('team/%s/events/%s/simple' % (self.key, str(year)))
		return [Event_Simple(d=event) for event in d]

	def events_year_keys(self, year):
		d = _fetch('team/%s/events/%s/keys' % (self.key, str(year)))
		return d

	def event_matches(self, event_key):
		event_key = validate_event_key(event_key)
		d = _fetch('team/%s/event/%s/matches' % (self.key, event_key))
		return [Match(d=match) for match in d]

	def event_matches_simple(self, event_key):
		event_key = validate_event_key(event_key)
		d = _fetch('team/%s/event/%s/matches/simple' % (self.key, event_key))
		return [Match_Simple(d=match) for match in d]

	def event_matches_keys(self, event_key):
		event_key = validate_event_key(event_key)
		d = _fetch('team/%s/event/%s/matches/keys' % (self.key, event_key))
		return d

	def event_awards(self, event_key):
		event_key = validate_event_key(event_key)
		d = _fetch('team/%s/event/%s/awards' % (self.key, event_key))
		return [Award(d=award) for award in d]

	def event_status(self, event_key):
		event_key = validate_event_key(event_key)
		d = _fetch('team/%s/event/%s/awards' % (self.key, event_key))
		return Event_Status(d=d)

	@property
	def awards(self):
		d = _fetch('team/%s/awards' % self.key)
		return [Award(d=award) for awards in d]

	def awards_year(self, year):
		d = _fetch('team/%s/awards/%s' % (self.key, str(year)))
		return [Award(d=award) for awards in d]

	def matches_year(self, year):
		d = _fetch('team/%s/matches/%s' % (self.key, str(year)))
		return [Match(d=match) for match in d]

	def matches_year_simple(self, year):
		d = _fetch('team/%s/matches/%s/simple' % (self.key, str(year)))
		return [Match_Simple(d=match) for match in d]

	def matches_year_keys(self, year):
		d = _fetch('team/%s/matches/%s/keys' % (self.key, str(year)))
		return d

	def media_year(self, year):
		d = _fetch('team/%s/media/%s' % (self.key, str(year)))
		return [Media(d=media) for media in d]

	@property
	def social_media(self):
		d = _fetch('team/%s/social_media')
		return [Social_Media(d=social) for social in d]

class Team_Robot:
	'''
	:param d: The dictionary constructor for the robot
	:type d: dictionary
	:rtype: Team_Robot object
	'''
	def __init__(self, d=None):
		if d:
			self.year = d['year']
			self.robot_name = d['robot_name']
			self.key = d['key']
			self.team_key = d['team_key']
		else:
			raise NoParametersException()

class Event_Simple:
	'''
	:param event_key: Event key with the format yyyy[EVENT_CODE], where yyyy is the year, and EVENT_CODE is the event code of the event.
	:type event_key: string
	:param d: Dictionary value used from other function calls
	:type d: dict
	:rtype: Event_Simple object.
	'''
	def __init__(self, event_key=None, d=None):
		if event_key:
			event_key = validate_event_key(event_key)
			d = _fetch('event/%s/simple' % event_key)
		self.key = d['key']
		self.name = d['name']
		self.event_code = d['event_code']
		self.event_type = d['event_type']
		self.district = d['district']
		self.city = d['city']
		self.state_prov = d['state_prov']
		self.country = d['country']
		self.start_date = d['start_date']
		self.end_date = d['end_date']
		self.year = d['year']

class Event:
	'''
	:param event_key: Event key with the format yyyy[EVENT_CODE], where yyyy is the year, and EVENT_CODE is the event code of the event.
	:type event_key: string
	:param d: Dictionary value used from other function calls
	:type d: dict
	:rtype: Event object.
	'''
	def __init__(self, event_key=None, d=None):
		if event_key:
			event_key = validate_event_key(event_key)
			d = _fetch('event/%s' % event_key)
		self.key = d['key']
		self.name = d['name']
		self.event_code = d['event_code']
		self.event_type = d['event_type']
		self.district = d['district']
		self.city = d['city']
		self.state_prov = d['state_prov']
		self.country = d['country']
		self.start_date = d['start_date']
		self.end_date = d['end_date']
		self.year = d['year']
		self.short_name = d['short_name']
		self.event_type_string = d['event_type_string']
		self.week = d['week']
		self.address = d['address']
		self.postal_code = d['postal_code']
		self.gmaps_place_id = d['gmaps_place_id']
		self.gmaps_url = d['gmaps_url']
		self.lat = d['lat']
		self.lng = d['lng']
		self.location_name = d['location_name']
		self.timezone = d['timezone']
		self.website = d['website']
		self.first_event_id = d['first_event_id']
		self.webcasts = d['webcasts']
		self.division_keys = d['division_keys']
		self.parent_event_key = d['parent_event_key']
		self.playoff_type = d['playoff_type']
		self.playoff_type_string = d['playoff_type_string']

		@property
		def alliances(self):
			d = _fetch('event/%s/alliances' % self.key)
			return d

		@property
		def insights(self):
			d = _fetch('event/%s/insights' % self.key)
			return Event_Insights_2017(d=d)

		@property
		def oprs(self):
			d = _fetch('event/%s/oprs' % self.key)
			return d

		@property
		def predictions(self):
			d = _fetch('event/%s/predictions' % self.key)
			return d

		@property
		def rankings(self):
			d = _fetch('event/%s/rankings' % self.key)
			return [Event_Ranking(d=ranking) for ranking in d]

		@property
		def district_points(self):
			d = _fetch('event/%s/district_points' % self.key)
			return [Event_District_Points(d=points) for points in d]

		@property
		def teams(self):
			d = _fetch('event/%s/teams' % self.key)
			return [Team(d=team) for team in d]

		@property
		def teams_simple(self):
			d = _fetch('event/%s/teams/simple' % self.key)
			return [Team_Simple(d=team) for team in d]

		@property
		def teams_keys(self):
			d = _fetch('event/%s/teams' % self.key)
			return d

		@property
		def matches(self):
			d = _fetch('event/%s/matches' % self.key)
			return [Match(d=match) for match in d]

		@property
		def matches(self):
			d = _fetch('event/%s/matches/simple' % self.key)
			return [Match_Simple(d=match) for match in d]

		@property
		def matches_keys(self):
			d = _fetch('event/%s/matches/keys' % self.key)
			return d

		def awards(self):
			d = _fetch('event/%s/awards' % self.key)
			return [Award(d=award) for award in d]

class Team_Event_Status:
	'''
	:param d: The value retrieved from the Team object
	:type d: dictionary
	:rtype: Team_Event_Status object
	'''
	def __init__(self, d=None):
		if d:
			self.qual = Team_Event_status_rank(d=d['qual'])
			self.alliance = Team_Event_status_alliance(d=d['alliance'])
			self.playoff = Team_Event_status_playoff(d=d['playoff'])
			self.alliance_status_str = d['alliance_status_str']
			self.playoff_status_str = d['playoff_status_str']
			self.overall_status_str = d['overall_status_str']
		else:
			raise NoParametersException()

class Team_Event_Status_rank:
	def __init__(self, d=None):
		if d:
			self.num_teams = d['num_teams']
			self.ranking = d['ranking']
			self.sort_order_info = d['sort_order_info']
			self.status = d['status']
		else:
			raise NoParametersException()

class Team_Event_Status_alliance:
	def __init__(self, d=None):
		if d:
			self.name = d['name']
			self.number = d['number']
			self.backup = Team_Event_Status_alliance_backup(d=d)
			self.pick = d['pick']
		else:
			raise NoParametersException()

class Team_Event_Status_alliance_backup:
	def __init__(self, d=None):
		if d:
			self.out = d['out']
			self.in_team = d['in']
		else:
			raise NoParametersException()

class Team_Event_Status_playoff:
	def __init__(self, d=None):
		if d:
			self.level = d['level']
			self.record = d['record']
			self.status = d['status']
		else:
			raise NoParametersException()

class Event_Ranking:
	def __init__(self, d=None):
		if d:
			self.rankings = d['rankings']
			self.sort_order_info = d['sort_order_info']
		else:
			raise NoParametersException()

class Event_District_Points:
	def __init__(self, d=None):
		if d:
			self.points = d['points']
			self.tiebreakers = d['tiebreakers']
		else:
			raise NoParametersException()

class Event_Insights_2016:
	def __init__(self, d=None):
		if d:
			self.qual = Event_Insights_2016_Detail(d=d)
			self.playoff = Event_Insights_2016_Detail(d=d)
		else:
			raise NoParametersException()

class Event_Insights_2016_Detail:
	def __init__(self, d=None):
		if d:
			self.LowBar = d['LowBar']
			self.A_ChevalDeFrise = d['A_ChevalDeFrise']
			self.A_Portcullis = d['A_Portcullis']
			self.B_Ramparts = d['B_Ramparts']
			self.B_Moat = d['B_Moat']
			self.C_SallyPort = d['C_SallyPort']
			self.C_Drawbridge = d['C_Drawbridge']
			self.D_RoughTerrain = d['D_RoughTerrain']
			self.D_RockWall = d['D_RockWall']
			self.average_high_goals = d['average_high_goals']
			self.average_low_goals = d['average_low_goals']
			self.breaches = d['breaches']
			self.challenges = d['challenges']
			self.captures = d['captures']
			self.average_win_score = d['average_win_score']
			self.average_win_margin = d['average_win_margin']
			self.average_score = d['average_score']
			self.average_auto_score = d['average_auto_score']
			self.average_crossing_score = d['average_crossing_score']
			self.average_boulder_score = d['average_boulder_score']
			self.average_tower_score = d['average_tower_score']
			self.average_foul_score = d['average_foul_score']
			self.high_score = d['high_score']

		else:
			raise NoParametersException()

class Event_Insights_2017:
	def __init__(self, d=None):
		if d:
			self.qual = Event_Insights_2017_Detail(d=d)
			self.playoff = Event_Insights_2017_Detail(d=d)
		else:
			raise NoParametersException()

class Event_Insights_2017_Detail:
	def __init__(self, d=None):
		if d:
			self.average_foul_score = d['average_foul_score']
			self.average_fuel_points = d['average_fuel_points']
			self.average_fuel_points_auto = d['average_fuel_points_auto']
			self.average_fuel_points_teleop = d['average_fuel_points_teleop']
			self.average_high_goals_auto = d['average_high_goals_auto']
			self.average_high_goals_teleop = d['average_high_goals_teleop']
			self.average_low_goals = d['average_low_goals']
			self.average_low_goals_auto = d['average_low_goals_auto']
			self.average_low_goals_teleop = d['average_low_goals_teleop']
			self.average_mobility_points_auto = d['average_mobility_points_auto']
			self.average_points_auto = d['average_points_auto']
			self.average_points_teleop = d['average_points_teleop']
			self.average_rotor_points = d['average_rotor_points']
			self.average_rotor_points_auto = d['average_rotor_points_auto']
			self.average_rotor_points_teleop = d['average_rotor_points_teleop']
			self.average_score = d['average_score']
			self.average_takeoff_points_teleop = d['average_takeoff_points_teleop']
			self.average_win_margin = d['average_win_margin']
			self.average_win_score = d['average_win_score']
			self.high_kpa = d['high_kpa']
			self.high_score = d['high_score']
			self.kpa_achieved = d['kpa_achieved']
			self.mobility_counts = d['mobility_counts']
			self.rotor_1_engaged = d['rotor_1_engaged']
			self.rotor_1_engaged_auto = d['rotor_1_engaged_auto']
			self.rotor_2_engaged = d['rotor_2_engaged']
			self.rotor_2_engaged_auto = d['rotor_2_engaged_auto']
			self.rotor_3_engaged = d['rotor_3_engaged']
			self.rotor_4_engaged = d['rotor_4_engaged']
			self.takeoff_counts = d['takeoff_counts']		

		else:
			raise NoParametersException()

class Event_OPRs:
	def __init__(self, d=None):
		if d:
			self.oprs = d['oprs']
			self.dprs = d['dprs']
			self.ccwms = d['ccwms']
		else:
			raise NoParametersException()

class Event_Predictions:
	def __init__(self):
		pass

class Webcast:
	def __init__(self, d=None):
		if d:
			self.type = d['type']
			self.channel = d['channel']
			self.file = d['file']
		else:
			raise NoParametersException()

class Match_Simple:
	def __init__(self, match_key=None, d=None):
		'''
		:param match_key: Match Key, eg 2016nytr_qm1
		:type event_key: string
		:param d: Dictionary value used from other function calls
		:type d: dict
		:rtype: Match_Simple object.
		'''
		if match_key:
			match_key = validate_match_key(match_key)
			d = _fetch('match/%s/simple' % match_key)
		self.key = d['key']
		self.comp_level = d['comp_level']
		self.set_number = d['set_number']
		self.match_number = d['match_number']
		self.alliances = d['alliances']
		self.winning_alliance = d['winning_alliance']
		self.event_key = d['event_key']
		self.time = d['time']
		self.predicted_time = d['predicted_time']
		self.actual_time = d['key']

class Match:
	def __init__(self, match_key=None, d=None):
		'''
		:param match_key: Match Key, eg 2016nytr_qm1
		:type event_key: string
		:param d: Dictionary value used from other function calls
		:type d: dict
		:rtype: Match object.
		'''
		if match_key:
			match_key = validate_match_key(match_key)
			d = _fetch('match/%s' % match_key)
		self.key = d['key']
		self.comp_level = d['comp_level']
		self.set_number = d['set_number']
		self.match_number = d['match_number']
		self.alliances = d['alliances']
		self.winning_alliance = d['winning_alliance']
		self.event_key = d['event_key']
		self.time = d['time']
		self.predicted_time = d['predicted_time']
		self.actual_time = d['actual_time']	
		self.post_result_time = d['post_result_time']	
		self.score_breakdown = d['score_breakdown']	
		self.videos = Media(d=d['videos'])	

class Match_Alliance:
	def __init__(self, d=None):
		if d:
			self.score = d['score']
			self.team_keys = d['team_keys']
			self.surrogate_team_keys = d['surrogate_team_keys']
		else:
			raise NoParametersException()

class Media:
	def __init__(self, d=None):
		if d:
			self.key = d['key']
			self.type = d['type']
			self.foreign_key = d['foreign_key']
			self.details = d['details']
			self.preferred = d['preferred']

class Elimination_Alliance:
	def __init__(self, d=None):
		if d:
			self.name = d['name']
			self.backup = d['backup']
			self.declines = d['declines']
			self.picks = d['picks']
			self.status = d['status']
		else:
			raise NoParametersException()

class Award:
	def __init__(self, d=None):
		if d:
			self.name = d['name']
			self.award_type = d['award_type']
			self.event_key = d['event_key']
			self.recipient_list = [Award_Recipient(d=recipient) for recipient in d['recipient_list']]
			self.year = d['year']
		else:
			raise NoParametersException()

class Award_Recipient:
	def __init__(self, d=None):
		if d:
			self.team_key = d['team_key']
			self.awardee = d['awardee']
		else:
			raise NoParametersException()

class District_List:
	def __init__(self, d=None):
		if d:
			self.abbreviation = d['abbreviation']
			self.display_name = d['display_name']
			self.key = d['key']
			self.year = d['year']
		else:
			raise NoParametersException()

class District_Ranking:
	def __init__(self, d=None):
		if d:
			self.team_key = d['team_key']
			self.rank = d['rank']
			self.rookie_bonus = d['rookie_bonus']
			self.point_total = d['point_total']
			self.event_points = d['event_points']
		else:
			raise NoParametersException()

class WLT_Record:
	def __init__(self, d=None):
		if d:
			self.losses = d['losses']
			self.wins = d['wins']
			self.ties = d['ties']
		else:
			raise NoParametersException()


def validate_team_key(team_key):
	team_key = str(team_key)
	if re.search('^frc\d{1,4}$', team_key):
		return team_key
	elif re.search('^\d{1,4}$', team_key):
		return 'frc%s' % team_key
	else:
		raise InvalidTeamKeyException(team_key, '%s isn\'t a valid key to use for a team.' % team_key)

def validate_event_key(event_key):
	event_key = str(event_key)
	if re.search('^\d{4}\w{1,}$', event_key):
		return event_key
	elif re.search('^\w{1,}$', event_key):
		return '%s%s' % (str(datetime.date.today().year), event_key)
	else:
		raise InvalidEventKeyException(event_key, '%s isn\'t a valid key to use for an event.' % event_key)

def validate_match_key(match_key):
	match_key = str(match_key)
	if re.search('^\d{4}\w{1,}_\w{1,2}\d{1,3}$', match_key):
		return match_key
	elif re.search('^\w{1,}_\w{1,2}\d{1,3}$', match_key):
		return '%s%s' % (str(datetime.date.today().year), match_key)
	else:
		raise InvalidMatchKeyException(match_key, '%s isn\'t a valid key to use for a match.' % event_key)

class InvalidTeamKeyException(Exception):
	def __init__(self, key, message):
		self.key = key
		self.message = message

class InvalidEventKeyException(Exception):
	def __init__(self, key, message):
		self.key = key
		self.message = message

class InvalidMatchKeyException(Exception):
	def __init__(self, key, message):
		self.key = key
		self.message = message

class NoParametersException(Exception):
	def __init__(self):
		self.message = 'There aren\'t enough parameters to create this class'