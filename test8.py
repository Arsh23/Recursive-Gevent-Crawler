from gevent import monkey
monkey.patch_all()

import requests
from gevent import pool
from lxml import html

import gevent
jobs = []
urls2 = []
# links = []
p = pool.Pool(32)

s = requests.Session()


urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']#,'https://en.wikipedia.org/wiki/Space_exploration']
# 'https://en.wikipedia.org/wiki/Colonisation_of_Africa',
# 'https://en.wikipedia.org/wiki/Western_imperialism_in_Asia',
# 'https://en.wikipedia.org/wiki/Colonisation_of_Oceania',
# 'https://en.wikipedia.org/wiki/Colonization_of_Antarctica',
# 'https://en.wikipedia.org/wiki/Ocean_colonization',
# 'https://en.wikipedia.org/wiki/Underground_living',
# 'https://en.wikipedia.org/wiki/List_of_sovereign_states_in_Europe_by_date_of_achieving_sovereignty',
# 'https://en.wikipedia.org/wiki/Decolonization_of_the_Americas',
# 'https://en.wikipedia.org/wiki/Decolonization_of_Africa',
# 'https://en.wikipedia.org/wiki/Decolonisation_of_Asia',
# 'https://en.wikipedia.org/wiki/Decolonisation_of_Oceania',
# 'https://en.wikipedia.org/wiki/Exploration',
# 'https://en.wikipedia.org/wiki/Maritime_history',
# 'https://en.wikipedia.org/wiki/Maritime_history_of_Europe',
# 'https://en.wikipedia.org/wiki/Age_of_Discovery',
# 'https://en.wikipedia.org/wiki/Discovery_and_exploration_of_the_Solar_System',
# 'https://en.wikipedia.org/wiki/Colonization',
# 'https://en.wikipedia.org/wiki/Colonies_in_antiquity',
# 'https://en.wikipedia.org/wiki/Imperialism',
# 'https://en.wikipedia.org/wiki/Chartered_company',
# 'https://en.wikipedia.org/wiki/Intervention_philosophy',
# 'https://en.wikipedia.org/wiki/Colonialism',
# 'https://en.wikipedia.org/wiki/Chronology_of_Western_colonialism',
# 'https://en.wikipedia.org/wiki/History_of_colonialism',
# 'https://en.wikipedia.org/wiki/Colonial_empire',
# 'https://en.wikipedia.org/wiki/United_Nations_list_of_Non-Self-Governing_Territories',
# 'https://en.wikipedia.org/wiki/Dependent_territory',
# 'https://en.wikipedia.org/wiki/International_Space_Station',
# 'https://en.wikipedia.org/wiki/Militarisation_of_space',
# 'https://en.wikipedia.org/wiki/Commercialization_of_space',
# 'https://en.wikipedia.org/wiki/Modern_history',
# 'https://en.wikipedia.org/wiki/British_Empire',
# 'https://en.wikipedia.org/wiki/Dutch_Empire',
# 'https://en.wikipedia.org/wiki/French_colonial_empire',
# 'https://en.wikipedia.org/wiki/German_colonial_empire',
# 'https://en.wikipedia.org/wiki/Italian_Empire',
# 'https://en.wikipedia.org/wiki/Portuguese_Empire',
# 'https://en.wikipedia.org/wiki/Spanish_Empire',
# 'https://en.wikipedia.org/wiki/United_States_territorial_acquisitions',
# 'https://en.wikipedia.org/wiki/Territory_of_Papua_and_New_Guinea',
# 'https://en.wikipedia.org/wiki/List_of_former_Austrian_colonies',
# 'https://en.wikipedia.org/wiki/Belgian_colonial_empire',
# 'https://en.wikipedia.org/wiki/Danish_colonial_empire',
# 'https://en.wikipedia.org/wiki/Realm_of_New_Zealand',
# 'https://en.wikipedia.org/wiki/List_of_possessions_of_Norway',
# 'https://en.wikipedia.org/wiki/Couronian_colonization',
# 'https://en.wikipedia.org/wiki/Swedish_overseas_colonies',
# 'https://en.wikipedia.org/wiki/United_States_territorial_acquisitions',
# 'https://en.wikipedia.org/wiki/Chinese_imperialism',
# 'https://en.wikipedia.org/wiki/Empire_of_Japan',
# 'https://en.wikipedia.org/wiki/State_organisation_of_the_Ottoman_Empire',
# 'https://en.wikipedia.org/wiki/Russian_Empire',
# 'https://en.wikipedia.org/wiki/South-West_Africa',
# 'https://en.wikipedia.org/wiki/Decolonization',
# 'https://en.wikipedia.org/wiki/Wars_of_national_liberation',
# 'https://en.wikipedia.org/wiki/List_of_predecessors_of_sovereign_states_in_Europe',
# 'https://en.wikipedia.org/wiki/List_of_predecessors_of_sovereign_states_in_South_America',
# 'https://en.wikipedia.org/wiki/List_of_sovereign_states_by_date_of_formation',
# 'https://en.wikipedia.org/wiki/Postcolonialism',
# 'https://en.wikipedia.org/wiki/Independence',
# 'https://en.wikipedia.org/wiki/Nation-building',
# 'https://en.wikipedia.org/wiki/Post-communism',
# 'https://en.wikipedia.org/wiki/Postcolonialism_(international_relations)',
# 'https://en.wikipedia.org/wiki/Terra_nullius',
# 'https://en.wikipedia.org/wiki/Indigenous_peoples',
# 'https://en.wikipedia.org/wiki/Uncontacted_peoples',
# 'https://en.wikipedia.org/wiki/Exploration_of_Mercury',
# 'https://en.wikipedia.org/wiki/Observations_and_explorations_of_Venus',
# 'https://en.wikipedia.org/wiki/Exploration_of_the_Moon',
# 'https://en.wikipedia.org/wiki/Lagrangian_point',
# 'https://en.wikipedia.org/wiki/Exploration_of_Mars',
# 'https://en.wikipedia.org/wiki/Exploration_of_Phobos',
# 'https://en.wikipedia.org/wiki/Exploration_of_Ceres',
# 'https://en.wikipedia.org/wiki/Exploration_of_the_asteroids',
# 'https://en.wikipedia.org/wiki/List_of_Solar_System_probes',
# 'https://en.wikipedia.org/wiki/Exploration_of_Jupiter',
# 'https://en.wikipedia.org/wiki/Exploration_of_Europa',
# 'https://en.wikipedia.org/wiki/Exploration_of_Callisto',
# 'https://en.wikipedia.org/wiki/Exploration_of_Saturn',
# 'https://en.wikipedia.org/wiki/Exploration_of_Titan',
# 'https://en.wikipedia.org/wiki/Exploration_of_Uranus',
# 'https://en.wikipedia.org/wiki/Exploration_of_Neptune',
# 'https://en.wikipedia.org/wiki/Trans-Neptunian_object',
# 'https://en.wikipedia.org/wiki/Exploration_of_Pluto',
# 'https://en.wikipedia.org/wiki/Space_colonization',
# 'https://en.wikipedia.org/wiki/Colonization_of_Mercury',
# 'https://en.wikipedia.org/wiki/Colonization_of_Venus',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_Moon',
# 'https://en.wikipedia.org/wiki/Lagrangian_point',
# 'https://en.wikipedia.org/wiki/Colonization_of_Mars',
# 'https://en.wikipedia.org/wiki/Colonization_of_Phobos',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_asteroids',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_outer_Solar_System',
# 'https://en.wikipedia.org/wiki/Colonization_of_Jupiter',
# 'https://en.wikipedia.org/wiki/Colonization_of_Europa',
# 'https://en.wikipedia.org/wiki/Colonization_of_Callisto',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_outer_Solar_System',
# 'https://en.wikipedia.org/wiki/Colonization_of_Titan',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_outer_Solar_System',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_outer_Solar_System',
# 'https://en.wikipedia.org/wiki/Colonization_of_trans-Neptunian_objects',
# 'https://en.wikipedia.org/wiki/Colonization_of_the_outer_Solar_System',
# 'https://en.wikipedia.org/wiki/Help:Authority_control',
# 'https://en.wikipedia.org/wiki/Integrated_Authority_File',
# 'https://en.wikipedia.org/wiki/National_Diet_Library']

def get_links(url):
    print 'request sent for - ',url,'job size = ',len(jobs)

    r = s.get(url)

    if r.status_code == 200:
        tree = html.fromstring(r.text)
        title = tree.xpath('//*[@id="firstHeading"]/text()')
        links = tree.xpath('//*[@id="mw-content-text"]//a')
        print 'extacted - ', title, 'job size = ',len(jobs)

        # next_links = []
        for link in links:
            next_link = link.xpath('.//@href')[0]

            if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                urls2.append('https://en.wikipedia.org' + next_link)
                # pass
                # urls2.append(p.spawn(get_links, 'https://en.wikipedia.org' + next_link))


for url in urls:
    jobs.append(p.spawn(get_links, url))
try:
    gevent.joinall(jobs)
except Exception as e:
    print e

for url in urls2:
    jobs.append(p.spawn(get_links, url))
try:
    gevent.joinall(jobs)
except Exception as e:
    print e
