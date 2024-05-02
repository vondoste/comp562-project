"""Visualize as a graph.

(Will have the list of nodes on the side in the future.)

python -m part-3-visualize

Before running this script, install packages:
pip install networkx
pip install pyvis
"""


import networkx as nx
from pyvis.network import Network
import sqlite3


# db info
DB_PATH: str = "./analysis.db"
db = sqlite3.Connection(DB_PATH)
cursor = db.cursor()

# queries
LUMPED_TERMS = """
    WITH Source_Text_Info AS (SELECT node_id, word FROM Nodes),
        Target_Text_Info AS (SELECT node_id, word FROM Nodes)
    SELECT S.word, T.word 
        FROM Edges E, Source_Text_Info S, Target_Text_Info T
        WHERE E.source_node = S.node_id
            AND E.target_node = T.node_id
        ORDER BY source_node;
"""
LUMPED_TERMS_FOCUS_POPULATION = """
    WITH Source_Text_Info AS (SELECT node_id, word FROM Nodes),
        Target_Text_Info AS (SELECT node_id, word FROM Nodes)
    SELECT S.word, T.word 
        FROM Edges E, Source_Text_Info S, Target_Text_Info T, Review_Notes Re, Literature_Sources_Nodes Li
        WHERE E.source_node = S.node_id
            AND E.target_node = T.node_id
            AND E.target_node = Li.node_id
            AND Li.paper_id = Re.paper_id
            AND Re.Focus_Population like ?
        ORDER BY source_node;
"""
ARTICLES_TO_TERMS = """
    SELECT Sc.Title, No.word
        FROM Scopus_Info Sc, Nodes No, Literature_Sources_Nodes Li
        WHERE Sc.paper_id = Li.paper_id
            AND No.node_id = Li.node_id;
"""
ARTICLE_ALL_POPULATONS_TO_TERMS = """
    SELECT Re.Focus_Population, No.word
        FROM Review_Notes Re, Nodes No, Literature_Sources_Nodes Li
        WHERE Re.paper_id = Li.paper_id
            AND No.node_id = Li.node_id;
"""
ARTICLE_FOCUS_POPULATON_TO_TERM_RAW_TEXT = """
    SELECT Re.Focus_Population, No.word
        FROM Review_Notes Re, Nodes No, Literature_Sources_Nodes Li
        WHERE Re.paper_id = Li.paper_id
            AND No.node_id = Li.node_id
            AND Re.Focus_Population like '%?%';
"""
ARTICLE_FOCUS_POPULATON_TO_TERMS = """
    SELECT ?, No.word
        FROM Review_Notes Re, Nodes No, Literature_Sources_Nodes Li
        WHERE Re.paper_id = Li.paper_id
            AND No.node_id = Li.node_id
            AND Re.Focus_Population LIKE ?;
"""
ARTICLE_FIELD_TO_TERMS = """
    SELECT ?, No.word
        FROM Review_Notes Re, Nodes No, Literature_Sources_Nodes Li
        WHERE Re.paper_id = Li.paper_id
            AND No.node_id = Li.node_id
            AND Re.Study_Country_ies LIKE ?;
"""


# write query for specific articles by terms
LUMPED_TERMS_FOCUS_LOCATION = """
    WITH Source_Text_Info AS (SELECT node_id, word FROM Nodes),
        Target_Text_Info AS (SELECT node_id, word FROM Nodes)
    SELECT S.word, T.word 
        FROM Edges E, Source_Text_Info S, Target_Text_Info T, Review_Notes Re, Literature_Sources_Nodes Li
        WHERE E.source_node = S.node_id
            AND E.target_node = T.node_id
            AND E.target_node = Li.node_id
            AND Li.paper_id = Re.paper_id
            AND (Re.Focus_Location like'%education%' OR 
                Re.Focus_Location like'%school%' OR 
                Re.Focus_Location like'%university%' OR 
                Re.Focus_Location like'%Higher Ed%')
        ORDER BY source_node;
"""


def main():
    print("hi")
    G = nx.Graph()

    global cursor

    # cursor.execute(LUMPED_TERMS_FOCUS_POPULATION, ("%mobil%", ))
    # cursor.execute(ARTICLES_TO_TERMS)

    # cursor.execute(LUMPED_TERMS_FOCUS_LOCATION)
    # location_info = cursor.fetchall()
    # G.add_edges_from(location_info, color="red")

    cursor.execute(LUMPED_TERMS)
    terms_info = cursor.fetchall()
    G.add_edges_from(terms_info)

    # sample_categories = ["mobility", "visual", "hear", "cognitive", "general"]
    # optional_color = ["red", "orange", "green", "purple", "black"]
    # # sample_categories = ["mobility", "visual"]
    # # optional_color = ["red", "black"]
    # i = 0
    # while i < len(sample_categories):
    #     category = '%' + sample_categories[i] + '%'
    #     cursor.execute(ARTICLE_FOCUS_POPULATON_TO_TERMS, (category, category, ))
    #     title_info = cursor.fetchall()
    #     G.add_edges_from(title_info, color=optional_color[i])
    #     i += 1

    # sample_categories = ["China", "India", "Canada"]
    # optional_color = ["red", "green", "black"]
    # i = 0
    # while i < len(sample_categories):
    #     category = '%' + sample_categories[i] + '%'
    #     cursor.execute(ARTICLE_FIELD_TO_TERMS, (category, category, ))
    #     title_info = cursor.fetchall()
    #     G.add_edges_from(title_info, color=optional_color[i])
    #     i += 1

    nt = Network('750px', '80%', cdn_resources='remote')
    nt.from_nx(G)
    nt.show_buttons()
    nt.show('test.html', notebook=False)
    # nx.write_gml(G, "test.gml")


if __name__ == "__main__":
    main()