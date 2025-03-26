import streamlit as st

st.title(" :grey[Explore le language des signes]")


genre = st.radio(
    "Selectionne une catégorie :",
    ["***Alphabet - Maîtriser les bases avec l'alphabet manuel***",
     "***Nombre - Apprendre à compter et à exprimer des quantités***",
     "***Expressions courantes - Expressions essentielles de la vie quotidienne***"]
    #,    captions=["A B C ...", "1 2 3 ...",  "Good Morning!!" ],
)

if genre == "***Alphabet - Maîtriser les bases avec l'alphabet manuel***":
    # st.write("tu as choisis l'Alphabet")
    st.image("media/Learning_Letters_W.png")
elif genre == "***Nombre - Apprendre à compter et à exprimer des quantités***":
    # st.write("Tu as choisis l'Alphabet")
    st.image("media/Learning_Numbers.png")
elif genre == ("***Expressions courantes - Expressions essentielles de la vie quotidienne***"):
    # st.write("tu as choisis les expressions courantes")
    st.image("media/Learning_Words.png")


st.image("media/Green_theme_2.jpg")
