import calendar
from jubatus.recommender.client import recommender
from jubatus.recommender.types import *

typhoon_client = recommender('127.0.0.1', 9199)
harvest_client = recommender('127.0.0.1', 9299)

method = "inverted_index"
converter = """
  {
    \"string_filter_types\" : {},
    \"string_filter_rules\" : [],
    \"num_filter_types\" : {},
    \"num_filter_rules\" : [],
    \"string_types\" : {},
    \"string_rules\" : [],
    \"num_types\" : {},
    \"num_rules\" : [
      {
        \"key\" : \"*\",
        \"type\" : \"num\"
      }
    ]
  }
"""
config = config_data(method, converter)

# train -- typhoon
typhoon_client.set_config('', config)
typhoon_years = []

with open('typhoon.csv', 'r') as typhoons:
  for typhoon in typhoons:

    # skip comments
    if not len(typhoon) or typhoon.startswith('#'): continue

    data = map(str.strip, typhoon.strip().split(','))

    num_values = []
    for month, str_month in enumerate(calendar.month_abbr):
      if month == 0: continue
      count = 0.0 if not len(data[month]) else float(data[month])
      num_values.append((str_month, count))

    d = datum([], num_values)
    typhoon_client.update_row('', data[0], d)
    typhoon_years.append(data[0])

# train -- harvest
harvest_client.set_config('', config)
harvest_years = []

with open('harvest.csv', 'r') as harvests:
  for harvest in harvests:

    # skip comments
    if not len(harvest) or harvest.startswith('#'): continue

    year, rice, orange = map(str.strip, harvest.strip().split(','))

    num_values = [
      ('rice', float(rice)),
      ('orange', float(orange)),
    ]

    d = datum([], num_values)
    harvest_client.update_row('', year, d)
    harvest_years.append(year)

# analyze
years = list(set(typhoon_years) & set(harvest_years))
years.sort()

for year in years:

  print '%s:' % (year)

  t_rows = typhoon_client.similar_row_from_id('', year, len(years))
  for t_row in t_rows:
    t_similar_year = t_row[0]
    if t_similar_year != year and t_similar_year in years: break

  print '  typhoon) %s is similar to %s' % (year, t_similar_year)

  h_rows = harvest_client.similar_row_from_id('', year, 4)
  h_similar_years = []
  for h_row in h_rows[1:]:
    if h_row[0] != year and h_row[0] in years:
      h_similar_years.append(h_row[0])

  if t_similar_year in h_similar_years:
    print '  harvest) %s is similar to %s too\n' % (year, t_similar_year)
  else:
    print '  harvest) %s is not similar to %s\n' % (year, t_similar_year)
