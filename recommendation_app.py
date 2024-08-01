import streamlit as st
import requests



st.set_page_config(
    page_title="Data Science methods",
    layout="wide",
    initial_sidebar_state="expanded",)
def intro():
    st.write("# Welcome to Minelli Product Development Tool! 👋")
    st.sidebar.success("Select a Dashboard above.")
    st.markdown(
        """
        
        This app is designed to help you find sustainable design suggestions for your product.
        
        Dashboards:
        - [New Ideas/concepts](#new-ideasconcepts)
        - [what has been done with respect to an existing product 'challenge'](#what-has-been-done-with-respect-to-an-existing-product-challenge)
        - [Latest Innovations](#latest-innovations)
        - [competitors for a product and topic](#competitors-for-a-product-and-topic)
        """
    )

def dashboard1():
    import streamlit as st
    import requests

    # Function to get sustainable design suggestions from Perplexity API
    def get_sustainable_design_suggestions(product_name,perplexity_api_key, custom_prompt=None):
        url = "https://api.perplexity.ai/chat/completions"
        default_prompt = f"""Provide a report with specific product challenges/problems related to the product category
                            {product_name}.
                            The challenge can be intended, for example, as a technical challenge (manufacturing point of view),
                            functional-design challenge (user point of view), supply challenge (supply chain point of view), sustainability
                            challenge (sustainable manager point of view), marketing challenge (marketing manager point of view), or
                            other. A product challenge is an aspect of the product that, if improved, can create a market opportunity.
                            At least 10 challenges.
                            The challenges should not be trivial.
                            Provide numeric proofs for each suggestion. These figures should prove that the suggestion is indeed a
                            relevant product problem to tackle.
                            Please check for quality and known articles and websites only.
                            Provide with the full reference and working link. Check that the link works.
                    """

        #prompt = custom_prompt if custom_prompt else default_prompt


        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following product name:\n{product_name}"
        else:
            prompt = default_prompt

        payload = {
            "model": "llama-3-sonar-large-32k-online",
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
            "authorization": f"Bearer {perplexity_api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']

    # Function to get OpenAI suggestions
    def get_openai_suggestions(results, openai_api_key, custom_prompt=None):
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)

        default_prompt = f"""Provide a report with suggestions for product designs based on these results: {''.join(results)}.
                                Check for quality and known articles and websites only.
                        
                                The suggestions should tackle a relevant problem and should not be trivial.
                                The suggestions should be technically advanced and precise.
                                Here is an example design process “from challenge to product” that we executed in the past. This is just a
                                general example for you to better understand:
                        Example: A monomaterial fragrance cap
                        Challenge: market likes wood fragrance caps (natural material, perceived sustainability, every cap is
                        different, etc.). However, an inner insert made in plastic is typically necessary to make a good, quality fit
                        between the cap and the pump. When the user sees the plastic insert, she does not like it. In addition wood
                        and plastic cannot be separated at the end of life.
                        Product solution: the fragrance cap is made using wood. The friction fit between cap and the pump is
                        ensured through three vertical cork pins. Cork is elastic and ensures a good fit. Cork and wood are
                        monomaterial. Cork and wood are perceived as sustainable natural products.
                    """

        #prompt = custom_prompt if custom_prompt else default_prompt

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following Results from Perplexity:\n{result}"
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
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    perplexity_api_key = st.sidebar.text_input("Enter your Perplexity API Key", type="password")

    st.sidebar.divider()

    product_name = st.sidebar.text_input("Enter product name")
    custom_perplexity_prompt = st.sidebar.text_area("Enter custom prompt for Perplexity API (optional)")
    custom_openai_prompt = st.sidebar.text_area("Enter custom prompt for OpenAI API (optional)")

    if st.button('Generate Suggestions'):
        st.write("Fetching suggestions, please wait...")

        # Generate suggestions from Perplexity API
        result = get_sustainable_design_suggestions(product_name,perplexity_api_key, custom_perplexity_prompt)

        # Display intermediate results
        st.subheader("Perplexity API Results:")
        st.write(result)

        # Generate final suggestions from OpenAI API
        final_suggestions = get_openai_suggestions(result,openai_api_key, custom_openai_prompt)

        # Display final suggestions
        st.subheader("Final Suggestions:")
        st.write(final_suggestions)

