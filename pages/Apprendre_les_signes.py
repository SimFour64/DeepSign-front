import streamlit as st

st.title(" :grey[Explore la langue des signes américain]")

st.markdown("""
Bienvenue sur cette page interactive pour apprendre les bases de la langue des signes américain (ASL) !
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
        "Hello": "media/learn/hello.png",
        "Yes": "media/learn/yes.png",
        "No": "media/learn/no.png",
        "Pardon": "media/learn/pardon.png",
        "Little bit": "media/learn/littlebit.png",
        "Please": "media/learn/please.png",
        "Project": "media/learn/project.png",
        "whats up": "media/learn/whatsup.png",
        "Good": "media/learn/good.png",
        "Good Morning": "media/learn/goodmorning.png",
        "Bye": "media/learn/bye.png"
    }
    col1, col2 = st.columns([1, 2])
    with col1:

        #st.header("📋 Liste des mots")
        selected_word = st.radio("", mots)

    with col2:
        st.image(images_mots[selected_word], use_container_width=True)
