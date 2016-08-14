#!/usr/bin/env python
# coding: utf-8
# Pokémon GO data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bs4, re, urllib

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

def read_csv(data, **kwargs):
    """Read CSV from a string."""
    return pd.read_csv(StringIO(data), delim_whitespace=True, **kwargs)

# Pokémon types
types = read_csv("""
           Type1    Type2
Aerodactyl Rock     Flying
Arbok      Poison   -
Arcanine   Fire     -
Bellsprout Grass    Poison
Charizard  Fire     Flying
Cubone     Ground   -
Dodrio     Normal   Flying
Electabuzz Electric -
Exeggcute  Grass    Psychic
Fearow     Normal   Flying
Flareon    Fire     -
Golduck    Water    -
Golbat     Poison   Flying
Golem      Rock     Ground
Graveler   Rock     Ground
Growlithe  Fire     -
Ivysaur    Grass    Poison
Jolteon    Electric -
Jynx       Psychic  Ice
Kabutops   Rock     Water
Lapras     Ice      Water
Lickitung  Normal   -
Machoke    Fighting -
Magmar     Fire     -
Marowak    Ground   -
Parasect   Bug      Grass
Pidgeot    Flying   Normal
Pinsir     Bug      -
Ponyta     Fire     -
Primeape   Fighting -
Rapidash   Fire     -
Raticate   Normal   -
Rhydon     Ground   Rock
Rhyhorn    Ground   Rock
Sandslash  Ground   -
Scyther    Flying   Bug
Snorlax    Normal   -
Squirtle   Water    -
Starmie    Psychic  Water
Tauros     Normal   -
Tentacool  Water    Poison
Vaporeon   Water    -
Venomoth   Bug      Poison
Weepinbell Grass    Poison
""", index_col=0)

# Move (attack) data from http://www.pokemongodb.net/.
moves = read_csv("""
                    Type Power Cooldown
Acid              Poison    10     1.05
Bite                Dark     6      0.5
Bubble             Water    25      2.3
BugBite              Bug     5     0.45
BulletPunch        Steel    10      1.2
Confusion        Psychic    15     1.51
Cut               Normal    12     1.13
DragonBreath      Dragon     6      0.5
Ember               Fire    10     1.05
FeintAttack         Dark    12     1.04
FireFang            Fire    10     0.84
FrostBreath          Ice     9     0.81
FuryCutter           Bug     3      0.4
IceShard             Ice    15      1.4
KarateChop      Fighting     6      0.8
Lick               Ghost     5      0.5
LowKick         Fighting     5      0.6
MetalClaw          Steel     8     0.63
MudShot           Ground     6     0.55
MudSlap           Ground    15     1.35
Peck              Flying    10     1.15
PoisonJab         Poison    12     1.05
PoisonSting       Poison     6     0.58
Pound             Normal     7     0.54
PsychoCut        Psychic     7     0.57
QuickAttack       Normal    10     1.33
RazorLeaf          Grass    15     1.45
RockSmash       Fighting    15     1.41
RockThrow           Rock    12     1.36
Scratch           Normal     6      0.5
ShadowClaw         Ghost    11     0.95
Spark           Electric     7      0.7
Splash             Water     0     1.23
SteelWing          Steel    15     1.33
SuckerPunch         Dark     7      0.7
Tackle            Normal    12      1.1
ThunderShock    Electric     5      0.6
VineWhip           Grass     7     0.65
WaterGun           Water     6      0.5
WingAttack        Flying     9     0.75
ZenHeadbutt      Psychic    12     1.05
AerialAce         Flying    30      2.9
AirCutter         Flying    30      3.3
AncientPower        Rock    35      3.6
AquaJet            Water    25     2.35
AquaTail           Water    45     2.35
Blizzard             Ice   100      3.9
BodySlam          Normal    40     1.56
BoneClub          Ground    25      1.6
BrickBreak      Fighting    30      1.6
Brine              Water    25      2.4
BubbleBeam         Water    30      2.9
BugBuzz              Bug    75     4.25
Bulldoze          Ground    35      3.4
CrossChop       Fighting    60        2
CrossPoison       Poison    25      1.5
DarkPulse           Dark    45      3.5
DazzlingGleam      Fairy    55      4.2
Dig               Ground    70      5.8
DisarmingVoice     Fairy    25      3.9
Discharge       Electric    35      2.5
DragonClaw        Dragon    35      1.6
DragonPulse       Dragon    65      3.6
DrainingKiss       Fairy    25      2.8
DrillPeck         Flying    40      2.7
DrillRun          Ground    50      3.4
Earthquake        Ground   100      4.2
FireBlast           Fire   100      4.1
FirePunch           Fire    40      2.8
FlameBurst          Fire    30      2.1
FlameCharge         Fire    25      3.1
FlameWheel          Fire    40      4.6
Flamethrower        Fire    55      2.9
FlashCannon        Steel    60      3.9
GunkShot          Poison    65        3
HeatWave            Fire    80      3.8
HornAttack        Normal    25      2.2
Hurricane         Flying    80      3.2
HydroPump          Water    90      3.8
HyperBeam         Normal   120        5
HyperFang         Normal    35      2.1
IceBeam              Ice    65     3.65
IcePunch             Ice    45      3.5
IcyWind              Ice    25      3.8
IronHead           Steel    30        2
LeafBlade          Grass    55      2.8
LowSweep        Fighting    30     2.25
MagnetBomb         Steel    30      2.8
Megahorn             Bug    80      3.2
Moonblast          Fairy    85      4.1
MudBomb           Ground    30      2.6
NightSlash          Dark    30      2.7
OminousWind        Ghost    30      3.1
PetalBlizzard      Grass    65      3.2
PlayRough          Fairy    55      2.9
PoisonFang        Poison    25      2.4
PowerGem            Rock    40      2.9
PowerWhip          Grass    70      2.8
Psybeam          Psychic    40      3.8
Psychic          Psychic    55      2.8
Psyshock         Psychic    40      2.7
RockSlide           Rock    50      3.2
RockTomb            Rock    30      3.4
Scald              Water    55        4
SeedBomb           Grass    40      2.4
ShadowBall         Ghost    45     3.08
SignalBeam           Bug    45      3.1
Sludge            Poison    30      2.6
SludgeBomb        Poison    55      2.6
SludgeWave        Poison    70      3.4
SolarBeam          Grass   120      4.9
Stomp             Normal    30      2.1
StoneEdge           Rock    80      3.1
Struggle          Normal    15      1.7
Submission      Fighting    30      2.1
Swift             Normal    30        3
Thunder         Electric   100      4.3
ThunderPunch    Electric    40      2.4
Thunderbolt     Electric    55      2.7
Twister           Dragon    25      2.7
ViceGrip          Normal    25      2.1
WaterPulse         Water    35      3.3
Wrap              Normal    25        4
X-Scissor            Bug    35      2.1
""")