def dashboard2():
    import streamlit as st
    import requests

    # Function to get sustainable design suggestions from Perplexity API
    def get_sustainable_design_suggestions(product_category, product_challenge, perplexity_api_key, custom_prompt=None):
        url = "https://api.perplexity.ai/chat/completions"
        default_prompt = f"""Provide a report with specific information on what has been done with respect to the following product challenge:
                            Product Category: {product_category}
                            Product Challenge: {product_challenge}
                            Please provide specific examples, solutions, and innovations that have addressed this challenge. Include references and working links to relevant articles and websites.
                            Look for 10 suggestions.Provide references.
                            """

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following product category and challenge:\n{product_category}\n{product_challenge}"
        else:
            prompt = default_prompt

        payload = {
            "model": "llama-3-sonar-large-32k-online",
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
            "authorization": f"Bearer {perplexity_api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']

    # Function to get OpenAI suggestions
    def get_openai_suggestions(results, openai_api_key, custom_prompt=None):
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)

        default_prompt = f"""Provide a report with suggestions based on what has been done to address the following product challenge: {result}.
                                Check for quality and known articles and websites only.
                        
                                The suggestions should tackle a relevant problem and should not be trivial.
                                The suggestions should be technically advanced and precise.

                            """

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following Results from Perplexity:\n{result}"
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
    st.title("What has been done with respect to an existing product challenge")

    # User input
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    perplexity_api_key = st.sidebar.text_input("Enter your Perplexity API Key", type="password")

    st.sidebar.divider()

    product_category = st.sidebar.text_input("Enter product category")
    product_challenge = st.sidebar.text_input("Enter product challenge")
    custom_perplexity_prompt = st.sidebar.text_area("Enter custom prompt for Perplexity API (optional)")
    custom_openai_prompt = st.sidebar.text_area("Enter custom prompt for OpenAI API (optional)")

    if st.button('Generate Suggestions'):
        st.write("Fetching suggestions, please wait...")

        # Generate suggestions from Perplexity API
        result = get_sustainable_design_suggestions(product_category, product_challenge,perplexity_api_key, custom_perplexity_prompt)

        # Display intermediate results
        st.subheader("Perplexity API Results:")
        st.write(result)

        # Generate final suggestions from OpenAI API
        final_suggestions = get_openai_suggestions(result, openai_api_key, custom_openai_prompt)

        # Display final suggestions
        st.subheader("Final Suggestions:")
        st.write(final_suggestions)



def dashboard3():
    import streamlit as st
    import requests

    # Function to get sustainable design suggestions from Perplexity API
    def get_latest_innovations(product_category, topic, perplexity_api_key, custom_prompt=None):
        url = "https://api.perplexity.ai/chat/completions"
        default_prompt = f"""Provide a report on the latest innovations and news in the product category {product_category} related to the topic {topic}.
                            Include recent advancements, trends, and technologies. Provide references and working links to relevant articles and websites.
                            Look for 10 suggestions.Provide references.
                            """

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following product category and topic:\n{product_category}\n{topic}"
        else:
            prompt = default_prompt

        payload = {
            "model": "llama-3-sonar-large-32k-online",
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
            "authorization": f"Bearer {perplexity_api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']

    # Function to get OpenAI suggestions
    def get_openai_suggestions(results, openai_api_key, custom_prompt=None):
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)

        default_prompt = f"""Provide a detailed report based on the latest innovations and news related to the following product category and topic: {result}.
                                Check for quality and known articles and websites only.
                        
                                The suggestions should tackle a relevant problem and should not be trivial.
                                The suggestions should be technically advanced and precise.
                            """

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following Results from Perplexity:\n{result}"
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
    st.title("Latest Innovations/News in a Product Category vs. a Specific Topic")

    # User input
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    perplexity_api_key = st.sidebar.text_input("Enter your Perplexity API Key", type="password")

    st.sidebar.divider()

    product_category = st.sidebar.text_input("Enter product category")
    topic = st.sidebar.text_input("Enter topic")
    custom_perplexity_prompt = st.sidebar.text_area("Enter custom prompt for Perplexity API (optional)")
    custom_openai_prompt = st.sidebar.text_area("Enter custom prompt for OpenAI API (optional)")

    if st.button('Generate Innovations'):
        st.write("Fetching latest innovations, please wait...")

        # Generate suggestions from Perplexity API
        result = get_latest_innovations(product_category, topic,perplexity_api_key, custom_perplexity_prompt)

        # Display intermediate results
        st.subheader("Perplexity API Results:")
        st.write(result)

        # Generate final suggestions from OpenAI API
        final_suggestions = get_openai_suggestions(result,openai_api_key, custom_openai_prompt)

        # Display final suggestions
        st.subheader("Final Suggestions:")
        st.write(final_suggestions)


