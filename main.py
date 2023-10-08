
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
import os
from dotenv import load_dotenv

load_dotenv()

huggingface_endpoint = os.getenv("hugging_face_api")


fallacies = {
    "Circular reasoning": "Circular reasoning occurs when the premise of an argument is used to support itself.\n\nExample: The President of the United States is a good leader (claim), because they are the leader of this country ",
    "Fallacy of logic": "The term 'fallacy of logic' is not a specific fallacy but may refer to various errors in logical reasoning. It lacks a clear definition in logical fallacies.\n\n This term lacks a specific example due to its general nature.",
    "Equivocation": "Equivocation involves using ambiguous language or shifting the meaning of a term within an argument.\n\nExample: An example is claiming that a feather is 'light' and therefore cannot be 'dark.'",
    "Fallacy of credibility": "This fallacy involves relying too heavily on the credibility of a source without considering the actual evidence or argument presented.\n\nExample: For instance, trusting a news article solely because it's from a reputable source.",
    "Ad populum": "Ad populum, or the bandwagon fallacy, occurs when someone appeals to popular beliefs or opinions to support an argument.\n\nExample: An example is believing something is true because everyone else does.",
    "Fallacy of extension": "This fallacy involves making unwarranted generalizations or assumptions about a group based on the characteristics of a few members.\n\nExample: For example, assuming all politicians are corrupt based on a few scandals.",
    "Intentional": "The term 'intentional' is not a specific fallacy but may refer to arguments made with deliberate deception or manipulation. It relates to the intention behind making an argument.\n\nExample: This term lacks a specific example due to its general nature.",
    "Faulty generalization": "Faulty generalization is the act of drawing a conclusion about an entire group based on insufficient or biased evidence.\n\nExample: For instance, concluding that everyone from a city is rude based on a couple of encounters.",
    "Appeal to emotion": "Appeal to emotion involves manipulating emotions to win an argument rather than relying on valid reasoning.\n\nExample: An example is urging support for a policy by evoking fear for innocent children.",
    "Fallacy of relevance": "The fallacy of relevance occurs when arguments are presented that are not pertinent to the topic under discussion.\n\nExample: For example, bringing up unrelated issues during a climate change debate.",
    "False dilemma": "A false dilemma, or false dichotomy, is presented when only two options are offered when there are more possible alternatives.\n\nExample: For instance, saying, 'You're either with us or against us.'",
    "Ad hominem": "Ad hominem attacks the person making the argument rather than addressing the argument itself.\n\nExample: An example is dismissing a scientist's research because of personal dislike.",
    "False causality": "False causality is the assumption that because one event followed another, the first event caused the second.\n\nExample: For example, wearing a red shirt and then your team winning, assuming the shirt caused the victory.",
    "Miscellaneous": "The 'miscellaneous' category is a catch-all for various fallacies that do not fit neatly into other categories. It includes arguments that may contain multiple fallacies, making them challenging to address directly.\n\nExample: An example is an argument containing various fallacies that make it hard to address directly."
}


st.set_page_config(page_title = "Logical Fallacy Detector", page_icon = "🧠", layout= "centered")

st.sidebar.markdown("---")
st.sidebar.markdown("Connect with me on LinkedIn:")
st.sidebar.link_button("LinkedIn", url ="https://www.linkedin.com/in/muhammed-ashhar-b07145267/")

def load_anime(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()

animation = load_anime("https://lottie.host/44a46447-0aac-4fb0-a430-9c58a97016ab/szMgs1h0mH.json")

with st.container():
    st.title("LOGICAL FALLACY DETECTOR 🔎")
    st.caption("TOP 3 PROBABLE FLAWS")
    st.write("---")

with st.container():
    try:
        st_lottie(animation, height=200)
    except:
        print("Error Loading The Animation")


API_URL = "https://api-inference.huggingface.co/models/q3fer/distilbert-base-fallacy-classification"
headers = {"Authorization": f"{huggingface_endpoint}"}

grouped_fallacies = []
def find_fallacies(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def top_three_fallacies():
      count = 0
      for i in output[0]:
          if count == 3:
             break
          fallacy = i.get("label").capitalize()
          grouped_fallacies.append(fallacy)
          count = count + 1

def visualize():
    with st.container():
        tab1, tab2, tab3 = st.tabs([grouped_fallacies[0], grouped_fallacies[1], grouped_fallacies[2]])
        for i in range(3):
            if i == 0:
                with tab1:
                    st.image("https://cdn-icons-png.flaticon.com/512/5238/5238429.png", width = 150)
                    st.subheader(grouped_fallacies[i])
                    st.write(fallacies.get(grouped_fallacies[i]))
            elif i == 1:
                with tab2:
                    st.image("https://cdn-icons-png.flaticon.com/512/5234/5234762.png", width = 150)
                    st.subheader(grouped_fallacies[i])
                    st.write(fallacies.get(grouped_fallacies[i]))
            elif i == 2:
                with tab3:
                    st.image("https://cdn-icons-png.flaticon.com/512/5776/5776927.png", width = 150)
                    st.subheader(grouped_fallacies[i])
                    st.write(fallacies.get(grouped_fallacies[i]))
        st.write("---")


if __name__ == "__main__":
    statement = st.text_input("Enter Your Statement Here : ")
    if statement:
        try:
           output = find_fallacies({"inputs": f"{statement}", })
        except:
            print("Error Acquiring Data, Try Again !")
        time.sleep(4)
        try:
            top_three_fallacies()
        except:
            print("Unable to detect fallacies! Try Again")

        try:
           visualize()
        except:
            print("Error Loading Data, Try Again")

        st.info(f"The most accurate logical fallacy is {grouped_fallacies[0]}. Others are less relevant.")