# Compute damage per second.
moves['DPS'] = moves['Power'] / moves['Cooldown']

# Data from http://pokemondb.net/type split into two tables for readability
data1 = read_csv("""
         Normal Fire Water Electric Grass Ice Fighting Poison Ground
Normal     -     -     -      -       -    -     -       -      -   
Fire       -    0.5   0.5     -       2    2     -       -      -   
Water      -     2    0.5     -      0.5   -     -       -      2   
Electric   -     -     2     0.5     0.5   -     -       -      0   
Grass      -    0.5    2      -      0.5   -     -      0.5     2   
Ice        -    0.5   0.5     -       2   0.5    -       -      2   
Fighting   2     -     -      -       -    2     -      0.5     -   
Poison     -     -     -      -       2    -     -      0.5    0.5  
Ground     -     2     -      2      0.5   -     -       2      -   
Flying     -     -     -     0.5      2    -     2       -      -   
Psychic    -     -     -      -       -    -     2       2      -   
Bug        -    0.5    -      -       2    -    0.5     0.5     -   
Rock       -     2     -      -       -    2    0.5      -     0.5  
Ghost      0     -     -      -       -    -     -       -      -   
Dragon     -     -     -      -       -    -     -       -      -   
Dark       -     -     -      -       -    -    0.5      -      -   
Steel      -    0.5   0.5    0.5      -    2     -       -      -   
Fairy      -    0.5    -      -       -    -     2      0.5     -   
""")

