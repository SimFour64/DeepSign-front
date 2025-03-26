import streamlit as st

st.markdown("<h1 style='text-align: center; color: '#555867';'>DeepSign</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: '#555867';'>L'application qui rend l'apprentissage de la langue des signes accessible à tous.</h1>", unsafe_allow_html=True)

left_1, center_1, right_1 = st.columns([0.25,0.5,0.25])
center_1.image("media/Green_theme_1.jpg",
             use_container_width=True,
             caption="Une femme et un homme parlent la langue des signes")

st.divider()


with st.expander("**Notre mission**",icon="🎯"):
    st.write("Rendre la langue des signes accessible au plus grand nombre et favoriser l'inclusion des personnes sourdes et malentendantes dans notre société.")

    left_2, center_2, right_2 = st.columns([0.3,0.4,0.3])
    center_2.image("media/Didactik_image_97%.png",
                use_container_width=True,
                caption="Exemple de l'application DeepSign")

    st.write("Notre plateforme interactive combine des exercices pratiques et une technologie de reconnaissance visuelle pour vous offrir une expérience d'apprentissage complète et immersive.")


with st.expander("**La langue des signes**", icon="🤟"):
    st.write("Environ 5% de la population mondiale présente un déficit auditif invalidant (suridté, limitations auditives moyennes à totales)")
    st.write("La langue des signes permet de communiquer avec les personnes présentant un tel handicap.")


with st.expander("**L'équipe**", icon="👯"):
    left_3, right_3 = st.columns([0.06,0.94])
    left_3.image('media/wagon.png')
    right_3.write('Ce projet a été conçu et développé dans le cadre du bootcamp du Wagon "Data Science & IA"')


    people = st.columns(4)
    people[0].image("media/Veronika.png")
    people[0].markdown("**Veronika Litvinova**")
    name_0 = people[0].columns([0.4,0.2,0.4])
    name_0[1].markdown("[![Foo](https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg)](https://www.linkedin.com/in/veronikalitvinova/)")
    people[1].image("media/Cyril2.PNG")
    people[1].markdown("**Cyril Buffard**")
    name_1 = people[1].columns([0.4,0.2,0.4])
    name_1[1].markdown("[![Foo](https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg)](https://www.linkedin.com/in/cyril-buffard/)")
    people[2].image("media/Fares.png")
    people[2].markdown("**Fares El Mehdaoui**")
    name_2 = people[2].columns([0.4,0.2,0.4])
    name_2[1].markdown("[![Foo](https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg)](https://www.linkedin.com/in/fares-el-mehdaoui/)")
    people[3].image("media/Simon.png")
    people[3].markdown("**Simon Fournier**")
    name_3 = people[3].columns([0.4,0.2,0.4])
    name_3[1].markdown("[![Foo](https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg)](https://www.linkedin.com/in/simon-fournier-4133566a/)")


with st.expander("**Le Deep Learning**", icon="🤖"):
    st.write("Les progrès en deep learning et en vision par ordinateur permettent de développer des systèmes de reconnaissance des signes plus précis et en temps réel.")
    st.write("Notre modèle permet de reconnaître 26 signes différents de la langue des signes américaine, et aider à diffuser cette langue des signes dans la population par le jeu")
