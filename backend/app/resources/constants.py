import enum

class DrDataSourceName(enum.Enum):
    incident = 'incident'
    daily_work = 'daily_work'

class DrDataSourceKeyName(enum.Enum):
    incident = 'incident_new_version'
    incident_trend_sr_with_note_summary = 'incident'
    installed_base = 'installed_base'
    daily_work = 'daily_work'#daily_work_new
    asset_life_event = 'asset_life_event'
    asset_conditions_events = 'asset_conditions_events'
    field_ops_form_data = 'fops'
    parts = 'parts_new_version'

class Constants(enum.Enum):
    oldest_date_for_data = '2000-01-01'


class EkrypAPI(enum.Enum):
    token_get_url = 'https://ekryp.auth0.com/oauth/token'
    grant_type = 'client_credentials'
    content_type = 'application/json'
