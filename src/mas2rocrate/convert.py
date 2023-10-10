import base64


def hash_identifier(identifier):
    return str(
        base64.b32encode(bytes(str(identifier), encoding='utf-8')),
        encoding="ascii",
    )


def process_nationality(nationality, country):
    nationality = nationality.strip()
    country = country.strip()
    ADJ_TO_NOUN_MAP = {
        'Austrian': 'Austria',
        'Chinese': 'China',
        'French': 'France',
        'German': 'Germany',
        'Lithuanian': 'Lithuania',
        'Norsk': 'Norway',
        'Norwegian': 'Norway',
        'Polish': 'Poland',
        'Portuguese': 'Portugal',
        'Spanish': 'Spain',
        'Turkish': 'Turkey',
        'USA': 'United States of America',
        'Norway': 'Norway',
    }
    NAME_TO_ISO_MAP = {
        'Austria': 'AUT',
        'China': 'CHN',
        'France': 'FRA',
        'Germany': 'DEU',
        'Lithuania': 'LTU',
        'Norway': 'NOR',
        'Poland': 'POL',
        'Portugal': 'PRT',
        'Spain': 'ESP',
        'Turkey': 'TUR',
        'United States of America': 'USA',
    }
    if not (nationality or country):
        return '', {}
    if not country:
        country = ADJ_TO_NOUN_MAP.get(nationality, nationality)
    identifier = NAME_TO_ISO_MAP[country]
    blob = {
        '@id': f'#{identifier}',
        '@type': 'Country',
        'name': country,
        'identifier': identifier,
        'sameAs': f'https://en.wikipedia.org/wiki/{country}',
    }
    return identifier, blob


def process_organization(org_short):
    MAP = {}
    return org_short, MAP.get(org_short, None)


def process_project_leader(person):
    country = None
    first_name = person['firstname']
    last_name = person['surname']
    slug_basis = f"{first_name}-{last_name}".lower()
    identifier = hash_identifier(slug_basis)
    person_blob = {
        '@id': f'#{identifier}',
        '@type': 'Person',
        'name': f'{first_name} {last_name}',
        'givenName': first_name,
        'familyName': last_name,
    }
    nationality = person['nationality']
    country = person['country']
    if nationality or country:
        nat_ident, country = process_nationality(nationality, country)
        person_blob['nationality'] = f'#{nat_ident}'
    orgid, organization = process_organization(person['org_short'])
    if organization:
        person_blob['affiliation'] = f'#{orgid}'
    return identifier, person_blob, organization, country


def process_project(project):
    root_dataset = {}
    items = []
    identifier = './'
    root_dataset['@id'] = './'
    root_dataset['identifier'] = project['account_number']
    root_dataset['name'] = project['title']
    root_dataset['description'] = project['description']
    pm = project['project_leader']
    if pm:
        pm_id, person, org, country = process_project_leader(pm)
        root_dataset['pm'] = f'#{pm_id}'
        items.append(person)
        if country:
            items.append(country)
    return identifier, root_dataset, items


def generate_skeleton(identifier='./', root_dataset=None):
    skeleton = {
       "@context": "https://w3id.org/ro/crate/1.1/context",
       "@graph": [
           {
               "@id": "ro-crate-metadata.json",
               "@type": "CreativeWork",
               "about": {
                   "@id": identifier,
               },
               "conformsTo": {
                   "@id": "https://w3id.org/ro/crate/1.1"
               }
           },
           {
               "@id": identifier,
               "@type": "Dataset"
           }
       ]
    }
    if root_dataset:
        skeleton['@graph'][1] = root_dataset
    return skeleton


def generate_jsonld(identifier, dataset, items):
    skeleton = generate_skeleton(identifier, dataset)
    item_set = set()
    for item in items:
        item_set.add(tuple(item.items()))
    for item in item_set:
        skeleton['@graph'].append(dict(item))
    return skeleton