data2 = read_csv("""
         Flying Psychic Bug Rock Ghost Dragon Dark Steel Fairy
Normal     -       -     -   0.5   0     -     -    0.5    -  
Fire       -       -     2   0.5   -    0.5    -     2     -  
Water      -       -     -    2    -    0.5    -     -     -  
Electric   2       -     -    -    -    0.5    -     -     -  
Grass     0.5      -    0.5   2    -    0.5    -    0.5    -  
Ice        2       -     -    -    -     2     -    0.5    -  
Fighting  0.5     0.5   0.5   2    0     -     2     2    0.5 
Poison     -       -     -   0.5  0.5    -     -     0     2  
Ground     0       -    0.5   2    -     -     -     2     -  
Flying     -       -     2   0.5   -     -     -    0.5    -  
Psychic    -      0.5    -    -    -     -     0    0.5    -  
Bug       0.5      2     -    -   0.5    -     2    0.5   0.5 
Rock       2       -     2    -    -     -     -    0.5    -  
Ghost      -       2     -    -    2     -    0.5    -     -  
Dragon     -       -     -    -    -     2     -    0.5    0  
Dark       -       2     -    -    2     -    0.5    -    0.5 
Steel      -       -     -    2    -     -     -    0.5    2  
Fairy      -       -     -    -    -     2     2    0.5    -
""")

# damage_factor[i, j] is the damage multiplier for attack of type i on Pokémon
# of type j.
damage_factor = pd.concat([data1, data2], axis=1).replace('-', 1.0)
damage_factor = damage_factor.apply(pd.to_numeric, errors='coerce')

def show_as_heatmap(df):
    """Display data in dataframe df as a heatmap."""
    plt.pcolor(df)
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation=90)
    plt.gca().invert_yaxis()
    plt.show()

def get_dps(pokemon, move):
    """Get Damage Per Second (DPS) adjusted for Same Type Attack Bonus."""
    t = types.loc[pokemon.Pokemon]
    m = moves.loc[move]
    dps = float(m.DPS)
    if m.Type == t.Type1 or m.Type == t.Type2:
        dps *= 1.25
    return round(dps, 1)

def fetch_bs_html(url):
    """Fetch an HTML page and return it as a BeautifulSoup object."""
    r = urllib.urlopen(url).read()
    return bs4.BeautifulSoup(r, "html.parser")    

def get_rows(soup, start_row=1):
    """Return contents of all table rows in soup."""
    def first(items):
        return items[0] if len(items) > 0 else None
    for tr in soup.table.find_all('tr')[start_row:]:
        yield [first(td.contents) for td in tr.find_all('td')]

def link2type(link):
    """Convert a link to Pokémon type."""
    if link is None:
        return '-'
    return re.sub('.*/(.*)-type-.*.html', r'\1', link['href']).title()

def get_moves(kind, moves):
    """Get move data from http://www.pokemongodb.net."""
    soup = fetch_bs_html(
        'http://www.pokemongodb.net/2016/04/{}-move.html'.format(kind))
    for move, type, _, _, power, seconds, _ in get_rows(soup, 2):
        move = move.contents[0]
        if move.endswith('STAB'):
            continue
        move = move.replace(' ', '')
        moves.append({'Move': move, 'Type': link2type(type),
                      'Power': power, 'Cooldown': seconds})

def update_data(content, df, name):
    pd.set_option('display.max_rows', len(df))
    content = re.sub(r'({} = read_csv\(""")([^"])*'.format(name),
                     r'\1\n' + df.to_string(index_names=False) + '\n',
                     content, 0)

if __name__ == '__main__':
    with open(__file__, 'r') as f:
        content = f.read().decode('utf-8')
    # Get move data.
    moves = []
    for kind in ['fast', 'charge']:
        get_moves(kind, moves)
    df = pd.DataFrame(moves, columns=('Move', 'Type', 'Power', 'Cooldown'))
    update_data(content, df.set_index('Move'), 'moves')
    # Get Pokémon data
    soup = fetch_bs_html(
        'http://www.pokemongodb.net/2016/07/pokemon-by-attack.html')
    pokemon_list = []
    for _, _, pokemon, type1, type2, _, attack, _ in get_rows(soup):
        pokemon = pokemon.contents[0]
        pokemon_list.append({'Pokemon': pokemon, 'Type1': link2type(type1),
                             'Type2': link2type(type2), 'Attack': attack})
    df = pd.DataFrame(pokemon_list,
                      columns=('Pokemon', 'Type1', 'Type2', 'Attack'))
    update_data(content, df.set_index('Pokemon'), 'types')
    # Write data.
    with open(__file__, 'w') as f:
        f.write(content.encode('utf-8'))
