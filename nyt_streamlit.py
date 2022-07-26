import streamlit as st
import matplotlib.pyplot as plt
import nyt_api as nyt
import json_utils as j

api_file = "app.json"
api_dict = j.read_from_file(api_file)


def gen_freqdist (url):
    # based on solution 2 in the assignment spec
    with st.spinner(text="Generating your frequency distribution..."):
        fd = nyt.freqdist_of_abstracts(url)

        fig = plt.figure(figsize = (12, 12))
        fd.plot(10)
        plt.show()
        return fig
    # thanks Greg!


def gen_wordcloud (url):
    # based on solution 2 in the assignment spec
    with st.spinner(text="Generating your image..."):
        wc = nyt.wc_of_abstracts(url)

        fig, ax = plt.subplots()
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        return fig
    # thanks Greg!


st.set_page_config(
    page_title = "New York Times API",
    layout = "wide" #,
)

st.title("COP 4813 - Web Application Programming")
st.title("Project 1")


st.header("Part A - Stories API")
st.write("This app uses the Top Stories API to display the most common words in the top current articles based on a specified topic selected by the user. The data is displayed as a line chart and as a wordcloud image.")

st.subheader("I - Topic Selection")
name = st.text_input("Please enter your name")
topic = st.selectbox("Select a topic of your interest", nyt.options)


if name and topic:
    st.write(f"Hey {name}, you've selected the {topic} topic")


    st.subheader("II - Frequency Distribution")
    sect_ii = st.checkbox("Check to view frequency distribution")

    if topic and sect_ii:
        url = nyt.gen_top_url(topic, api_dict["key"])
        fd = gen_freqdist(url)
        st.pyplot(fd)
        st.write(f"Frequency distribution generated!")



    st.subheader("III - Wordcloud")
    sect_iii = st.checkbox("Check to show wordcloud")

    if topic and sect_iii:
        # Leverage session state (so that irrelevant value changes don't force regenerating the whole wordcloud)
        # i.e. only regenerate a wordcloud if the topic changes
        # https://docs.streamlit.io/library/api-reference/session-state

        if ('topic' not in st.session_state or 'top_wc_fig' not in st.session_state # we haven't generated a wordcloud yet
            or topic != st.session_state['topic']): # or the topic is just different from the last one

            st.session_state['topic'] = topic
            url = nyt.gen_top_url(topic, api_dict["key"])
            st.session_state['top_wc_fig'] = gen_wordcloud(url)


        st.pyplot(st.session_state['top_wc_fig'])
        st.write(f"Wordcloud generated!")



st.header("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed, or viewed articles.")

# In this second part of the WebApp, ask the user for their preferred
# set of articles: shared, emailed or viewed. Ask the user for the
# amount of time they want to collect articles from, the options
# should be the last: 1 day, 7 days or 30 days. Finally, display the
# image created by the wordcloud library.


match_timeframe_as_int = { # for easy matching on user-friendly choices
    'day': 1,
    'week (past 7 days)' : 7,
    'month (past 30 days)' : 30
}

match_share_type = { # for easy matching on user-friendly choices
    'with the most views': 'viewed',
    'most shared on Facebook': 'shared',
    'sent in the most emails': 'emailed'
}


share_method = st.selectbox("View articles", list(match_share_type))
timeframe = st.selectbox("in the last", list(match_timeframe_as_int))

if share_method and timeframe:
    # see comment above in Section III for state rationale

    # this is somewhat verbose but it makes the UI cleaner in my opinion
    # hopefully the comments are illustrative!

    if ('share_method' not in st.session_state # either we haven't generated a wordcloud yet
        or 'timeframe' not in st.session_state # ...
        or 'popular_wc_fig' not in st.session_state # ...
        or share_method != st.session_state['share_method'] # or the input has changed from when we last did generate a wordcloud
        or timeframe != st.session_state['timeframe']): # ...
    
        st.session_state['share_method'] = share_method
        st.session_state['timeframe'] = timeframe

        url = nyt.gen_popular_url(match_share_type[share_method], # convert the share method's UI label into the actual category used in the API's URL
                                 match_timeframe_as_int[timeframe], # convert their text input into an int
                                 api_dict["key"])

        st.session_state['popular_wc_fig'] = gen_wordcloud(url)
    

    st.pyplot(st.session_state['popular_wc_fig'])
    st.write(f"Wordcloud generated!")

