import streamlit as st
import requests

# Function to get sustainable design suggestions from Perplexity API
def get_sustainable_design_suggestions(product_name, target_audience, custom_prompt=None):
    url = "https://api.perplexity.ai/chat/completions"
    default_prompt = f"""Provide a report with specific product challenges/problems from the perspective
                 of the consumer or from a sustainability perspective related to the product category {product_name}.
                 
                 The challenge can be intended as a technical aspect or a sustainable design aspect.
                 
                 The target audience for this product is {target_audience} who are willing to pay more for sustainable products.
                 
                 
                Provide numeric proofs for each suggestion.
                
                Please check for quality and known articles and websites only.
                
                provide with the full reference and link.
                """

    #prompt = custom_prompt if custom_prompt else default_prompt


    if custom_prompt:
        prompt = custom_prompt
        prompt = f"{prompt}\n\n use the following product name and target audience:\n{product_name}\n{target_audience}"
    else:
        prompt = default_prompt

    payload = {
        "model": "llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "return_citations": True
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer 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"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']

# Function to get OpenAI suggestions
def get_openai_suggestions(results, custom_prompt=None):
    from openai import OpenAI

    client = OpenAI(api_key="sk-proj-6LOJAQQOLOdAu8kqqYdBT3BlbkFJf4601un6HDH7Qe38VNH1")

    default_prompt = f"""Provide a report with  suggestions for sustainable designs based on these results: {' '.join(results)}. 

                Please check for quality and known articles and websites only.
                
                Here are some designs that I made in the past. these are just general examples for you to better understand-
                example 1:
                    A NATURAL AND COMPOSTABLE MAKE UP COMPACT
                    No microplastics: 0% release of microplastics with this pack during life nor at the end of life
                    Biobased materials: 100% of materials are not derived from petroleum.
                    Composting: mBlack biodegrades in 3 months vs. the several hundred years of traditional plastics
                    Easy separability at end of life: The mirror, which is not glued, separates for recycling in seconds.
                    Changing market: millennials are willing to pay more for sustainable products
                example 2:
                    A CUSTOMIZABLE FRAGRANCE CAP WITH A CIRCULAR STORY TELLING (similar to what I showed during the call)
                    One bioplastic capsule (platform), multiple outer shell shapes (in wood). Because the tooling costs of wood are one order of magnitude lower than plastic, so it’s easier to customize
                    the capsule is made with our own bioplastic material that is called mBlack, which contains our own wood waste from our manufacturing activities. So, the marketing team can tell a nice circularity story (e.g. when I make the wood component I generate waste, that I use to make a bioplastic, that I use to make the capsule… there is some circularity in the cap)
                    bioplastic capsule ensures a nice fit with the parfume pump. At the same time the wood part gives a premium, unique touch to the cap
                """

    #prompt = custom_prompt if custom_prompt else default_prompt

    if custom_prompt:
        prompt = custom_prompt
        prompt = f"{prompt}\n\n use the following Results from Perplexity:\n{' '.join(results)}"
    else:
        prompt = default_prompt

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2400,
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    return response.choices[0].message.content

# Streamlit app
st.title("Sustainable Design Suggestions Generator")

# User input
product_name = st.sidebar.text_input("Enter product name")
target_audience = st.sidebar.text_input("Enter target audience")
iterations = st.number_input("Enter number of iterations", min_value=1, step=1)
custom_perplexity_prompt = st.sidebar.text_area("Enter custom prompt for Perplexity API (optional)")
custom_openai_prompt = st.sidebar.text_area("Enter custom prompt for OpenAI API (optional)")

if st.button('Generate Suggestions'):
    st.write("Fetching suggestions, please wait...")

    # Generate suggestions from Perplexity API
    results = [get_sustainable_design_suggestions(product_name, target_audience, custom_perplexity_prompt) for _ in range(iterations)]

    # Display intermediate results
    st.subheader("Perplexity API Results:")
    for i, result in enumerate(results, start=1):
        st.write(f"Result {i}:")
        st.write(result)

    # Generate final suggestions from OpenAI API
    final_suggestions = get_openai_suggestions(results, custom_openai_prompt)

    # Display final suggestions
    st.subheader("Final Suggestions:")
    st.write(final_suggestions)
