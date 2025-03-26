import streamlit as st

st.title(" :grey[Explore le language des signes américain]")

st.markdown("""
Bienvenue sur cette page interactive pour apprendre les bases du langage des signes américain (ASL) !
Choisis une catégorie et découvre visuellement les signes essentiels.
""")

col1, col2, = st.columns([1, 2])
with col1:
    st.image("media/Green_theme_2.jpg")

with col2:

    genre = st.radio(
        "Selectionne une catégorie :",
        ["***Alphabet - Maîtriser les bases avec l'alphabet manuel***",
        "***Nombre - Apprendre à compter et à exprimer des quantités***",
        "***Mots - Quelques mots de la vie courante***"]
        #,    captions=["A B C ...", "1 2 3 ...",  "Good Morning!!" ],
    )

if genre == "***Alphabet - Maîtriser les bases avec l'alphabet manuel***":
    # st.write("tu as choisis l'Alphabet")
    st.image("media/Learning_Letters_W.png")

elif genre == "***Nombre - Apprendre à compter et à exprimer des quantités***":
    # st.write("Tu as choisis l'Alphabet")
    st.image("media/Learning_Numbers.png")

elif genre == ("***Mots - Quelques mots de la vie courante***"):
    # st.write("tu as choisis les expressions courantes")
    mots = ["Hello","Yes","No","Good","Good Morning","Bye","Pardon","Little bit","Please","Project","whats up"]
    images_mots = {
        "Hello": "media/signs/hello.png",
        "Yes": "media/signs/yes.png",
        "No": "media/signs/no.png",
        "Pardon": "media/signs/pardon.png",
        "Little bit": "media/signs/littlebit.png",
        "Please": "media/signs/please.png",
        "Project": "media/signs/project.png",
        "whats up": "media/signs/whatup.png",
        "Good": "media/signs/good.png",
        "Good Morning": "media/signs/goodmorning.png",
        "Bye": "media/signs/bye.png"
    }
    col1, col2 = st.columns([1, 2])
    with col1:

        #st.header("📋 Liste des mots")
        selected_word = st.radio("", mots)

    with col2:
        st.image(images_mots[selected_word], use_container_width=True)
