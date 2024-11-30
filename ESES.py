import pandas as pd
from experta import *
import streamlit as st
import os
import base64

import base64


# Load the knowledge base (CSV file)
df = pd.read_csv('knowledgebase.csv')

# Define the facts for the expert system
class FactData(Fact):
    pass

# Define the Expert System
class EndangeredSpeciesExpertSystem(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield FactData()

    # Rule 1: Habitat + Diet → Population
    @Rule(Fact(habitat=MATCH.habitat), Fact(diet=MATCH.diet))
    def habitat_diet_population(self, habitat, diet):
        species = df[(df['habitat'] == habitat) & (df['diet'] == diet)]
        if not species.empty:
            self.declare(Fact(population=species.iloc[0]['population']))

    # Rule 2: Population + Lifespan → Threats
    @Rule(Fact(population=MATCH.population), Fact(lifespan=MATCH.lifespan))
    def population_lifespan_threats(self, population, lifespan):
        species = df[(df['population'] == population) & (df['lifespan'] == lifespan)]
        if not species.empty:
            self.declare(Fact(threats=species.iloc[0]['threats']))

    # Rule 3: Habitat + Offsprings → Physical Description
    @Rule(Fact(habitat=MATCH.habitat), Fact(offsprings=MATCH.offsprings))
    def habitat_offsprings_physical_description(self, habitat, offsprings):
        species = df[(df['habitat'] == habitat) & (df['Offspring'] == offsprings)]
        if not species.empty:
            self.declare(Fact(physical_description=species.iloc[0]['physical_description']))

    # Rule 4: Population + Lifespan → Conservation Status
    @Rule(Fact(population=MATCH.population), Fact(lifespan=MATCH.lifespan))
    def population_lifespan_conservation_status(self, population, lifespan):
        species = df[(df['population'] == population) & (df['lifespan'] == lifespan)]
        if not species.empty:
            self.declare(Fact(conservation_status=species.iloc[0]['conservation_status']))

    # Rule 5: Habitat + Diet + Lifespan → Name
    @Rule(Fact(habitat=MATCH.habitat), Fact(diet=MATCH.diet), Fact(lifespan=MATCH.lifespan))
    def habitat_diet_lifespan_name(self, habitat, diet, lifespan):
        species = df[(df['habitat'] == habitat) & (df['diet'] == diet) & (df['lifespan'] == lifespan)]
        if not species.empty:
            self.declare(Fact(name=species.iloc[0]['name']))

    # Rule 6: Name → All other output features
    @Rule(Fact(name=MATCH.name))
    def name_all_features(self, name):
        species = df[df['name'] == name]
        if not species.empty:
            self.declare(Fact(scientific_name=species.iloc[0]['scientific_name']))
            self.declare(Fact(conservation_status=species.iloc[0]['conservation_status']))
            self.declare(Fact(population=species.iloc[0]['population']))
            self.declare(Fact(warning=species.iloc[0]['warning']))
            self.declare(Fact(recommendation_to_save=species.iloc[0]['recommendation_to_save']))
            self.declare(Fact(physical_description=species.iloc[0]['physical_description']))

# Function to run the expert system
def run_expert_system(habitat, diet, offsprings, lifespan):
    engine = EndangeredSpeciesExpertSystem()  # Create an instance of the expert system
    engine.reset()  # Reset the engine to clear any previous state
    
    # Declare user input as facts
    engine.declare(Fact(habitat=habitat))
    engine.declare(Fact(diet=diet))
    engine.declare(Fact(offsprings=offsprings))
    engine.declare(Fact(lifespan=lifespan))
    
    # Run the inference engine
    engine.run()
    
    # Retrieve the results
    results = {}
    for fact in engine.facts.values():
        if isinstance(fact, Fact):
            results.update(fact)
    
    return results

# Streamlit interface
st.title("Endangered Species Expert System")
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('img3.jpg')

# Collect user input from Streamlit widgets
habitat = st.selectbox('Select Habitat:', ['Bamboo Forest', 'Savannah', 'Rainforest', 'Grassland', 'Arctic', 'Mountain', 'Ocean', 'Coastal'])
diet = st.selectbox('Select Diet:', ['Herbivore', 'Carnivore', 'Omnivore'])
offsprings = st.text_input('Enter Offsprings:')
lifespan = st.text_input('Enter Lifespan:')

# Button to run the expert system
if st.button('Run Expert System'):
    result = run_expert_system(habitat, diet, offsprings, lifespan)
    
    order = [
        "name", "scientific_name", "habitat", "conservation_status", "population", 
        "threats", "diet", "offsprings", "lifespan", "physical_description", 
        "habitat_type", "endangered_factors", "warning", "recommendation_to_save"
    ]
      # Define CSS styles for bold labels and colored text
    label_style = "font-weight: bold; color: #228B22;"  # Orange color for labels
    value_style = "color: #37474f;"  # Dark gray color for values

    # Display results in the specified order
    st.write("Results:")
    for key in order:
        if key in result:
            st.markdown(f"<span style='{label_style}'>{key}:</span> <span style='{value_style}'>{result[key]}</span>", unsafe_allow_html=True)