def dashboard4():
    import streamlit as st
    import requests

    # Function to get sustainable design suggestions from Perplexity API
    def get_competitors(product_category, topic, perplexity_api_key, custom_prompt=None):
        url = "https://api.perplexity.ai/chat/completions"
        default_prompt = f"""Provide a report on the competitors in the product category {product_category} related to the topic {topic}.
                            Include major companies, their products, and any relevant information on their market strategies and innovations.
                            Provide references and working links to relevant articles and websites.
                            Look for 10 suggestions. Provide references.
                            """

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following product category and topic:\n{product_category}\n{topic}"
        else:
            prompt = default_prompt

        payload = {
            "model": "llama-3-sonar-large-32k-online",
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
            "authorization": f"Bearer {perplexity_api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']

    # Function to get OpenAI suggestions
    def get_openai_suggestions(results, openai_api_key, custom_prompt=None):
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)

        default_prompt = f"""Provide a detailed report based on the competitors in the following product category and topic: {result}.
                                Check for quality and known articles and websites only.
                        
                                The suggestions should tackle a relevant problem and should not be trivial.
                                The suggestions should be technically advanced and precise.
                            """

        if custom_prompt:
            prompt = custom_prompt
            prompt = f"{prompt}\n\n use the following Results from Perplexity:\n{result}"
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
    st.title("Competitors for a Product and Topic")

    # User input
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    perplexity_api_key = st.sidebar.text_input("Enter your Perplexity API Key", type="password")

    st.sidebar.divider()

    product_category = st.sidebar.text_input("Enter product category")
    topic = st.sidebar.text_input("Enter topic")
    custom_perplexity_prompt = st.sidebar.text_area("Enter custom prompt for Perplexity API (optional)")
    custom_openai_prompt = st.sidebar.text_area("Enter custom prompt for OpenAI API (optional)")

    if st.button('Generate Competitors'):
        st.write("Fetching competitors, please wait...")

        # Generate suggestions from Perplexity API
        result = get_competitors(product_category, topic, perplexity_api_key, custom_perplexity_prompt)

        # Display intermediate results
        st.subheader("Perplexity API Results:")
        st.write(result)

        # Generate final suggestions from OpenAI API
        final_suggestions = get_openai_suggestions(result,  openai_api_key, custom_openai_prompt)

        # Display final suggestions
        st.subheader("Final Suggestions:")
        st.write(final_suggestions)




page_names_to_funcs = {
    "Introduction": intro,
    "New Ideas/concepts": dashboard1,
    "what has been done with respect to an existing product 'challenge": dashboard2,
    "Latest Innovations": dashboard3,
    "competitors for a product and topic": dashboard4
}

dashboard_name = st.sidebar.selectbox("Choose a dashboard", page_names_to_funcs.keys())
page_names_to_funcs[dashboard_name]()
